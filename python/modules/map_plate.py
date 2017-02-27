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
        correctness = _verify_input_files(mp_file, delimiter, dimensions)
        if correctness == False:
            exit()
        else:
            _collect_exp_settings(input_path, mp_file, delimiter, mp_dict)

def _parse_base_params(input_path, delimiter, mp_dict):
    active_path = FM.path_join(input_path, "args_active.csv")
    id_path = FM.path_join(input_path, "args_ind.csv")
    name_path = FM.path_join(input_path, "args_names.csv")
    active = CSV_M.read_csv(active_path, delimiter)
    x = len(active)
    y = len(active[0])
    dimensions = [x,y]
    if not FM.path_check_existence(name_path):
        name_path = id_path
    else:
        if not _verify_input_files(name_path, delimiter, dimensions):
            exit()
    if not _verify_input_files(id_path, delimiter, dimensions):
        exit()
    name = CSV_M.read_csv(name_path, delimiter)
    mp_id = CSV_M.read_csv(id_path, delimiter)
    for row in range(len(active)):
        for col in range(len(active[row])):
            if int(active[row][col]) != 0:
                position = [row, col]
                key = name[row][col] #name_value
                id_value = mp_id[row][col]
                mp_dict[key] = {"position" : position, "name" : key, "id" : id_value}
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

def _verify_input_files(input_file, delimiter, dimensions = 0):
    if not FM.file_verify_extension(input_file, ".csv"):
        logger.error("Wrong input format: %s", input_file)
        return False
    if dimensions != 0:
        data = CSV_M.read_csv(input_file, delimiter)
        x = len(data)
        y = len(data[0])
        if dimensions != [x,y]:
            logger.error("Wrong input file: %s.", input_file)
            return False
    return True

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

