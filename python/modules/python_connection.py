#! /usr/bin/python
import importlib.util
import logging

logger = logging.getLogger("IPIQA.python_connection")

def execute_python_script(param_dict, python_script_path, function_name):
    """
    Executes chosen function of defined python script.
   
    python_connection works like r_connection module:
    - All parameters from input_settings would be parsed 
     within python dictionary.
    - All executable functions should take dictionary as an input.
    - Any return values should be give back witin dictionary.
    In the absence of output, function execute_python_script would create
    empty dictionary itself.
   
    In case of multi-module scripts programmer 
    should take care of proper module imports 
    (due to current working directory might be different than script's directory).
   
    input_settings usage example:
    <TASK class="TASK_PYTHON">
        <parameters>
            <parameter key="python_function_name" value = <FUNCTION_NAME>/>
            <parameter key="python_script_path" value = <PATH_TO_SCRIPT>/>
            <parameter key="arg" value = "<ARG>"/>
        </parameters>
    </TASK>
   
    i.e.
    <TASK class="TASK_PYTHON">
        <parameters>
            <parameter key="python_function_name" value = "rename_file"/>
            <parameter key="python_script_path" value = "F://AG//files_manipulations.py"/>
            <parameter key="in_name" value = "filename"/>
            <parameter key="out_name" value="filename_v2"/>
        </parameters>
    </TASK>
    """
    p_source = importlib.util.spec_from_file_location(
                    "external_module", python_script_path)
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
                val = local_dict[key].get_value(local_dict)
                param_dict[key] = val
    _remove_external_params(param_dict, external_params)
    return param_dict

def _remove_external_params(param_dict, external_params):
    for param in external_params:
        try:
            del param_dict[param]
        except:
            pass
