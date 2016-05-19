#! /usr/bin/python
import string, os
import modules.file_managment as FM
import csv

def preparing_output_csv(input_data, output_path, mp_data, names):
    output_data = []
    num = 0
    position = 0 
    for line in input_data:
        if num == 0: 
            new_line = line
            for i in range(len(line)):
                if line[i] == "PositionName":
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

def getting_paths_mp(input_path):
    subfile_list = FM.get_file_paths(input_path)
    param_paths = []
    all_paths = []
    for root, dires, files in os.walk(input_path):
        for name in files:
            all_paths.append(FM.join_paths(root, name))
    for path in all_paths:
        if path not in subfile_list and path[-4:] == ".csv":
            param_paths.append(path)
    return param_paths
    
def making_path_list(main_path, file_list): # maybe this should be in file_managment?? gonna change method of path joining to more safe (not simple strings merge)
    path_list = []
    for filepath in file_list:
        path = main_path + filepath
        path_list.append(path)
    return path_list

def parsing_matrix(path, deltimer):
    active_wells = []
    data = FM.read_csv(path, deltimer)
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == "1":
                nums = [row, col]
                active_wells.append(nums)
    return active_wells

def parsing_map_plate(mp_path, paths_mp, deltimer):
    param_dict = {}
    active_path = FM.join_paths(mp_path, "args_active.csv")
    names_path = FM.join_paths(mp_path, "args_ind.csv")
    active_wells = parsing_matrix(active_path, deltimer)
    for well in active_wells:
        result = []
        name = collecting_exp_settings(names_path, well, deltimer = ",")
        for mp_file in paths_mp:
            param = collecting_exp_settings(mp_file, well, deltimer)
            result.append(param)
        param_dict[name] = ",".join(result)
    return param_dict
  
def collecting_exp_settings(mp_file, well, deltimer):
    row_nr, col_nr = well
    data = FM.read_csv(mp_file, deltimer)
    return (data[row_nr][col_nr])
    
def getting_column_titles(abs_path, paths):
    names = []
    for path in paths:
        rel_path = FM.get_relative_path(abs_path, path)
        name = (".".join(FM.split_path_by(rel_path)))[:-4]
        #ext_len = len(FM.get_file_extension(rel_path))
        #name = (".".join(FM.split_path_by(rel_path)))[:-ext_len]
        names.append(name)
    #names = ",".join(names)
    return names

def combine(path_csv, path_map_plate, path_output, csv_names, deltimer = "\t", csv_deltimer = ","):
    f_paths_map_plate = getting_paths_mp(path_map_plate)
    f_paths_output = making_path_list(path_output, csv_names)
    if isinstance(path_csv,str):
        f_paths_csv = making_path_list(path_csv, csv_names)
    mp_output = parsing_map_plate(path_map_plate, f_paths_map_plate, deltimer)
    names = getting_column_titles(path_map_plate, f_paths_map_plate)
    for i in range(len(f_paths_output)):
        if isinstance(path_csv,dict):
            in_data = paths_csv[csv_names[i]]  
        elif isinstance(path_csv,str):
            in_data = FM.read_csv(f_paths_csv[i], csv_deltimer)
        else:
            break #might be some error msg
        if FM.if_exist(f_paths_output[i]):
            FM.remove_directory(f_paths_output[i])
        out = preparing_output_csv(in_data, f_paths_output[i], mp_output, names)
        FM.write_csv(f_paths_output[i], deltimer, out)
        
