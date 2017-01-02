### ### ### ### ### ###
### ImageCalculator ###
### ### ### ### ### ###

#### writeTIFFDefault ####
writeTIFFDefault <- function(what, where){
  writeTIFF(what = what, 
            where =  where,
            bits.per.sample = 16,
            compression = "none")
}

#### merge ####
merge <- function(img, 
                  nrow              = ffc.height,
                  ncol              =  ffc.width,#ffc.width,#ffc.width,
                  resize            = 4,
                  nrow.resize       = resize*nrow,
                  ncol.resize       = resize*ncol,
                  ncol.merge = ncol.resize/ncol,
                  nrow.merge = nrow.resize/nrow){
  img.tmp <- img
  for( i in 1:(nrow.merge - 1) ){ 
    img.tmp <- rbind(img.tmp, img)
  }
  img.tmp.col <- img.tmp 
  for( i in 1:(ncol.merge - 1) ){ 
    img.tmp.col <- cbind(img.tmp.col, img.tmp)
  }
  return(img.tmp.col)
}


#### getMeanImage ####
getMeanImage <- function(input.dir, 
                         output.dir,
                         nrow = ffc.height,
                         ncol =  ffc.width,#ffc.width,
                         pattern = ".*Alexa.*tif"){
  
  images.list <- lapply(list.files(input.dir,
                                   pattern = pattern,
                                   recursive = TRUE),
                        function(ref.name){
                          print(ref.name)
                          readTIFF( paste(input.dir, 
                                          ref.name,
                                          sep ="/"))
                        })
  
  images.div.list <- list()
  for(i in 1:length(images.list)){
    images.div.list <- c(images.div.list,
                         divide(images.list[[i]],
                                nrow = nrow, 
                                ncol = ncol))
  }
  
  
  images.mean <- matrix(data = rep(x = 0, times = nrow*ncol), 
                        nrow = nrow, 
                        ncol = ncol)
  
  for(i in 1:length(images.div.list)){
    images.mean <- images.mean + images.div.list[[i]]
  }
  images.mean <- images.mean/length(images.div.list)
  
  
  writeTIFFDefault(what = images.mean,
                   where = output.dir)
  images.mean
}

#### getMeanImageMatrix ####
getMeanImageMatrix <- function(
  images.list,
  nrow = ffc.height,
  ncol = ffc.width#ffc.width#ffc.width
  ){
  
  images.mean <- matrix(data = rep(x = 0, times = nrow*ncol), 
                        nrow = nrow, 
                        ncol = ncol)
  
  for(i in 1:length(images.list)){
    images.mean <- images.mean + images.list[[i]]
  }
  images.mean <- images.mean/length(images.list)
  
  return(images.mean)
}