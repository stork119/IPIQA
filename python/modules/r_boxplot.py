#! /usr/bin/python
import rpy2.robjects as robjects
from rpy2.robjects.vectors import DataFrame
import file_managment as FM
#import modules.file_managment as FM

abs_path = "C://Users//Pathway//Documents//PathwayPackage//" #gonna get it from global_dict in the future 
script_name = "pp_boxplot.R" #same here
r_script_path = FM.path_join(abs_path, "R", script_name)
#probably whole part presented above is gonna be moved to Task and we will just pass the source_path
input_path = "E://AG//PathwayPackage//resources//output//2016-06-07//raw//map_plate//Nuclei.csv"
output_path = "C://Users//Pathway//Desktop//machlojki//plot.pdf"

r_source = robjects.r['source']
r_source(r_script_path)
r_makeplot = robjects.globalenv['pp.boxplot']

data = DataFrame.from_csvfile(input_path, sep = "\t")

r_makeplot(data, output_path, "compare.1.1", "Intensity_MeanIntensity_CHA", "PositionName", "group.1.1")

# data - data.frame
# filename - path to plot output file 
# x - "compare.1.1"
# y <- "Intensity_MeanIntensity_CHA"
# boxplot.group - "PositionName" or "ImageNumber"
# x_axis.group - "group.?.?", here group.1.1
