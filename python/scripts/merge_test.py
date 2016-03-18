#! /usr/bin/python
import logging, os, sys
#import logging.config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import modules.logs_configuration as LC
from modules import file_managment as FM
from modules import csv

def main():
    
    LC.configure()
    logger = logging.getLogger(__name__)

    input_path = "C://Users//Agnieszka//Documents//Out"
    output_path = "C://Users//Agnieszka//Documents//Out"
    csv_names = ['Cells.csv', 'Cytoplasm.csv', 'ExpandedNucleiLess.csv', 'ExpandedNucleiMore.csv', 'Image.csv', 'Nuclei.csv', 'RingCytoplasm.csv', 'ShrinkedNuclei.csv']
    #'Experiment.csv' was not icluded in 'csv_names' list of files, because of different structure
    subdir_list = FM.get_dir_names(input_path) # getting the subdirectories' list (1 subdir = 1 well data) of the given directory 
    for csv_name in csv_names: # merging data file (type) by file
        csv.merge(csv_name, subdir_list, input_path, output_path)
       
    

if __name__ == "__main__":
    main()