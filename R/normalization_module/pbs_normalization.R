### ###
###
### pbs normalization module
###
### ###

#### PREPROCESSING  ####

### libraries ###
try({package.list <- list()
package.load <- sapply(package.list, function(package.name){
  package.exist <- require(package.name, character.only = TRUE)
  if(!package.exist){
    install.packages(package.name)
    return(library(package.name, character.only = TRUE))
  }
  return(package.exist)
})
})

pbs_normalization <- function(camcor_path,
                              input_path,
                              output_path,
                              filename,
                              delimeter = ",",
                              pbs_ref = 0.0003,
                              ...
                              ){
  
  pbs_ref <- as.integer(pbs_ref)
  camcor_path <- normalizePath(camcor_path, "/")
  input_path <-  normalizePath(paste(input_path, filename, sep = "/"), "/")

  camcor <- read.table(file = camcor_path, header = TRUE, sep = delimeter)
  
  data <- read.table(file = input_path, header = TRUE, sep = delimeter)
  data.intensity_colnames <- grepl("Intensity", colnames(data)) & !grepl("Location", colnames(data))
  
  data[,data.intensity_colnames] <- data[,data.intensity_colnames]*pbs_ref/camcor$pbs
  try({
    output_path <- normalizePath(paste(output_path, sep = "/"), "/")
    dir.create(output_path, recursive = TRUE)
    output_path <- normalizePath(paste(output_path, filename, sep = "/"), "/")
    write.table(x = data, file = output_path, col.names  = TRUE, sep = delimeter)
  })
}

pbs_normalization <- function(camcor_path,
                              input_path,
                              output_path,
                              filename,
                              delimeter = ",",
                              pbs_ref = 0.0003,
                              ...
){
  
  pbs_ref <- as.integer(pbs_ref)
  camcor_path <- normalizePath(camcor_path, "/")
  input_path <-  normalizePath(paste(input_path, filename, sep = "/"), "/")
  
  camcor <- read.table(file = camcor_path, header = TRUE, sep = delimeter)
  
  data <- read.table(file = input_path, header = TRUE, sep = delimeter)
  data.intensity_colnames <- grepl("Intensity", colnames(data)) & !grepl("Location", colnames(data))
  
  data[,data.intensity_colnames] <- data[,data.intensity_colnames]*pbs_ref/camcor$pbs
  try({
    output_path <- normalizePath(paste(output_path, sep = "/"), "/")
    dir.create(output_path, recursive = TRUE)
    output_path <- normalizePath(paste(output_path, filename, sep = "/"), "/")
    write.table(x = data, file = output_path, col.names  = TRUE, sep = delimeter)
  })
}

#### ####
background_normalization <- function(background_path,
                              input_path,
                              output_path,
                              filename,
                              delimeter = ",",
                              fun_norm  = function(data, data_norm){return(data - data_norm)}, 
                              ...
){
  
  background_path <- normalizePath(background_path, "/")
  input_path <-  normalizePath(paste(input_path, filename, sep = "/"), "/")
  
  image_data <- read.table(file = background_path, header = TRUE, sep = delimeter)
  #background$Intensity_MeanIntensity_Background
  data <- read.table(file = input_path, header = TRUE, sep = delimeter)
  
  image_data.intensity_colnames <- colnames(image_data)[grepl("^Intensity_[A-z]*Intensity_Background$",
                                                        colnames(image_data))]
  image_data.intensity_colnames_stop <- sapply(gregexpr("^Intensity_[A-z]*Intensity_", image_data.intensity_colnames),
                                         function(l){return(attr(l, "match.length"))})
  data.intensity_regex <- sapply(1:length(image_data.intensity_colnames_stop),
         function(i){substr(image_data.intensity_colnames[i], 1, image_data.intensity_colnames_stop[i])})
    
  
# data.intensity_colnames[ sapply(gregexpr("^.*?Background",data.intensity_colnames), function(l){return(attr(l, "match.length"))}))
  
  for(image.i in 1:nrow(image_data)){
    image <- image_data[image.i,]
    for(regex.i in 1:length(data.intensity_regex)){
      regex <- data.intensity_regex[regex.i]
      data.intensity_colnames <- grepl(regex,
                                    colnames(data))
      if(sum(data.intensity_colnames) > 0){
        data[data$position.name == image$position.name, data.intensity_colnames]  <-  
          fun_norm(data[
            data$position.name == image$position.name,
            data.intensity_colnames], 
            image[,image_data.intensity_colnames[regex.i]])  
      }
    }
  }
  
  try({
    output_path <- normalizePath(paste(output_path, sep = "/"), "/")
    dir.create(output_path, recursive = TRUE)
    output_path <- normalizePath(paste(output_path, filename, sep = "/"), "/")
    write.table(x = data, file = output_path, col.names  = TRUE, sep = delimeter)
  })
}