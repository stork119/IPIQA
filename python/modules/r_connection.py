#! /usr/bin/python
import logging
from rpy2.rinterface import RRuntimeError

logger = logging.getLogger("IPIQA.r_connection")

try:
    import rpy2.robjects as robjects
    from rpy2.robjects.vectors import DataFrame
except:
    logger.warning("Rpy2 import error. The package is not installed. R scripts processing is not available.")

logger = logging.getLogger("IPIQA.r_connection")

def execute_r_script(param_dict, r_script_path, function_name):
    r_source = robjects.r['source']
    r_source(r_script_path)
    r_runfunction = robjects.globalenv[function_name]
    r_param_list = robjects.ListVector(param_dict)
    do_call = robjects.r['do.call']
    try:
        out = do_call(r_runfunction, r_param_list)
    except RRuntimeError as e:
        """
        Msg will display two times,
        first time just because exception was called,
        second time would proper, normal logger msg.
        It seems you cannot avoid first msg pop
        even by catching and redirecting stream.
        """
        logger.error("Cannot execute fucntion %s from %s script due to: %s.", 
                     function_name,r_script_path, e)
        return {}
    try:
        output_dict = {key : out.rx2(key) if len(out.rx2(key)) > 1 else out.rx2(key)[0] for key in out.names }
    except:
        output_dict = {}
    gc = robjects.r['gc']
    out = gc()
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

def read_dataframe_from_csv(input_path, delimiter):
    data = DataFrame.from_csvfile(input_path, sep = delimiter)
    return data

def write_dataframe_to_csv(output_path, data, delimiter):
    DataFrame.to_csvfile(data, output_path, sep = delimiter, row_names=False, eol = '\n')
