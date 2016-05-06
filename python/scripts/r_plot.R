f <- function(data, x_col_name, y_col_name , path){
  library(ggplot2)

  g <- ggplot(data, aes_string( x = x_col_name, y = y_col_name)) + geom_point()
  ggsave(filename = path, plot = g)
}