### ###
###
### normalize_data
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

### sources ###
# wd.tmp <- "X:/EG/CellProfiller/Analysis/2016-06-16-pstat1-summary/"
# source(paste(wd.tmp, "theme_jetka.R", sep = ""))

normalize_data <- function(data,
                   normalize_factor = 65535){
  
  data.intensity_colnames <- grepl("Intensity", colnames(data)) & !grepl("Location", colnames(data))
  data[,data.intensity_colnames] <- data[,data.intensity_colnames]*normalize_factor
  return(data)
}