### ###
###
###
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
wd.tmp <- "C:/Users/Pathway/Documents/IPIQA/PathwayPackage/R/"
source(paste(wd.tmp, "theme_jetka.R", sep = ""))


#### MAIN ####
plot_boxplot_compare <- function(data,
                                 ...,
                                 output_path,
                               filename,
                               x = "time",
                               y = "Intensity_IntegratedIntensity_DAPI",
                               boxplot.group = x,
                               ylab = y,
                               xlab = x,
                               ylim.min = 0,
                               ylim.max = 2000,
                               plot.width = 24,
                               plot.height = 8,
                               plot.title = "",
                               xlab.angle = 90,
                               xlab.hjust = 0,
                               legend.position = "bottom",
                               plot_fun = "geom_boxplot",
                               theme.text_size = 12){
  data[,y] <- 65535*data[,y]
  ylim.max <- 1.2*max(data[,y])
  gplot <- ggplot(data = data, 
                  aes_string(x = x,
                             y = y,
                             group = boxplot.group)
  ) + 
    do.call(plot_fun, args = list()) +
    ylim(ylim.min, ylim.max) +
    xlab(xlab) +
    ylab(ylab) + 
    ggtitle(plot.title) +
    theme_jetka(text_size = theme.text_size)
  try({
    output_path <- normalizePath(output_path, "/")
    dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)
    
  ggsave(filename = paste(output_path, "/", filename, ".pdf", sep = ""),
         plot = gplot,
         width = plot.width,
         height = plot.height,
         useDingbats = FALSE)
  })
  return()
}