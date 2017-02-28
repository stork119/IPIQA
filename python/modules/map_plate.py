#! /usr/bin/python
import string, os, logging
import modules.file_managment as FM
import modules.csv_managment as CSV_M
import csv

logger = logging.getLogger("map plate")
logger.info("Executing map_plate module.")

def parse_mp(input_path, delimiter):
    mp_dict = {}
    dim =_parse_base_params(input_path, delimiter, mp_dict)
    _parse_params(input_path, delimiter, dim, mp_dict)
    return mp_dict

def _parse_params(input_path, delimiter, dimensions, mp_dict):
    param_paths =_get_param_paths(input_path)
    param_paths = sorted(param_paths, key = str)
    logger.debug("Map_plate params input paths: %s.", param_paths)
    for mp_file in param_paths:
        correctness = CSV_M.verify_input_files(mp_file, delimiter, dimensions)
        if correctness == False:
            logger.error("Fatal error occured while trying to read mapplate.")
            exit()
        else:
            _collect_exp_settings(input_path, mp_file, delimiter, mp_dict)

def _parse_base_params(input_path, delimiter, mp_dict):
    active_path = FM.path_join(input_path, "args_active.csv")
    # >>temporary change<<
    #id_path = FM.path_join(input_path, "args_ind.csv") 
    #name_path = FM.path_join(input_path, "args_names.csv")
    name_path = FM.path_join(input_path, "args_ind.csv")
    id_path = FM.path_join(input_path, "args_names.csv")
    # >>temporary change<<
    if not FM.path_check_existence(active_path):
        logger.error("Fatal error occured while trying to read mapplate. Cannot parse map_plate active, file doesn't exist: %s", active_path)
        exit()
    active = CSV_M.read_csv(active_path, delimiter)
    x = len(active)
    y = len(active[0])
    dimensions = [x,y]
    if not FM.path_check_existence(id_path):
        logger.info("Map_plate names would be used also as ids due to original id file doesn't exist: %s", id_path)
        id_path = name_path
    else:
        if not CSV_M.verify_input_files(id_path, delimiter, dimensions):
            logger.error("Fatal error occured while trying to read mapplate.")
            exit()
    if not FM.path_check_existence(name_path):
        logger.error("Fatal error occured while trying to read mapplate. Cannot parse map_plate names, file doesn't exist: %s", name_path)
        exit()
    if not CSV_M.verify_input_files(name_path, delimiter, dimensions):
        logger.error("Fatal error occured while trying to read mapplate.")
        exit()
    name = CSV_M.read_csv(name_path, delimiter)
    mp_id = CSV_M.read_csv(id_path, delimiter)
    for row in range(len(active)):
        for col in range(len(active[row])):
            exp_part = active[row][col]
            if exp_part != "0":
                position = [row, col]
                key = mp_id[row][col] #id_value
                name_value = name[row][col]
                mp_dict[key] = {"position" : position, "name" : name_value, "id" : key, "exp_part" : exp_part}
    return dimensions

def _get_param_paths(input_path):
    subfile_list = FM.file_get_paths(input_path)
    param_paths = []
    all_paths = []
    for root, dires, files in os.walk(input_path):
        for name in files:
            all_paths.append(FM.path_join(root, name))
    for path in all_paths:
        if path not in subfile_list and path[-4:] == ".csv":
            param_paths.append(path)
    return param_paths

def _collect_exp_settings(abs_path, mp_file, delimiter, mp_dict):
    rel_path = FM.path_get_relative(abs_path, mp_file)
    fullname = ".".join(FM._path_split(rel_path))
    extension_length = len(FM.file_get_extension(fullname))  #extracting proper column name from rel_path i.e. compare.1.1 from compare/1.1.csv
    name = fullname[:-extension_length]
    data = CSV_M.read_csv(mp_file, delimiter)
    for well in mp_dict:
        position = mp_dict[well]["position"]
        value = (data[position[0]][position[1]])
        mp_dict[well][name] = value

def get_param_value(mp_dict, well_name, param): # get values for a given well and parameter
    value = mp_dict[well_name][param]
    return value

def get_param_all_values(mp_dict, param): # get all values for a given param from map_plate dictionary
    values = []
    for well in mp_dict:
        values.append(mp_dict[well][param])
    return values

def get_param_unique_values(mp_dict, param): # get all unique values for a given param from map_plate dictionary
    values = get_param_all_values(mp_dict, param)
    unique = list(set(values))
    return unique

def get_all_params_names(mp_dict): # get all key names from map_plate dictionary
    names = []
    key_0 = list(mp_dict.keys())[0]
    names = list(mp_dict[key_0].keys()) # if we assume that number of information between wells is constant
    """params_count = len(mp_dict[key_0])
    for well in mp_dict: # if we assume that number of information about wells may somehow differ
        tmp= len(mp_dict[well])
        if params_count != tmp:
            logger.warning("Some wells are not described by the same number of information: %s, %s", key_0, well)
            if tmp > params_count:
                names = []
                params_count = tmp
                for param in mp_dict[well]:
                    names.append(param)"""
    return names

def get_well_params(mp_dict, well): # get all parameters values for a given well
    values = []
    for param in mp_dict[well]:
        values.append(mp_dict[well][param])
    return values
