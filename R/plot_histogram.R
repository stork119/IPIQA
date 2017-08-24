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
# wd.tmp <- "" ### Rstudio
wd.tmp <- dirname(sys.frame(1)$ofile) ### script
source(paste(wd.tmp, "theme_jetka.R", sep = "/"))
source(paste(wd.tmp, "data_library.R", sep = "/"))

#### plot_histogram ####
plot_histogram <- function(data,
                           output_path = "",
                           filename = "",
                           x = "Intensity_IntegratedIntensity_DAPI",
                           data_nrow_min = 10,
                           ylab = "density",
                           xlab = x,
                           xlim_min = 0,
                           xlim_max = max(as.numeric(data[,x])),
                           bin_number = 50,
                           bin_width = (xlim_max - xlim_min)/bin_number,
                           plot_width = 24,
                           plot_height = 8,
                           plot_title = "",
                           theme_text_size = 12,
                           line_size = 1.5,
                           save_plot = TRUE,
                           ...){

  if(!CheckColumnExistence(data = data, list(x))){
    return()
  }

  if(nrow(data) > data_nrow_min){
    gplot <- ggplot(data = data) +
      geom_histogram(aes_string(x = x, "..density.."), binwidth = bin_width) +
      xlim(xlim_min, xlim_max) +
      ggtitle(plot_title) +
      theme_jetka(text_size = theme_text_size)
    if(save_plot){
      try({
        output_path <- normalizePath(output_path, "/")
        dir.create(path = output_path ,recursive = TRUE)
        ggsave(filename = paste(output_path, "/", filename, ".pdf", sep = ""),
               plot = gplot,
               width = plot_width,
               height = plot_height,
               useDingbats = FALSE)
        })
    }
    return(gplot)
  }
  return()

}


#### plot_histogram_list ####
plot_histogram_list <- function(data,
                                output_path,
                                filename = "boxplot",
                                grid_col,
                                grid_col_name = grid_col,
                                args_filename = list(),
                                x = "Intensity_IntegratedIntensity_DAPI",
                                data_nrow_min = 10,
                                ylab = "density",
                                xlab = x,
                                xlim_min = 0,
                                xlim_max = max(as.numeric(data[,x])),
                                bin_number = 50,
                                bin_width = (xlim_max - xlim_min)/bin_number,
                                plot_width = 24,
                                plot_height = 8,
                                plot_title = "",
                                theme_text_size = 12,
                                line_size = 1.5,
                                ...

){
print(x)
print(x %in% colnames(data))
  grid <- expand.grid(sapply(grid_col,
                             function(g){

                               return(sort(unique(data[,g])))}))
  plots.list <- list()


  filename.global <- paste(output_path,
                           filename,
                           sep = "/")


  for(i in 1:nrow(grid)){
    try({
      data.tmp <- data[as.logical(
        apply(
          sapply(1:length(grid_col),
                 function(j){
                   data[,grid_col[j]] == grid[i,j]}),
          1,
          prod)),]

      plot_title <- paste("cells = ",
                          data.tmp$cells[1],
                          paste(sapply(1:length(grid_col),
                                       function(j){
                                         paste(grid_col_name[j], "=", grid[i,j])}
                          ), collapse = " ")
      )

      plots.list[[i]] <-   plot_histogram(data.tmp,
                                          x = x,
                                          plot_width = plot_width,
                                          plot_height = plot_height,
                                          plot_title = plot_title,
                                          theme_text_size = theme_text_size,
                                          line_size = line_size,
                                          save_plot = FALSE

      )
    })
  }

  try({
    output_path <- normalizePath(output_path, "/")
    dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)
    try({dev.off()})
    pdf(file = paste(filename.global, ".pdf", sep = ""),
      useDingbats = FALSE,
      width = plot_width,
      height = plot_height)
    l <- lapply(plots.list, print)
    dev.off()
  })
}


#### plot_histogram_grid ####
plot_histogram_grid <- function(data,
                                output_path,
                                ...,
                                filename,
                                x = "Intensity_IntegratedIntensity_DAPI",
                                grid_x,
                                grid_y,
                                data_nrow_min = 10,
                                ylab = grid_y,
                                xlab = grid_x,
                                xlim_min = 0,
                                xlim_max = max(as.numeric(data[,x])),
                                bin_number = 50,
                                bin_width = (xlim_max - xlim_min)/bin_number,
                                plot_width = 64,
                                plot_height = 64,
                                plot_title = "",
                                theme_text_size = 48,
                                line_size = 1.5){

  data[,grid_x] <- factor(data[,grid_x], levels = sort(unique(data[,grid_x])))
  data[,grid_y] <- factor(data[,grid_y], levels = sort(unique(data[,grid_y])))
  if(nrow(data) > data_nrow_min){
    gplot <- ggplot(data = data) +
      geom_histogram(aes_string(x = x, "..density.."), binwidth = bin_width) +
      facet_grid(facets = paste(grid_x, "~", grid_y, sep =" " )) +
      xlim(xlim_min, xlim_max) +
      ggtitle(plot_title) +
      theme_jetka(text_size = theme_text_size)
    try({
      output_path <- normalizePath(output_path, "/")
      dir.create(path = output_path, recursive = TRUE, showWarnings = FALSE)
      ggsave(filename = paste(output_path, "/", filename, ".pdf", sep = ""),
           plot = gplot,
           width = plot_width,
           height = plot_height,
           useDingbats = FALSE,
           limitsize = FALSE)
    })
    return(gplot)
  }
  return()
}
