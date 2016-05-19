#! /usr/bin/python
import os.path, csv
from time import sleep
import logging
import shutil # for function copy_data

logger = logging.getLogger(__name__)
logger.info("Executing file_managment module.")
"""
Checking out if the director and file exist ["C:/path/to/file"].
"""
def if_exist(path):
    if (os.path.exists(path)):
        logger.debug("%s path exists.", path)
        return True
    #logger.debug("%s path doesn't exist.", path)
    return False
"""
Operations on paths.
"""  
def path_unification(in_path):
    windows = True
    path = split_path_by(in_path)
    path = path_unification_from_list(path)
    if in_path.endswith("/") or in_path.endswith("\\"):
        if windows == True:
            path = path + "//"
    return path

def path_unification_from_list(path):
    windows = True #we may add more conditions in the future.
    if windows == True:
        path = "//".join(path)
    return path

def join_paths(*paths_list):
    final_path = []
    if len(paths_list) < 2:
        logger.error("Can't join less then 2 paths. Paths to join list: %s", paths_list)
        return 0
    for path in paths_list:
        splited_path = split_path_by(path)
        final_path = final_path + splited_path
    final_path = path_unification_from_list(final_path)
    return final_path

def get_relative_path(abs_path, file_path):
    windows = True
    abs_path = split_path_by(abs_path)
    file_path = split_path_by(file_path)
    rel_path = [x for x in file_path if x not in abs_path]
    rel_path = path_unification_from_list(rel_path)
    return rel_path
  
def split_path_by(path):
    possible_marks = ["\\\\","\\","//","/"]
    ele_list = [path]
    for mark in possible_marks:
        output = []
        for ele in ele_list:
            data = ele.split(mark)
            if len(data) > 1:
                for i in data:
                    output.append(i)    
            else:
                output.append(data[0])
        ele_list = output
    output = list(filter(None, ele_list))
    return output
"""
Getting all names/paths of files/directories located in a given directory.
"""
def get_dir_names(input_path):
    if not if_exist(input_path):
        logger.error("Error. Can't get subdirs names list for a given path: %s. Path doesn't exist", input_path)
        return
    subdir_list = []
    for subdir in os.listdir(input_path):
        if os.path.isdir(os.path.join(input_path, subdir)):
            subdir_list.append(subdir)
            logger.debug("Folder %s added to subdirectories' list of path %s.", subdir, input_path)
    return subdir_list

def get_file_names(input_path):
    if not if_exist(input_path):
        logger.error("Error. Can't get subfile names list for a given path: %s. Path doesn't exist", input_path)
        return
    subfile_list = []
    for subfile in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path, subfile)):
            subfile_list.append(subfile)
            logger.debug("File %s added to subfiles' list of path %s.", subfile, input_path)
    return subfile_list

def get_file_paths(input_path):
    if not if_exist(input_path):
        logger.error("Error. Can't get subfiles names list for a given path: %s.", input_path)
        return False
    subfile_paths = []
    names = get_file_names(input_path)
    for name in names:
        tmp = join_paths(input_path, name)
        subfile_paths.append(tmp)
        logger.debug("File's path %s added to subfiles' list of path %s.", tmp, input_path)
    return subfile_paths

def get_dir_paths(input_path):
    if not if_exist(input_path):
        logger.error("Error. Can't get subfiles names list for a given path: %s.", input_path)
        return False
    subdir_paths = []
    names = get_dir_names(input_path)
    for name in names:
        tmp = join_paths(input_path, name)
        subdir_paths.append(tmp)
        logger.debug("Directory's path %s added to subdirs' list of path %s.", tmp, input_path)
    return subdir_paths
"""
Functions for removing objects.
"""
def remove_file(path):
    try:
        os.remove(path)
        logging.info("File %s succesfully removed.", path)
    except Exception as e:
        logging.error(e)
        
def remove_folder(path):
    try:
        shutil.rmtree(path)
        logging.info("Folder %s succesfully removed.", path)
    except Exception as e:
        logging.error(e)

def remove_directory(path): # file or folder 
    if os.path.isfile(path):
        remove_file(path)
    elif os.path.isdir(path):
        remove_folder(path)
    else:
        logging.info("Object \"" + path + "\" not found.")        
"""
Functions for coping objects.
"""
def copy_directory_constantly(in_path, out_path, sleep_time):
    while True:
        if os.path.exists(in_path):
            copy_directory(in_path, out_path)
            return
        else:
            sleep(sleep_time)

def copy_directory(in_path, out_path):
    copied_dir_path = out_path
    #dir_name = extract_dir_name(in_path)
    #copied_dir_path = FM.join_paths(out_path, dir_name)
    if os.path.exists(copied_dir_path):
        logger.warning("Directory %s already exists. Removing old data.", copied_dir_path)
        remove_directory(copied_dir_path)
    os.makedirs(copied_dir_path)
    files_paths_list = get_file_paths(in_path)
    dirs_paths_list = get_dir_paths(in_path)
    for f in files_paths_list:
        copy_data(f, copied_dir_path)
    for f in dirs_path_list:
        copy_directory(f, copied_dir_path)
      
def copy_data(in_path, out_path):
    if if_exist(in_path):
        try:
            shutil.copy(in_path, out_path)
            return out_path
        except shutil.Error as e: #same path
            logging.error(e)
        except IOError as e:
            print('Error: %s' % e.strerror)
            logging.error(e)
    else:
        logging.error("Object \"" + in_path + "\" not found.")

def copy_data_constantly(in_path, out_path, sleep_time): #sleep_time is given in seconds and it's meant to be higher than 0.
    while True:
        if if_exist(in_path):
            try:
                shutil.copy(in_path, out_path)
                logging.info("Object succesfully copied to \"" + out_path + "\".")
                return out_path
            except shutil.Error as e: #same path
                logging.error(e)
            except IOError as e:
                print('Error: %s' % e.strerror)
                logging.error(e)
        else:
            logging.info("Object \"" + in_path + "\" have not been found yet. Searching will be continued.")
            sleep(sleep_time)
"""
Other functionalities.
"""
def dir_completeness(in_path, required_files, sleep_time):
    filelist = []
    while True:
        for f in os.listdir(in_path):
            if f not in filelist:
                filelist.append(f)
            if all(element in filelist for element in required_files):
                break
            else:
                sleep(sleep_time)

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

def extension_verification(filename, pattern):
    if filename.endswith(pattern):
        return True
    else:
        return False

def get_file_extension(filename):
    extension = os.path.splitext(filename)[1]
    return extension
    
def extract_dir_name(filename):
    path_list = split_path_by(filename)
    name = path_list[-1:]
    return name