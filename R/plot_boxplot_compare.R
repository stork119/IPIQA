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
# wd.tmp <- "" ### Rstudio 
wd.tmp <- dirname(sys.frame(1)$ofile) ### script
source(paste(wd.tmp, "theme_jetka.R", sep = "/"))
source(paste(wd.tmp, "data_library.R", sep = "/"))


#### plot_boxplot_compare ####
plot_boxplot_compare <- function(data,
                                 ...,
                                 output_path,
                               filename,
                               x = "time",
                               y = "Intensity_IntegratedIntensity_DAPI",
                               boxplot_group = x,
                               ylab = y,
                               xlab = x,
                               ylim_min = 0,
                               ylim_max = 2000,
                               plot_width = 24,
                               plot_height = 8,
                               plot_title = "",
                               xlab_angle = 90,
                               xlab_hjust = 0,
                               legend_position = "bottom",
                               plot_fun = "geom_boxplot",
                               theme_text_size = 12,        
                               normalize_data   = TRUE, 
                               normalize_factor = 65535,
                               ylim_max_const = FALSE){
  
  ylim_min <- as.integer(ylim_min)
  ylim_max  <- as.integer(ylim_max)
  plot_width <- as.integer(plot_width)
  plot_height <- as.integer(plot_height)
  xlab_angle <- as.integer(xlab_angle)
  xlab_hjust <- as.integer(xlab_hjust)
  theme_text_size <- as.integer(theme_text_size)
  normalize_data <- as.integer(normalize_data)
  normalize_factor <- as.integer(normalize_factor)
  ylim_max_const <- as.integer(ylim_max_const)
  
  if(!CheckColumnExistence(data = data, list(x,y,boxplot_group))){
    return()
  }
  
  if(normalize_data){
    data[,y] <- normalize_factor*data[,y]
  }
  if(!ylim_max_const){
    ylim_max <- 1.2*max(data[,y])
  }
  
  gplot <- ggplot(data = data, 
                  aes_string(x = x,
                             y = y,
                             group = boxplot_group)
  ) + 
    do.call(plot_fun, args = list()) +
    ylim(ylim_min, ylim_max) +
    xlab(xlab) +
    ylab(ylab) + 
    ggtitle(plot_title) +
    theme_jetka(text_size = theme_text_size)
  try({
    output_path <- normalizePath(output_path, "/")
    dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)
    
  ggsave(filename = paste(output_path, "/", filename, ".pdf", sep = ""),
         plot = gplot,
         width = plot_width,
         height = plot_height,
         useDingbats = FALSE)
  })
  return()
}

#### plot_boxplot_compare_grid ####
plot_boxplot_compare_grid <- function(data,
                                      path,
                                      filename = "boxplot", 
                                      grid.col,
                                      grid.col.name,
                                      boxplot.group,
                                      plot.width = 24,
                                      plot.height = 8,
                                      args.filename = list(),
                                      theme.text_size = 12,
                                      ...
){
  if(!CheckColumnExistence(data = data, list(x,y))){
    return()
  }
  
  plot_width <- as.integer(plot_width)
  plot_height <- as.integer(plot_height)
  
  grid <- expand.grid(sapply(grid.col, function(g){unique(data[,g])}))
  plots.list <- list()
  
  filename.global.path <- paste(path,
                                paste(unlist(args.filename), collapse = "/"),
                                paste(grid.col, collapse = "-"),
                                sep = "/")
  
  filename.global <- paste(filename.global.path,
                           "boxplot",
                           sep = "/")
  
  dir.create(path = filename.global.path, recursive = TRUE)
  
  for(i in 1:nrow(grid)){
    try({
      data.tmp <- data[as.logical(
        apply(
          sapply(1:length(grid.col),
                 function(j){ 
                   data[,grid.col[j]] == grid[i,j]}),
          1,
          prod)),]
      
      data.tmp[,boxplot.group] <- factor(data.tmp[,boxplot.group],
                                         levels = sort(as.character(unique(data.tmp[,boxplot.group]))))
      
      plot.title <- paste("cells = ",
                          data.tmp$cells[1],
                          paste(sapply(1:length(grid.col),
                                       function(j){ 
                                         paste(grid.col.name[j], "=", grid[i,j])}
                          ), collapse = " ")
      )
      
      filename <- paste(filename.global, "-",
                        paste(sapply(1:length(grid.col),
                                     function(j){ 
                                       paste(grid.col[j], grid[i,j], sep = "-")}),
                              collapse = "-"), sep = "")
      plots.list[[i]] <-   plot_boxplot_compare(data.tmp,
                                                filename= filename,
                                                x = boxplot.group,
                                                y = "ShrinkedNuclei.Intensity",
                                                boxplot.group = boxplot.group,
                                                theme.text_size = theme.text_size,
                                                plot.title = plot.title,
                                                ylab = "Intensity",
                                                xlab = "",
                                                plot.height = plot.height,
                                                plot.width = plot.height,
                                                ...
      )
    })
  }
  
  try({dev.off()})
  pdf(file = paste(filename.global, ".pdf", sep = ""),
      width = plot.width,
      height = plot.height,
      useDingbats = FALSE)
  l <- lapply(plots.list, print)
  dev.off()
}
