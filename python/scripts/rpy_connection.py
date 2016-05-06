#! /usr/bin/python
import csv
import rpy2.robjects as robjects
from rpy2.robjects.vectors import DataFrame

from rpy2.robjects.packages import importr
grdevices = importr('grDevices')

def parsing_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
    return reader

input_path = "C://Users//Agnieszka//Desktop//input//example_data.csv"
output_path = "C://Users//Agnieszka//Desktop//output//proba_plot.png"
#data = parsing_csv(input_path)
data = DataFrame.from_csvfile(input_path, sep = ",")
#static from_csvfile(path, header=True, sep=', ', quote='"', dec='.', row_names=rpy2.rinterface.MissingArg, col_names=rpy2.rinterface.MissingArg, fill=True, comment_char='', as_is=False)


r_source = robjects.r['source']
r_source('r_plot.R')
r_getname = robjects.globalenv['f']
#grdevices.png(file=output_path, width=1300, height=1000)
r_getname(data, "position_name", "position_name", output_path)
