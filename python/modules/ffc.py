#! /usr/bin/python
import modules.r_connection as R_connection
import modules.file_managment as FM
import os

def prepare_script_path():
    path = os.path.abspath('..')
    path = FM.path_join(path, "R/ffc_module/ffc_module.R")
    return path

def create_camcor(dict_local, parameters_by_value, parameters_by_name):
    r_script_path = prepare_script_path()
    function_name = "fun_camcor_create"
    param_dict = R_connection.prepare_param_dict(dict_local, parameters_by_value, parameters_by_name, [])
    output_dict = R_connection.execute_r_script(param_dict, r_script_path, function_name)
    return output_dict

def read_camcor(dict_local, parameters_by_value, parameters_by_name):
    r_script_path = prepare_script_path()
    function_name = "fun_camcor_read"
    param_dict = R_connection.prepare_param_dict(dict_local, parameters_by_value, parameters_by_name, [])
    output_dict = R_connection.execute_r_script(param_dict, r_script_path, function_name)
    return output_dict

def apply_camcor(dict_local, parameters_by_value, parameters_by_name):
    r_script_path = prepare_script_path()
    function_name = "fun_camcor_apply"
    param_dict = R_connection.prepare_param_dict(dict_local, parameters_by_value, parameters_by_name, [])
    output_dict = R_connection.execute_r_script(param_dict, r_script_path, function_name)
    return output_dict

def read_apply_camcor(dict_local, parameters_by_value, parameters_by_name):
    r_script_path = prepare_script_path()
    function_name = "fun_camcor_read_apply"
    param_dict = R_connection.prepare_param_dict(dict_local, parameters_by_value, parameters_by_name, [])
    output_dict = R_connection.execute_r_script(param_dict, r_script_path, function_name)
    return output_dict
