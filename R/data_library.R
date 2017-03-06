### ###
### data_library
### ###


CheckColumnExistence <- function(data, columns.list = list()){
  return(sum(!(unlist(columns.list) %in% colnames(data))) == 0)
}