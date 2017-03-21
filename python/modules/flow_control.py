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
    - wells_params - list of base parameters of chosen wells set
    - used_value - value defying if given dir name reflects well tag or id
    Returns
    - verified_dirst- list of dirs which parameters are present 
                        in wells_params list
    """
    all_dir_list = FM.dir_get_names(input_path)
    verified_dirs = []
    for well in wells_params:
        if used_value == "tag":
            if any(dir_name == well["wellname_tag"] for dir_name in all_dir_list):
                verified_dirs.append(well)
        elif used_value == "id":
            if any(dir_name == well["wellname_id"] for dir_name in all_dir_list):
                verified_dirs.append(well)
        else:
            logger.error("Unexpected used_value: %s", used_value)
    return verified_dirs

def get_active_wells(mp_dict, exp_part):
    """
    Returns list of active wells from mp_dict for given experiment part.
    """
    wells = mp_dict.keys()
    active_wells = []
    for well in wells:
        if mp_dict[well]["exp_part"] == exp_part:
            active_wells.append(well)
    return active_wells

def get_wells_base_params(mp_dict, wells, prefix, sufix, exp_part):
    """
    Gets wells base params from mp_dict.
    Base params:
    - mp_id
    - mp_tag
    - exp_part
    Adds prefixes and sufixes to mp_id and mp_tag to get:
    - wellname_id
    - wellname_tag
    """
    params = []
    for well in wells:
        wellname_id = prefix + mp_dict[well]["id"] + sufix
        wellname_tag = prefix + mp_dict[well]["name"] + sufix
        params.append({"wellname_id" : wellname_id, "wellname_tag" : wellname_tag, "exp_part" : exp_part, "mp_key" : mp_dict[well]["id"]})
    return params
