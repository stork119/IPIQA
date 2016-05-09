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
    logger.error("%s path doesn't exist.", path)
    return False
"""
Operations on paths.
"""  
def path_unification(path):
    windows = True #we may add more conditions in the future.
    if windows == True:
        path = path.replace("\\","//")
    return path

def join_paths(*paths_list):
    windows = True
    possible_marks = ["\\\\","\\","//","/"]
    if len(paths_list) < 2:
        logger.error("Can't join less then 2 paths. Paths to join list: %s", paths_list)
        return 0
    for mark in possible_marks:
        paths_list = split_list_by(paths_list, mark)
    if windows == True:
        final_path = "//".join(paths_list)
    return final_path

def split_list_by(ele_list, mark):
    output = []
    for ele in ele_list:
        data = ele.split(mark)
        if len(data) > 1:
            for i in data:
                output.append(i)    
        else:
            output.append(data[0])
    return output
"""
Getting all subdirs names/subfile paths of a given directory.
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
    
def get_filepaths(input_path):
    if not if_exist(input_path):
        print("Error. Can't get subfiles names list for a given path: %s.", input_path)
        return False
   # subdir_path = []
    subfile_names = []
    for path, subdir, files in os.walk(input_path):
        for name in files:
       #     subdir_path.append(os.path.join(path, name)) # get list of path to each subdir
            subfile_names.append(path + "//" + name)
    return subfile_names
    
def get_dirpaths(input_path): #temporary duplicated code !!!
    if not if_exist(input_path):
        print("Error. Can't get subfiles names list for a given path: %s.", input_path)
        return False
   # subdir_path = []
    subdir_names = []
    for path, subdirs, files in os.walk(input_path):
        for name in subdirs:
       #     subdir_path.append(os.path.join(path, name)) # get list of path to each subdir
            subdir_names.append(path + "//" + name)
    return subdir_names
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
    dir_name = (in_path.split("/"))[-1]
    copied_dir_path = out_path + dir_name
    if os.path.exists(copied_dir_path):
        logger.warning("Directory %s already exists. Removing old data.", copied_dir_path)
        remove_directory(copied_dir_path)
    os.makedirs(copied_dir_path)
    files_paths_list = get_filepaths(in_path)
    dirs_paths_list = get_dirpaths(in_path)
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

def write_csv(path, mark, data = None, key = ""):
    if isinstance(data,dict):
        data = data[key]
    with open(path, 'w') as f:
        for row in data:
            f.write(mark.join(row) + "\n")
  
a = {"c":'1', 'b':'2'}
try:
    job_done= a["a"]
    if job_done == "1":
        print("yes")
except:
    pass
print("im done")