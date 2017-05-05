#! /usr/bin/python
import os, logging, csv
import modules.file_managment as FM

logger = logging.getLogger("CSV managment")
logger.info("Executing csv (merge) module.")

def merge_csv_files(csv_name, main_subdir_list, delimiter, column_name, output_path):
    subdir_list = filter_subdir_list(main_subdir_list, csv_name) #filtering directiories containing given csv file
    data = merge_subdir_csv(csv_name, subdir_list, delimiter, column_name)
    extension = FM.file_get_extension(csv_name)
    name = csv_name[:-(len(extension))]
    #Saving data
    out_path = FM.path_join(output_path, csv_name)
    if FM.path_check_existence(out_path):
        logger.warning("File %s already exists. Removing old data.", out_path)
        FM.dir_remove(out_path)
    write_csv(out_path, delimiter, data)

def merge_subdir_csv(csv_name, subdir_list, delimiter = ",", column_name = "well.name"): 
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
            tmp = [x for x in line.rstrip().split(delimiter)]
            tmp.append(column_name)
            output.append(tmp)
            num = 1
        else:
            tmp = [x for x in line.rstrip().split(delimiter)] #adding the rest of lines with proper position (well id)
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
            tmp = [x for x in line.rstrip().split(delimiter)] #adding the rest of lines with proper position (well id)
            tmp.append(position)
            output.append(tmp)
        f.close()
    logger.info("%s data successfully merged.", csv_name)
    return output

def simple_merge(csv_name, input_paths, delimiter, header = True):
    full_paths = [FM.path_join(path, csv_name) for path in input_paths]
    tmp = 0
    output = []
    for f in full_paths:
        try:
            data = read_csv(f, mark = delimiter)
        except:
            logger.error("Cannot read csv input file: %s. Unable to perform merge.", f)
            break
        if tmp == 0:
            tmp = 1
            output = data
        else:
            if header == True:
                output = output + data[1:]
            else:
                output = output + data
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

def write_csv(path, delimiter, data = None, key = ""):
    if isinstance(data,dict):
        data = data[key]
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, 'w') as f:
        for row in data:
            f.write(delimiter.join(row) + "\n")

def filter_subdir_list(main_subdir_list, csv_name):
    final_list = []
    for subdir in main_subdir_list:
        path = FM.path_join(subdir, csv_name)
        if FM.path_check_existence(path):
            final_list.append(subdir)
    return final_list
