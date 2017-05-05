### ###
###
### flat field correction module
###
### ###

#### PREPROCESSING  ####

### libraries ###
try({package.list <- list("tiff")
     package.load <- sapply(package.list, function(package.name){
       package.exist <- require(package.name, character.only = TRUE)
       if(!package.exist){
         install.packages(package.name)
         return(library(package.name, character.only = TRUE))
       }
       return(package.exist)
     })
})

### sources ###
ffc.width <- 1392#1344
ffc.height <- 1024

wd.tmp <- dirname(sys.frame(1)$ofile)
l <- lapply(list("DivideImage.R", "ImageCalculator.R"), 
            function(f){source(normalizePath(paste(wd.tmp, f, sep = "//"), "/"))})
rm(l)

fun_ref_image <- function(image.ref.mean,
                          ind){
  image.ref <- matrix(0,
                      nrow = nrow(image.ref.mean[[ind[1]]]),
                      ncol = ncol(image.ref.mean[[ind[1]]]))
  
  for(ref_i in ind){
    image.ref <- image.ref + image.ref.mean[[ref_i]]
  }
  image.ref <- image.ref/length(ind) 
  return(image.ref)
}


fun_camcor_create <- function(input_path,
                               output_path,
                               well_path_regex = "Well\\s[A-Z]\\d\\d$",
                               well_file_regex = ".tif$",
                               logical_divide_images = TRUE,
                               pbs_ind = 1,
                               save_files = FALSE,
                               delimeter = ",",
                               ...
                               ){
  try({
    input_path <- normalizePath(input_path, "/")
    output_path <- normalizePath(output_path, "/")
    dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)})
  wells.list <- list.files(path = input_path)
  wells.list <- wells.list[grep(well_path_regex, wells.list)]
  df.camcor <- matrix( nrow= 0, ncol = 16)
  image.ref.mean <- list()
  camcor.df <- data.frame(x = numeric(), y = numeric(), val = numeric(), ref = numeric())
  for(well in wells.list){
    well.output.path <- paste(output_path, well, "/", sep = "/")
    try({dir.create(path = well.output.path, recursive = TRUE, showWarnings = FALSE)})
    well.input.path <- paste(input_path, well, sep = "/")
    well.list <- list.files(path = well.input.path)
    well.name <- well.list[grep(well_file_regex, well.list)]
    well.input.path <- paste(well.input.path, well.name, sep = "/")
    if(logical_divide_images){
      df.camcor<- rbind(df.camcor,
                        DivideImage(input.dir = well.input.path,
                  output.dir = well.output.path,
                  output.name = well.name,
                  ncol = ffc.width,#1392,#1344,#1392,
                  nrow = ffc.height))
    }
    print(well.output.path)
    image.ref.mean[[well]] <- getMeanImage(input.dir = well.output.path,
                                           output.dir = paste(output_path,
                                                              well, ".tif",
                                                              sep = ""),
                                           pattern = ".*Alexa.*tif")
    if(!save_files){
      file.remove(list.files(normalizePath(well.output.path, "/"), full.names = TRUE), recursive = TRUE)
    }
    gc()
  }
  
  image.pbs <- fun_ref_image(image.ref.mean = image.ref.mean, ind = pbs_ind)
  ref_ind <- (1:length(image.ref.mean))[-pbs_ind]
  image.ref <- fun_ref_image(image.ref.mean = image.ref.mean, ind = ref_ind)
  
  write.table(row.names = FALSE, col.names = TRUE,
              file = paste(output_path,
                           "camcor.csv",
                           sep = ""),
              x = data.frame(pbs = mean(image.pbs), ref = mean(image.ref)), 
              sep = delimeter)

  write.table(row.names = FALSE, col.names = TRUE,
              file = paste(output_path,
                           "camcor-images.csv",
                           sep = ""),
              x = df.camcor,
              sep = delimeter)
  
  
  image.ref.rel <- image.ref - image.pbs
 
  data_camcor_pbs <- merge(img = image.pbs)

  writeTIFF(what = data_camcor_pbs,
            where = paste(output_path,
                          "PBS.tif",
                          sep = ""),  
            bits.per.sample = 16,
            compression = "none",
            reduce = FALSE
  )

  
    data_camcor_ref  <- merge(img = image.ref.rel)
  writeTIFF(what = data_camcor_ref,
            where = paste(output_path,
                          "REF.tif",
                          sep = ""),  
            bits.per.sample = 16,
            compression = "none",
            reduce = FALSE
  )
  return(list(
    data_camcor_pbs = data_camcor_pbs,
    data_camcor_ref = data_camcor_ref))
}

fun_camcor_read <- function(output_path,
                            ...
){
  
    data_camcor <- list()
    data_camcor[["data_camcor_pbs"]] <-  readTIFF(paste(output_path,
                          "PBS.tif",
                          sep = ""))
    data_camcor[["data_camcor_ref"]] <- readTIFF(paste(output_path,
                          "REF.tif",
                          sep = ""))
  return(data_camcor)
}


ffc <- function(image,
                data_camcor_pbs,
                data_camcor_ref,
                GLOBAL.sref.factor){
  print(memory.size(max = FALSE))
  print(memory.size(max = TRUE))
  
  image <- image - data_camcor_pbs
  image[image < 0] <- 0
  image <- image/data_camcor_ref 
  #signal3 <- GLOBAL.sref.factor*signal2
  image <- mean(data_camcor_ref)*image 
  ### we don't assume that reference signal is constant between experiments
  image[image < 0] <- 0
  return(image)
}

fun_camcor_apply <- function(input_path,
                             output_path,
                             data_camcor_pbs,
                             data_camcor_ref,
                             regex,
                             #image_regex = list("^Alexa.*\\.tif$", "^DAPI.*\\.tif$"),
                             GLOBAL.sref.factor = 0.01,
                             ...
){
  input_path <- normalizePath(input_path, "/")
  output_path <- normalizePath(output_path, "/")
  images.list <- list.files(path = input_path)
 # for(regex in image_regex){
    image.name <- images.list[grep(regex, images.list)]
    print(image.name)
    gc()
    image <- readTIFF(paste(input_path,
                            image.name,
                            sep = "/"))
    image <- ffc(image,
                   data_camcor_pbs,
                   data_camcor_ref,
                   GLOBAL.sref.factor)
    try({dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)
      writeTIFF(what = image,
              where = paste(output_path,
                            image.name,
                            sep = "/"),  
              bits.per.sample = 16,
              compression = "none",
              reduce = FALSE
      )
    })
  #}
  
}

fun_camcor_read_apply <- function(camcor_path,
                                  input_path,
                                  output_path,
                                  regex_name = NULL,
                                  image_regex = list("^Alexa.*\\.tif$", "^DAPI.*\\.tif$"),
                                  GLOBAL.sref.factor = 0.01,
                                  ...
){
  tryCatch({
  print(regex_name)
  memory.limit(size=1800)
  #print(memory.size(max = TRUE))
  #print(memory.limit())
  if(!is.null(regex_name)){
    image_regex <- list(paste("^", regex_name, ".*\\.tif$", sep = ""))
  }
  gc()
  camcor <- fun_camcor_read(output_path = camcor_path)
    gc()
  for(regex in image_regex){
    gc()
    print(regex)
    fun_camcor_apply(input_path = input_path,
                   output_path = output_path,
                   data_camcor_pbs = camcor[["data_camcor_pbs"]],
                   data_camcor_ref = camcor[["data_camcor_ref"]],
                   regex = regex,
                   GLOBAL.sref.factor = GLOBAL.sref.factor,
                   ...)
          }
          }, error = function(e){print(e)})
  return()
}
  
