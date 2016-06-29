#! /usr/bin/python
import os, logging, csv
import modules.file_managment as FM

logger = logging.getLogger(__name__)
logger.info("Executing csv (merge) module.")

def merge(csv_name, subdir_list, deltimer = ","): 
    """csv_names = the list of filenames with given CP output data (for example: Nuclei.csv,Cytoplasm.csv)
    subdir_list = the list of subdir's paths, each of subdir contains data of given well"""
    output= []
    logger.info("Creating %s output (merged) data.", csv_name)
    # first file:
    num = 0
    position = subdir_list[0].split()
    position = position[1] # getting position (well id)
    logger.debug("Merging data from %s.", position)
    for line in open(FM.path_join(subdir_list[0], csv_name), "r"):
        if num == 0: #adding first line from the first input file (to include the header)
            tmp = [x for x in line.rstrip().split(deltimer)]
            tmp.append("well.name")
            output.append(tmp)
            num = 1
        else:
            tmp = [x for x in line.rstrip().split(deltimer)] #adding the rest of lines with proper position (well id)
            tmp.append(position)
            output.append(tmp)
    # rest of files:
    for subdir in (subdir_list[1:]):
        position = subdir.split()
        position = position[1]
        logger.debug("Merging data from %s.", position)
        f = open(FM.path_join(subdir, csv_name), "r")
        # skip the header
        first_line = f.readline() # first line is header, it is called to put it out of set
        for line in f:
            tmp = [x for x in line.rstrip().split(deltimer)] #adding the rest of lines with proper position (well id)
            tmp.append(position)
            output.append(tmp)
        f.close()
    logger.info("%s data successfully merged.", csv_name)
    return output

def read_csv(path, mark, dict_local = {}, key_name = ""):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        data = list(list(line) for line in csv.reader(f, delimiter=mark))
    if len(dict_local) == 0: #no dictionary was passed
        return data
    else:
        dict_local[key_name] = data
        return dict_local

def write_csv(path, deltimer, data = None, key = ""):
    if isinstance(data,dict):
        data = data[key]
    with open(path, 'w') as f:
        for row in data:
            f.write(deltimer.join(row) + "\n")

def filter_subdir_list(main_subdir_list, csv_name):
    final_list = []
    for subdir in main_subdir_list:
        path = FM.path_join(subdir, csv_name)
        if FM.path_check_existence(path):
            final_list.append(subdir)
    return final_list
