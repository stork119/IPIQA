### ### ### ### ###
### DivideImage ###
### ### ### ### ###

##### divide #####
divide <- function(image, ncol = 1392, nrow = 1024){
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
DivideImage <- function(input.dir,
                        output.dir,
                        output.name,
                        ncol = 1392,
                        nrow = 1024,
                        output = TRUE){
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

