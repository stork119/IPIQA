### ###
###
### plot_histogram
###
### ###

#### PREPROCESSING  ####

### libraries ###
try({package.list <- list("ggplot2")
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
wd.tmp <- "C:/Users/Pathway/Documents/PathwayPackage/R/"
source(paste(wd.tmp, "theme_jetka.R", sep = ""))


#### MAIN ####
plot_histogram <- function(data,
                           filename,
                           x = "Intensity_IntegratedIntensity_DAPI",
                           data_nrow_min = 10,
                           ylab = "density",
                           xlab = x,
                           xlim.min = 0,
                           xlim.max = max(data[,x]),
                           bin_number = 50,
                           bin_width = (xlim.max - xlim.min)/bin_number,
                           plot.width = 24,
                           plot.height = 8,
                           plot.title = "",
                           theme.text_size = 12,
                           line.size = 1.5){
#  print(colnames(data))
#  print(x %in% colnames(data))
  if(nrow(data) > data_nrow_min){  
    gplot <- ggplot(data = data) +
      geom_histogram(aes_string(x = x, "..density.."), binwidth = bin_width) +
      xlim(xlim.min, xlim.max) + 
      ggtitle(plot.title) +
      theme_jetka(text_size = theme.text_size)
    ggsave(filename = paste(filename, ".pdf", sep = ""),
           plot = gplot,
           width = plot.width,
           height = plot.height,
           useDingbats = FALSE)
    return(gplot)
  }
  return()
}
