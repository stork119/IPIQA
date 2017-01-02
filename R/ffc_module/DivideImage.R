### ### ### ### ###
### DivideImage ###
### ### ### ### ###

##### divide #####
divide <- function(image,
                   ncol = ffc.width, #1344,
                   nrow = ffc.height){
  ncol.def <- ncol(image)
  nrow.def <- nrow(image)
  
  images.list <- list()
  
  for(j in 1:(ncol.def/ncol)){
    for(i in 1:(nrow.def/nrow)){
      images.list[[(j-1)*(ncol.def/ncol) + i]] <- 
        image[((i-1)*nrow + 1):(i*nrow), ((j-1)*ncol + 1):(j*ncol)]
    } 
  }
  return(images.list)
}

##### Divide Image #####
DivideImageList <- function(input.dir,
                            output.dir,
                            output.name,
                            ncol = ffc.width,#1344,#ffc.width,
                            nrow = ffc.height,
                            output = FALSE){
  image <- readTIFF(input.dir)
  ncol.def <- ncol(image)
  nrow.def <- nrow(image)
  
  images.list <- list()
  
  for(j in 1:(ncol.def/ncol)){
    for(i in 1:(nrow.def/nrow)){
      images.list[[(j-1)*(ncol.def/ncol) + i]] <- 
        image[((i-1)*nrow + 1):(i*nrow), ((j-1)*ncol + 1):(j*ncol)]
      writeTIFF(what = images.list[[(j-1)*(ncol.def/ncol) + i]],
                where = paste(output.dir, "/", output.name, "-", i, "-", j, ".tif", sep = "" ),  
                bits.per.sample = 16,
                compression = "none",
                reduce = FALSE
      )
    } 
  }
  if(output){
    return(images.list)
  } else{
    return()
  }
}

##### Divide Image #####
DivideImage <- function(input.dir,
                        output.dir,
                        output.name,
                        ncol = ffc.width, #1344,#ffc.width,
                        nrow = ffc.height){
  image <- readTIFF(input.dir)
  ncol.def <- ncol(image)
  nrow.def <- nrow(image)
  
  data <- c()
  for(j in 1:(ncol.def/ncol)){
    for(i in 1:(nrow.def/nrow)){
      image.tmp <- 
        image[((i-1)*nrow + 1):(i*nrow), ((j-1)*ncol + 1):(j*ncol)]
      writeTIFF(what = image.tmp,
                where = paste(output.dir, "/", output.name, "-", i, "-", j, ".tif", sep = "" ),  
                bits.per.sample = 16,
                compression = "none",
                reduce = FALSE
      )
      data <- c(data, mean(image.tmp))
    } 
  }
  
  return(data)
}