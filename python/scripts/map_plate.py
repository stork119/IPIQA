#! /usr/bin/python
import string
#import map_plate

"""class MAP_PLATE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)
    def execute_specify(self, dict_local):
        input_path = dict_local["input_path"]
        output_flist = dict_local["csv_names_list"]
        map_plate.combine(input_path, output_flist)"""

def writing_output_csv(input_path, output_path, output_data):
    out_file= open(output_path, "a")
    num = 0
    position = 0 
    for line in open(input_path):
        if num == 0: # GET THE POSTION: DO UZUPELNIENIA
            new_line = [line]
            data = line.split(",")
            for i in range(len(data)):
                if data[i] == "PositionName":
                    position = i
            for i in output_data:
                new_line.append(output_data["column_title"])
            ",".join(new_line)
            out_file.write(new_line)
            num = 1
        else:
            new_line = [line]
            data = line.split(","):
            key = data[position]            
            # the place to check out the key (position name)
            for i in output_data:
                new_line.append(output_data[key])
            ",".join(new_line)
            out_file.write(new_line)
    out_file.close()

    
def collecting_exp_settings(input_path, alphabet):
    column_title = ".".join(input_path.split("//")[-2:])
    output_dict = {"column_title":column_title}
    for line, alphabet in zip(open(input_path), alphabet):
        data = line.split("\t")
        for i in range(data):
            well_number = alphabet + (str(i+1).zfill(2))
            output_dict[well_number] = data[i]
    return output_dict

def parsing_map_plate(input_path_list):
    alphabet_list = list(string.ascii_uppercase)
    let_number = 8 # int(sth from input_settings?)
    alphabet_list = alphabet_list[:let_number]
    output_data = []
    for in_file in input_path_list:
        output_dict = collecting_exp_settings(in_file, alphabet)
        output_data.append(output_dict)
    return output_data
    
def making_path_list(main_path, file_list): # maybe this should be in file_managment?? gonna change method of path joining to more safe (not simple strings merge)
    path_list = []
    for filepath in file_list:
        path = main_path + filepath
        path_list.append(path)
    return path_list

def run_map_plate(path_csv, path_map_plate, path_output, csv_names, map_plate_files):
    f_map_plate = making_path_list(path_map_plate, map_plate_files)
    f_paths_csv = making_path_list(path_csv, csv_names)
    f_paths_output = making_path_list(path_output, csv_names)
    output_data = parsing_map_plate(input_path_list)        

path_map_plate = ""
path_output = 

map_plate_files_list = [] 

f_paths_csv = []
f_paths_map_plate = []