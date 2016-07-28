### ###
###
### plot_density
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
# wd.tmp <- "" ### Rstudio 
wd.tmp <- dirname(sys.frame(1)$ofile) ### script
source(paste(wd.tmp, "theme_jetka.R", sep = "/"))


#### MAIN ####
plot_density <- function(data,
                         filename,
                         x = "Intensity_IntegratedIntensity_DAPI",
                         data_nrow_min = 10,
                         ylab = "density",
                         xlab = x,
                         xlim_min = 0,
                         xlim_max = max(data[,x]),
                         bin_number = 50,
                         bin_width = 0,
                         plot_width = 24,
                         plot_height = 8,
                         plot_title = "",
                         theme_text_size = 12,
                         line_size = 1.5,
                         normalize_data   = TRUE, 
                         normalize_factor = 65535){
  

  xlim_min <- as.integer(xlim_min)
  xlim_max  <- as.integer(xlim_max)
  bin_number <- as.integer(bin_number)
  bin_width  <- as.integer(bin_width)
  if(bin_width == 0){
    bin_width <- (xlim_max - xlim_min)/bin_number
  }
  plot_width <- as.integer(plot_width)
  plot_height <- as.integer(plot_height)
  plot_title <- as.integer(plot_title)
  theme_text_size <- as.integer(theme_text_size)
  normalize_data <- as.integer(normalize_data)
  normalize_factor <- as.integer(normalize_factor)
  
  if(normalize_data){
    data[,x] <- normalize_factor*data[,x]
  }
  
  if(nrow(data) > data_nrow_min){  
    gplot <- ggplot(data = data) +
      geom_density(aes_string(x = x, "..density.."), line.size = line_size) +
      xlim(xlim_min, xlim_max) + 
      ggtitle(plot_title) +
      theme_jetka(text_size = theme_text_size)
    ggsave(filename = paste(filename, ".pdf", sep = ""),
           plot = gplot,
           width = plot_width,
           height = plot_height,
           useDingbats = FALSE)
    return(gplot)
  }
  return()
}
