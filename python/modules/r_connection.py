#! /usr/bin/python
import rpy2.robjects as robjects
from rpy2.robjects.vectors import DataFrame

def make_boxplot(param_dict, input_path, r_script_path, function_name, delimiter = "\t"):
    data = DataFrame.from_csvfile(input_path, sep = delimiter)
    param_dict['data'] = data
    r_source = robjects.r['source']
    r_source(r_script_path)
    r_makeplot = robjects.globalenv[function_name]
    r_param_list = robjects.ListVector(param_dict)
    do_call = robjects.r['do.call']
    do_call(r_makeplot, r_param_list)

def prepare_param_dict(local_dict, parameters_by_value, parameters_by_name, external_params):
    keys_by_value = list(parameters_by_value.keys())
    keys_by_name = list(parameters_by_name.keys())
    keys_list = set(keys_by_value + keys_by_name)
    param_dict = {}
    for key in local_dict:
        for element in keys_list:
            if key == element:
                param_dict[key] = local_dict[key]
    _remove_external_params(param_dict, external_params)
    return param_dict

def _remove_external_params(param_dict, external_params):
    for param in external_params:
        try:
            del param_dict[param]
        except:
            pass

