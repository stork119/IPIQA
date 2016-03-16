#! /usr/bin/python
import os.path
from time import sleep
import logging
import shutil # for function copy_data

"""
Temporary logfile's settings.
"""
logging.basicConfig(level=logging.DEBUG, 
		    filename="logfile_temp", 
		    format="%(asctime)-2s \t %(levelname)-4s \t %(message)s")


logging.info("Executing file_managment module.")
"""
Checking out if the director and file exist ["C:/path/to/file"].
"""
def if_exist(path):
    if (os.path.exists(path)):
        return True

"""
Functions for removing objects.
"""
def remove_file(path):
    try:
        os.remove(path)
        logging.info("Object \"" + path + "\" succesfully removed.")
    except Exception as e:
        logging.error(e)
        
def remove_folder(path):
    try:
        shutil.rmtree(path)
        logging.info("Object \"" + path + "\" succesfully removed.")
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
        logging.info("Object \"" + in_path + "\" not found.")


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
