#! /usr/bin/python
import os.path
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
Getting all subdirs names of a given directory.
"""
def get_dir_names(input_path):
    if not if_exist(input_path):
        logger.error("Error. Can't get subdirs names list for a given path: %s.", input_path)
        return False
   # subdir_path = []
    subdir_names = []
    for path, subdir, files in os.walk(input_path):
        for name in subdir:
       #     subdir_path.append(os.path.join(path, name)) # get list of path to each subdir
            subdir_names.append(str(name))
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
