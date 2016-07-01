#! /usr/bin/python
import string, os
import modules.file_managment as FM
import modules.csv_managment as CSV_M
import csv

def _preparing_output_csv(input_data, output_path, mp_data, names):
    output_data = []
    num = 0
    position = 0 
    for line in input_data:
        if num == 0: 
            new_line = line
            for i in range(len(line)):
                if line[i] == "well.name":
                    position = i
            for j in names:
                new_line.append(j)
            output_data.append(new_line)
            num = 1
        else:
            new_line = line
            key = line[position]           
            new_line.append(mp_data[key])
            output_data.append(new_line)
    return output_data

def _getting_paths_mp(input_path):
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
    
def _making_path_list(main_path, file_list): # maybe this should be in file_managment?? gonna change method of path joining to more safe (not simple strings merge)
    path_list = []
    for filepath in file_list:
        path = main_path + filepath
        path_list.append(path)
    return path_list

def _parsing_matrix(path, deltimer, exp_part):
    active_wells = []
    data = CSV_M.read_csv(path, deltimer)
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == exp_part:
                nums = [row, col]
                active_wells.append(nums)
    return active_wells

def _parsing_map_plate(mp_path, paths_mp, deltimer, exp_part, exp_name):
    param_dict = {}
    active_path = FM.path_join(mp_path, "args_active.csv")
    names_path = FM.path_join(mp_path, "args_ind.csv")
    positions_path = FM.path_join(mp_path, "args_names.csv")
    if FM.path_check_existence(positions_path):
        tmp = True
    active_wells = _parsing_matrix(active_path, deltimer, exp_part)
    for well in active_wells:
        name = _collecting_exp_settings(names_path, well, deltimer)
        result = []
        if tmp == True:
            result.append(_collecting_exp_settings(positions_path, well, deltimer))
        else:
            result.append(name)
        result.append(exp_name)
        for mp_file in paths_mp:
            param = _collecting_exp_settings(mp_file, well, deltimer)
            result.append(param)
        param_dict[name] = deltimer.join(result)
    return param_dict
  
def _collecting_exp_settings(mp_file, well, deltimer):
    row_nr, col_nr = well
    data = CSV_M.read_csv(mp_file, deltimer)
    return (data[row_nr][col_nr])
    
def _getting_column_titles(abs_path, paths):
    names = []
    names.append("position.name")
    names.append("exp.id")
    for path in paths:
        rel_path = FM.path_get_relative(abs_path, path)
        fullname = ".".join(FM._path_split(rel_path))
        extension_length = len(FM.file_get_extension(fullname))  #extracting proper column name from rel_path i.e. compare.1.1 from compare/1.1.csv
        name = fullname[:-extension_length]
        names.append(name)
    #names = ",".join(names)
    return names

def _getting_exp_name(path_csv):
    #E:\AG\PathwayPackage\resources\output\2016-01-23-EG13\raw\data_quantify\2016-01-19-EG12-02\2016-01-19_003\costam.csv
    name = FM._path_split(path_csv)
    name = name[-3:][0] #awfull hardcoding, will be replaced when ID will showup in metadata
    return name

def getting_exp_part(path):
    name = _getting_exp_name(path)
    exp_id = name.split("-")[4]
    return exp_id

def combine(path_csv, path_map_plate, path_output, csv_names, deltimer = "\t", csv_deltimer = ",", exp_part = "1"):
    exp_name = _getting_exp_name(path_csv)
    f_paths_map_plate = _getting_paths_mp(path_map_plate)
    f_paths_map_plate = sorted(f_paths_map_plate, key = str)
    f_paths_output = _making_path_list(path_output, csv_names)
    if isinstance(path_csv,str):
        f_paths_csv = _making_path_list(path_csv, csv_names)
    mp_output = _parsing_map_plate(path_map_plate, f_paths_map_plate, deltimer, exp_part, exp_name) # exp_part
    names = _getting_column_titles(path_map_plate, f_paths_map_plate)
    for i in range(len(f_paths_output)):
        if isinstance(path_csv,dict):
            in_data = paths_csv[csv_names[i]]  
        elif isinstance(path_csv,str):
            in_data = CSV_M.read_csv(f_paths_csv[i], csv_deltimer)
        else:
            break #might be some error msg
        if FM.path_check_existence(f_paths_output[i]):
            FM.dir_remove(f_paths_output[i])
        out = _preparing_output_csv(in_data, f_paths_output[i], mp_output, names)
        CSV_M.write_csv(f_paths_output[i], deltimer, out)
        
