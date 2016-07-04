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
wd.tmp <- "X:/EG/CellProfiller/Analysis/2016-06-16-pstat1-summary/"
source(paste(wd.tmp, "theme_jetka.R", sep = ""))


#### plot_histogram ####
plot_histogram <- function(data,
                           filename = "",
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
                           line.size = 1.5,
                           save.plot = TRUE){
  
  if(nrow(data) > data_nrow_min){  
    gplot <- ggplot(data = data) +
      geom_histogram(aes_string(x = x, "..density.."), binwidth = bin_width) +
      xlim(xlim.min, xlim.max) + 
      ggtitle(plot.title) +
      theme_jetka(text_size = theme.text_size)
    if(save.plot){
      ggsave(filename = paste(filename, ".pdf", sep = ""),
             plot = gplot,
             width = plot.width,
             height = plot.height,
             useDingbats = FALSE)
    }
    return(gplot)
  }
  return()
}


#### plot_histogram_list ####
plot_histogram_list <- function(data,
                                path,
                                filename = "boxplot", 
                                grid.col,
                                grid.col.name = grid.col,
                                args.filename = list(),
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
                                line.size = 1.5
                                
){
  
  
  grid <- expand.grid(sapply(grid.col, function(g){unique(data[,g])}))
  plots.list <- list()
  

  filename.global <- paste(path,
                           filename,
                           sep = "/")
  
  dir.create(path = path, recursive = TRUE)
  
  for(i in 1:nrow(grid)){  
    try({
      data.tmp <- data[as.logical(
        apply(
          sapply(1:length(grid.col),
                 function(j){ 
                   data[,grid.col[j]] == grid[i,j]}),
          1,
          prod)),]
      
      plot.title <- paste("cells = ",
                          data.tmp$cells[1],
                          paste(sapply(1:length(grid.col),
                                       function(j){ 
                                         paste(grid.col.name[j], "=", grid[i,j])}
                          ), collapse = " ")
      )
    
      plots.list[[i]] <-   plot_histogram(data.tmp,
                                          x = x,
                                          plot.width = plot.width,
                                          plot.height = plot.height,
                                          plot.title = plot.title,
                                          theme.text_size = theme.text_size,
                                          line.size = line.size,
                                          save.plot = FALSE
                                          
      )
    })
  }
  
  try({dev.off()})
  pdf(file = paste(filename.global, ".pdf", sep = ""),
      useDingbats = FALSE,
      width = plot.width,
      height = plot.height)
  l <- lapply(plots.list, print)
  dev.off()
}


#### plot_histogram_grid ####
plot_histogram_grid <- function(data,
                                path,
                                filename,
                                x = "Intensity_IntegratedIntensity_DAPI",
                                grid.x,
                                grid.y,
                                data_nrow_min = 10,
                                ylab = grid.y,
                                xlab = grid.x,
                                xlim.min = 0,
                                xlim.max = max(data[,x]),
                                bin_number = 50,
                                bin_width = (xlim.max - xlim.min)/bin_number,
                                plot.width = 64,
                                plot.height = 64,
                                plot.title = "",
                                theme.text_size = 48,
                                line.size = 1.5){
  dir.create(path = path, recursive = TRUE)
  data[,grid.x] <- factor(data[,grid.x])
  data[,grid.y] <- factor(data[,grid.y])
  if(nrow(data) > data_nrow_min){  
    gplot <- ggplot(data = data) +
      geom_histogram(aes_string(x = x, "..density.."), binwidth = bin_width) +
      facet_grid(facets = paste(grid.x, "~", grid.y, sep =" " )) +
      xlim(xlim.min, xlim.max) + 
      ggtitle(plot.title) +
      theme_jetka(text_size = theme.text_size)
    ggsave(filename = paste(path, "/", filename, ".pdf", sep = ""),
           plot = gplot,
           width = plot.width,
           height = plot.height,
           useDingbats = FALSE,
           limitsize = FALSE)
    return(gplot)
  }
  return()
}