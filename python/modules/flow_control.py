#! /usr/bin/python

import os, logging
import modules.file_managment as FM

logger = logging.getLogger("flow control")
logger.info("Executing flow_control module.")


def compare_args(arg1, arg2, comparison):
    if comparison == "equal" or comparison == "==":
        if arg1 == arg2:
            return True
    elif comparison == "different" or comparison == "!=":
        if arg1 != arg2:
            return True
    elif (comparison == "greater" or comparison == ">" or 
            comparison == "less" or comparison == "<"):
        if _greater_or_less(arg1, arg2, comparison):
            return True
    else:
        logger.error("Unknown for TASK_IF comparison type: %s", comparison)
    return False

def _greater_or_less(arg1, arg2, comparison):
    try:
        arg1 = int(arg1)
        arg2 = int(arg2)
    except:
        logger.error("Cannot compare non-numeric arguments: %s, %s", arg1, arg2)
        return False
    if comparison == "greater" or comparison == ">":
        if arg1 > arg2:
            return True
    else:
        if arg1 < arg2:
            return True
    return False

def create_elements_list(input_path, wells_params, used_value):   
    """
    Arguments:
    - input_path - path to directories
    - wells_params - list of lists of chosen wells parameters
    - used_value - value defying if given dir name reflects well tag or id
    Returns
    - verified_dirs- list of subdirs representing chosen active wells set
    """
    all_dir_list = FM.dir_get_names(input_path)
    verified_dirs = []
    for well in wells_params:
        try:
            if any(dir_name == well[("wellname_" + used_value)] for dir_name in all_dir_list):
                verified_dirs.append(well)
        except: 
            logger.error("Unexpected used_value: %s", used_value)
    return verified_dirs
