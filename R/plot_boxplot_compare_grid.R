### ###
###
### plot_boxplot_compare_grid
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
source(paste(wd.tmp, "plot_boxplot_compare.R", sep = "/"))

plot_boxplot_compare_grid <- function(data,
                                      path,
                                      filename = "boxplot", 
                                      grid.col,
                                      grid.col.name,
                                      boxplot.group,
                                      plot.width = 24,
                                      plot.height = 8,
                                      args.filename = list(),
                                      theme.text_size = 12
){
  
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
                                                plot.width = plot.height
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
