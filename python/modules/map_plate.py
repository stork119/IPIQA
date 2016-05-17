#! /usr/bin/python
import string, os
import modules.file_managment as FM
import csv

def writing_output_csv(input_path, output_path, output_data, names):
    out_file= open(output_path, "a")
    num = 0
    position = 0 
    for line in open(input_path):
        if num == 0: 
            new_line = [line.rstrip()]
            data = line.rstrip().split(",")
            for i in range(len(data)):
                if data[i] == "PositionName":
                    position = i
            for j in names:
                new_line.append(j)
            new_line = ",".join(new_line)
            out_file.write(new_line + "\n")
            num = 1
        else:
            new_line = [line.rstrip()]
            data = line.rstrip().split(",")
            key = data[position]           
            new_line.append(output_data[key])
            new_line = ",".join(new_line)
            out_file.write(new_line + "\n")
    out_file.close()

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
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter)
        num_row = 0
        for row in reader:
            num_column = 0
            for column in row:
                if column == "1":
                    nums = [num_row, num_column]
                    active_wells.append(nums)
                num_column = num_column + 1
            num_row = num_row + 1
    return active_wells

def parsing_map_plate(mp_path, paths_mp, deltimer):
    param_dict = {}
    active_path = FM.join_paths(mp_path, "args_active.csv")
    names_path = FM.join_paths(mp_path, "args_ind.csv")
    active_wells = parsing_matrix(active_path, deltimer)
    for well in active_wells:
        result = []
        name = collecting_exp_settings(names_path, well, deltimer)
        for mp_file in paths_mp:
            param = collecting_exp_settings(mp_file, well, deltimer)
            result.append(param)
        param_dict[name] = ",".join(result)
    return param_dict
  
def collecting_exp_settings(mp_file, well, mark):
    row_nr, col_nr = well
    data = FM.read_csv(mp_file, mark)
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

def combine(path_csv, path_map_plate, path_output, csv_names, deltimer = "\t"):
    f_paths_map_plate = getting_paths_mp(path_map_plate)
    f_paths_output = making_path_list(path_output, csv_names)
    output = parsing_map_plate(path_map_plate, f_paths_map_plate, deltimer)
    names = getting_column_titles(path_map_plate, f_paths_map_plate)
    f_paths_csv = making_path_list(path_csv, csv_names)
    for i in range(len(f_paths_csv)):
        writing_output_csv(f_paths_csv[i], f_paths_output[i], output, names)

