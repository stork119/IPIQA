### ###
# 8function : pp.boxplot
# author : knt
#
### ###

# data - data.frame
# filename - path to plot output file 
# y - column with intensities "Nuclei.Intensity_MeanIntensity_CHA" or "Nuclei.Intensity_IntegratedIntensity_CHA"
# x - "compare.1.1"
# boxplot.group - "PositionName" or "ImageNumber"
# x_axis.group - "group.?.?"

library("ggplot2") ### ???

# data <- read.csv(file = "E:/AG/PathwayPackage/resources/output/2016-06-07/raw/map_plate/Nuclei.csv", sep = "\t", header = TRUE)
# filename <- "C:/Users/Pathway/Desktop/machlojki/plot.pdf"
# x <- "compare.1.1"
# y <- "Intensity_MeanIntensity_CHA"
# boxplot.group <-"PositionName"
# x_axis.group <- "group.1.1"


pp.boxplot <- function(
  data,
  filename,
  x,
  y,
  boxplot.group,
  x_axis.group,
  facet_grid.group = x_axis.group,
  ylab = y,
  xlab = x,
  ylim.min = 0,
  ylim.max = max(as.numeric(data[, y])),
  plot.width = 24,
  plot.height = 14,
  xlab.angle = 90,
  xlab.hjust = 0,
  legend.position = "bottom",
  plot_fun = "geom_boxplot"){
  
  data[,y] <- as.numeric(data[,y])
  
  gplot <- ggplot(data = data, 
                  aes_string(x = x,
                             y = y,
                             group = boxplot.group),
                  group = x_axis.group
  ) + 
    do.call(plot_fun, args = list()) +
    ylim(ylim.min, ylim.max) +
    xlab(xlab) +
    ylab(ylab) + 
    facet_grid(paste("~", facet_grid.group, sep = ""))+
    theme(legend.position = "bottom",
          axis.text.x = element_text(angle = xlab.angle,
                                     hjust = xlab.hjust))
  ggsave(filename = filename,
         plot = gplot,
         width = plot.width,
         height = plot.height,
         useDingbats = FALSE)
}
