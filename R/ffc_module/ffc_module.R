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
wd.tmp <- "C:/Users/Pathway/Documents/IPIQA/PathwayPackage/R/ffc_module/"
l <- lapply(list("DivideImage", "ImageCalculator"), 
       function(f){source(paste(wd.tmp, f, ".R", sep = ""))})
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


fun_camcor_analyse <- function(input_path,
                               output_path,
                               well_path_regex = "Well\\s[A-Z]\\d\\d$",
                               well_file_regex = ".tif$",
                               logical_divide_images = TRUE,
                               pbs_ind = 1,
                               ...
                               ){
  
  try({
    input_path <- normalizePath(input_path, "/")
    output_path <- normalizePath(output_path, "/")
    dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)})
  wells.list <- list.files(path = input_path)
  wells.list <- wells.list[grep(well_path_regex, wells.list)]
  
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
      DivideImage(input.dir = well.input.path,
                  output.dir = well.output.path,
                  output.name = well.name,
                  ncol = 1392,
                  nrow = 1024,
                  output = FALSE)
    }
    image.ref.mean[[well]] <- getMeanImage(input.dir = well.output.path,
                                           output.dir = paste(output_path,
                                                              well, ".tif",
                                                              sep = ""),
                                           pattern = ".*Alexa.*tif")
  }
  
  image.pbs <- fun_ref_image(image.ref.mean = image.ref.mean, ind = pbs_ind)
  ref_ind <- (1:length(image.ref.mean))[-pbs_ind]
  image.ref <- fun_ref_image(image.ref.mean = image.ref.mean, ind = ref_ind)
  
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

ffc <- function(image,
                data_camcor_pbs,
                data_camcor_ref,
                GLOBAL.sref.factor){
  signal1 <- image - data_camcor_pbs
  signal1[signal1 < 0] <- 0
  signal2 <- signal1/data_camcor_ref 
  signal3 <- GLOBAL.sref.factor*signal2
  signal3[signal3 < 0] <- 0
  return(signal3)
}

fun_camcor_apply <- function(input_path,
                             output_path,
                             data_camcor_pbs,
                             data_camcor_ref,
                             image_regex = list("^Alexa.*\\.tif$", "^DAPI.*\\.tif$"),
                             GLOBAL.sref.factor = 0.01,
                             ...
){
  input_path <- normalizePath(input_path, "/")
  output_path <- normalizePath(output_path, "/")
  images.list <- list.files(path = input_path)
  for(regex in image_regex){
    image.name <- images.list[grep(regex, images.list)]
    image <- readTIFF(paste(input_path,
                            image.name,
                            sep = "/"))
    signal3 <- ffc(image,
                   data_camcor_pbs,
                   data_camcor_ref,
                   GLOBAL.sref.factor)
    try({dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)
      writeTIFF(what = signal3,
              where = paste(output_path,
                            image.name,
                            sep = "/"),  
              bits.per.sample = 16,
              compression = "none",
              reduce = FALSE
      )
    })
  }
  
}
  