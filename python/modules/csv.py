#! /usr/bin/python
import os
import logging
#from modules.file_managment import get_dir_names

logger = logging.getLogger(__name__)
logger.info("Executing csv (merge) module.")

def merge(csv_name, subdir_list, input_path, output_path): 
    """csv_names = the list of filenames with given CP output data (for example: Nuclei.csv, Cytoplasm.csv)
    subdir_list = the list of subdir's names, each of subdir contains data of given well"""
    out_file= open((os.path.join(output_path, csv_name)), "a") #creating output file
    logger.info("Creating %s output (merged) file.", csv_name)
    # first file:
    num = 0
    position = subdir_list[0].split()
    position = position[1] # getting position (well id)
    logger.debug("Merging data from %s.", position)
    for line in open((os.path.join(input_path, subdir_list[0], csv_name))): 
        if num == 0: #adding first line from the first input file (to include the header)
            out_file.write(line.rstrip() + "," + "PositionName" + "\n")
            num = 1
        else:
            out_file.write(line.rstrip() + "," + position + "\n") #adding the rest of lines with proper position (well id)
    # rest files:
    for subdir in (subdir_list[1:]):
        position = subdir.split()
        position = position[1]
        logger.debug("Merging data from %s.", position)
        f = open((os.path.join(input_path, subdir, csv_name)), "r")
        # skip the header
        first_line = f.readline() # first line is header, it is called to put it out of set
        for line in f:
            out_file.write(line.rstrip() + "," + position + "\n") #adding the rest of lines with proper position (well id)
        f.close()
    out_file.close()
    logger.info("%s data successfully merged.", csv_name)

