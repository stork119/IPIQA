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
def path_check_existence(path):
    if (os.path.exists(path)):
        logger.debug("%s path exists.", path)
        return True
    logger.debug("%s path doesn't exist.", path)
    return False
"""
Operations on paths.
"""
def _path_check_end_slash(path):
    if path.endswith("/") or path.endswith("\\"):
        return True
    else:
        return False

def path_unify(in_path): # Normalize the path for your system, at the moment feature is available only for Windows
    windows = True
    path = _path_split(in_path)
    end_slash = _path_check_end_slash(in_path)
    path = _unification_by_list(path, end_slash)
    logger.debug("Path unification completed. Previous path: %s, actual path: %s", in_path, path)
    return path

def path_join(*paths_list):
    final_path = []
    if len(paths_list) < 2:
        logger.error("Can't join less then 2 paths. Paths to join list: %s", paths_list)
        return 0
    for path in paths_list:
        splited_path = _path_split(path)
        final_path = final_path + splited_path
    # checking out if the last partial path has got slash on its end, if so the final (joint) path will also be finished by slash
    paths_num = len(paths_list)
    end_slash = _path_check_end_slash(paths_list[(paths_num - 1)])
    final_path = _unification_by_list(final_path, end_slash)
    logger.debug("Paths joining completed. List of paths to join: %s, final path: %s", paths_list, final_path)
    return final_path

def path_get_relative(abs_path, destination_path):
    windows = True
    abs_path = _path_split(abs_path)
    dir_path = _path_split(destination_path)
    rel_path = [x for x in dir_path if x not in abs_path]
    end_slash = _path_check_end_slash(destination_path)
    rel_path = _unification_by_list(rel_path, end_slash)
    logger.debug("Creating relative path completed. Absolute path: %s, destination path: %s, relative path:", abs_path, destination_path, rel_path)
    return rel_path

def _unification_by_list(path, end_slash = False): #Join list of path pieces 
    windows = True #we may add more conditions in the future.
    if windows == True:
        path = "//".join(path)
    if end_slash == True:
        if windows == True:
            path = path + "//"
    return path

def _path_split(path):
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
def file_get_names(input_path):
    if not path_check_existence(input_path):
        logger.error("Error. Can't get subfile names list for a given path: %s. Path doesn't exist", input_path)
        return
    subfile_list = []
    for subfile in os.listdir(input_path):
        if os.path.isfile(path_join(input_path, subfile)):
            subfile_list.append(subfile)
            logger.debug("File %s added to subfiles' list of path %s.", subfile, input_path)
    return subfile_list

def file_get_paths(input_path):
    if not path_check_existence(input_path):
        logger.error("Error. Can't get subfiles names list for a given path: %s.", input_path)
        return False
    subfile_paths = []
    names = file_get_names(input_path)
    for name in names:
        tmp = path_join(input_path, name)
        subfile_paths.append(tmp)
        logger.debug("File's path %s added to subfiles' list of path %s.", tmp, input_path)
    return subfile_paths

def dir_get_names(input_path):
    if not path_check_existence(input_path):
        logger.error("Error. Can't get subdirs names list for a given path: %s. Path doesn't exist", input_path)
        return
    subdir_list = []
    for subdir in os.listdir(input_path):
        if os.path.isdir(path_join(input_path, subdir)):
            subdir_list.append(subdir)
            logger.debug("Folder %s added to subdirectories' list of path %s.", subdir, input_path)
    return subdir_list

def dir_get_paths(input_path):
    if not path_check_existence(input_path):
        logger.error("Error. Can't get subfiles names list for a given path: %s.", input_path)
        return False
    subdir_paths = []
    names = dir_get_names(input_path)
    for name in names:
        tmp = path_join(input_path, name)
        subdir_paths.append(tmp)
        logger.debug("Directory's path %s added to subdirs' list of path %s.", tmp, input_path)
    return subdir_paths
"""
Functions for removing objects.
"""
def dir_remove(path): # file or directory
    if os.path.isfile(path):
        _file_remove(path)
    elif os.path.isdir(path):
        _folder_remove(path)
    else:
        logging.info("Unable to remove %s. Object not found.", path)   

def _file_remove(path):
    try:
        os.remove(path)
        logging.info("File %s succesfully removed.", path)
    except Exception as e:
        logging.error(e)
        
def _folder_remove(path):
    try:
        shutil.rmtree(path)
        logging.info("Folder %s succesfully removed.", path)
    except Exception as e:
        logging.error(e)   
"""
Functions for coping objects.
"""
def dir_copy(in_path, out_path):
    copied_dir_path = out_path
    if path_check_existence(copied_dir_path):
        logger.warning("Directory %s already exists. Removing old data.", copied_dir_path)
        dir_remove(copied_dir_path)
    os.makedirs(copied_dir_path)
    files_paths_list = file_get_paths(in_path)
    dirs_paths_list = dir_get_paths(in_path)
    for f in files_paths_list:
        file_copy(f, copied_dir_path)
    for f in dirs_paths_list:
        dir_copy(f, copied_dir_path)
      
def file_copy(in_path, out_path):
    if path_check_existence(in_path):
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

def file_copy_constantly(in_path, out_path, sleep_time): #sleep_time is given in seconds and it's meant to be higher than 0.
    while True:
        if path_check_existence(in_path):
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

def dir_copy_constantly(in_path, out_path, sleep_time):
    while True:
        if path_check_existence(in_path):
            dir_copy(in_path, out_path)
            return
        else:
            sleep(sleep_time)

"""
Other functionalities.
"""
def dir_check_completeness(in_path, required_files, sleep_time): # checking out if the given list of files exist in given directory (path)
    filelist = []
    while True:
        for f in os.listdir(in_path):
            if f not in filelist:
                filelist.append(f)
            if all(element in filelist for element in required_files):
                break
            else:
                sleep(sleep_time)

def file_verify_extension(filename, extension): #checking out if the given file have got given extension
    if filename.endswith(extension):
        return True
    else:
        logger.debug("File %s doesn't have got extension %s..", path, extension)
        return False

def file_get_extension(filename): #extracting extension from file i.e. ".py" from "foo.py"
    extension = os.path.splitext(filename)[1]
    return extension
    
def path_extract_name(path): #extract file/dir name from path i.e. "foo.txt" from "path/to/foo.txt"
    path_list = _path_split(path)
    tmp = len(path_list)
    name = path_list[(tmp - 1)]
    return name
