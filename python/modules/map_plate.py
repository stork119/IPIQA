#! /usr/bin/python
import string

def writing_output_csv(input_path, output_path, output_data):
    out_file= open(output_path, "a")
    num = 0
    position = 0 
    for line in open(input_path):
        if num == 0: # GET THE POSTION: DO UZUPELNIENIA
            new_line = [line.rstrip()]
            data = line.rstrip().split(",")
            for i in range(len(data)):
                if data[i] == "PositionName":
                    position = i
            for j in output_data:
                new_line.append(j["column_title"])
            new_line = ",".join(new_line)
            out_file.write(new_line + "\n")
            num = 1
        else:
            new_line = [line.rstrip()]
            data = line.rstrip().split(",")
            key = data[position]           
            for i in output_data:
                new_line.append(i[key])
            new_line = ",".join(new_line)
            out_file.write(new_line + "\n")
    out_file.close()

    
def collecting_exp_settings(input_path, alphabet):
    column_title = ".".join(input_path.split("//")[-2:])
    output_dict = {"column_title":column_title}
    for line, alphabet in zip(open(input_path), alphabet):
        data = line.split("\t")
        for i in range(len(data)):
            well_number = alphabet + (str(i+1).zfill(2))
            output_dict[well_number] = data[i]
    return output_dict

def parsing_map_plate(input_path_list, let_number):
    alphabet_list = list(string.ascii_uppercase)
    alphabet_list = alphabet_list[:let_number]
    output_data = []
    for in_file in input_path_list:
        output_dict = collecting_exp_settings(in_file, alphabet_list)
        output_data.append(output_dict)
    return output_data
    
def making_path_list(main_path, file_list): # maybe this should be in file_managment?? gonna change method of path joining to more safe (not simple strings merge)
    path_list = []
    for filepath in file_list:
        path = main_path + filepath
        path_list.append(path)
    return path_list

def combine(path_csv, path_map_plate, path_output, csv_names, map_plate_files, let_number):

    f_map_plate = making_path_list(path_map_plate, map_plate_files)
    f_paths_csv = making_path_list(path_csv, csv_names)
    f_paths_output = making_path_list(path_output, csv_names)
    output_data = parsing_map_plate(f_map_plate, let_number)
    for i in range(len(f_paths_csv)):
        writing_output_csv(f_paths_csv[i], f_paths_output[i], output_data)

