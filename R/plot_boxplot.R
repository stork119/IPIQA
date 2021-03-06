### ###
###
### plot_boxplot_group
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
#wd.tmp <- "Y:/IPIQA/PP-21/R/" ### Rstudio 
wd.tmp <- dirname(sys.frame(1)$ofile) ### script
source(paste(wd.tmp, "theme_jetka.R", sep = "/"))
source(paste(wd.tmp, "data_library.R", sep = "/"))

#### MAIN ####
plot_boxplot_group <- function(data,
                               ...,
                               output_path,
                               filename,
                               x = "time",
                               y = "ShrinkedNuclei.CHA.Intensity",
                               boxplot_group = x,
                               facet_grid_group_y = "",
                               facet_grid_group_x = "",
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
                               ylim_max_const = TRUE,
                               x_factor = TRUE){
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
  x_factor  <- as.integer(x_factor)
  
  if(!CheckColumnExistence(data = data, list(x,y,boxplot_group,facet_grid_group_y))){
    return()
  }
  
  if(normalize_data){
    data[,y] <- normalize_factor*data[,y]
  }
  if(!ylim_max_const){
    ylim_max <- 1.2*max(data[,y])
  }
  if(x_factor){
    data[,x] <- factor(data[,x])
  }
  
#  data$bg <- factor(sapply(1:nrow(data),function(i){paste(as.character(data[i,boxplot_group]), sep = " ", collapse = " ")}))
  if(facet_grid_group_x != "" & !CheckColumnExistence(data = data, list(facet_grid_group_x))){
    facet_grid_group_x <- ""
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
    facet_grid(paste(facet_grid_group_x, "~", facet_grid_group_y, sep = " "), scale ="free", space = "free") +
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
  return(gplot)
}
