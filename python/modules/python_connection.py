#! /usr/bin/python
import importlib.util
import logging

logger = logging.getLogger("IPIQA.python_connection")

def execute_python_script(param_dict, python_script_path, function_name):
    p_source = importlib.util.spec_from_file_location("external_module", python_script_path)
    module = importlib.util.module_from_spec(p_source)
    p_source.loader.exec_module(module)
    p_runfunction = getattr(module, function_name)
    try:
        output_dict = p_runfunction(param_dict)
        if output_dict == None:
            output_dict = {}
    except Exception as e:
        logger.error(e)
        output_dict = {}
    return output_dict

def prepare_param_dict(local_dict, parameters, external_params):
    keys_list = list(parameters.keys())
    param_dict = {}
    for key in local_dict:
        for element in keys_list:
            if key == element:
                param_dict[key] = local_dict[key].get_value(local_dict)
    _remove_external_params(param_dict, external_params)
    return param_dict

def _remove_external_params(param_dict, external_params):
    for param in external_params:
        try:
            del param_dict[param]
        except:
            pass
