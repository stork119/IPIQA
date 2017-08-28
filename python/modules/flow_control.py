#! /usr/bin/python

import os, logging
import modules.file_managment as FM

logger = logging.getLogger("IPIQA.flow_control")

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

def create_elements_list(input_path, wells_params, used_value, input_path_list = None):   
    """
    Arguments:
    - input_path - path to directories
    - wells_params - list of lists of chosen wells parameters
    - used_value - value defying if given dir name reflects well tag or id
    Returns
    - verified_dirs- list of subdirs representing chosen active wells set
    """
    try:
        if input_path_list is None:
            input_path_list = [input_path]
        all_dir_list = [{'dir_list': FM.dir_get_names(input_path), 'input_path':input_path} for input_path in input_path_list]
        verified_dirs = []
        for well in wells_params:
            well_found = False
            for path_dir_list in all_dir_list:
                if not well_found:
                    if any(dir_name == well[("wellname_" + used_value)] for dir_name in path_dir_list['dir_list']):
                        well['input_path'] = path_dir_list['input_path']
                        verified_dirs.append(well)
                        well_found = True
    except:
        logger.error("Unexpected error in create_elements_list")
    return verified_dirs
