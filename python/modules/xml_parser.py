
#! /usr/bin/python
import logging, sys
import xml.etree.ElementTree as ET
import modules.file_managment as FM
import modules.task as TK
import modules.variable as VAR

logger = logging.getLogger("XML parser")

def _parse_parted_param(param_dict, param, parted_dict, p_part):
    key = param.get('key')
    if key not in parted_dict:
        parted_dict[key] = {}
    variable = _create_variable(param)[0]
    parted_dict[key][p_part] = variable

def _add_variable_parted(settings, parted_params):
    for key, params_set in parted_params.items():
        variable = VAR.VariableParted(key, parted_params[key])
        settings[key] = variable

def _parse_variable_structure(key, param, args):
    struc_dict = {}
    for j, subparam in enumerate(param):
        var, subkey = _create_variable(subparam)
        struc_dict[subkey] = var
    variable = VAR.VariableStructure(key, struc_dict)
    return variable

def _parse_mp_element(key, value, param, args):
    if value == None:
        value = param.get('mp_name')
    for mp_param in param:
        variable, mpe_key = _create_variable(mp_param)
        if mpe_key in ["param", "well"]:
            args[mpe_key] = variable
        else:
            logger.error("Unexpected map_plate parameter key: %s", mpe_key)
    variable = VAR.VariableMP(key, value, args)
    return variable

def _parse_variable_list(key, param, args):
    values_list = []
    for i, subparam in enumerate(param):
        var = _create_variable(subparam, key)[0]
        values_list.append(var)
    variable = VAR.VariableList(key, values_list, args)
    return variable

def _create_variable(param, tmp_key = ""):
    key = param.get('key')
    if key == None:
        key = tmp_key
    value = param.get('value')
    p_type = param.get('type')
    args = {"type" : p_type}
    if p_type == "ref" or p_type == "reference":
        var = VAR.VariableReference(key, value, args)
    elif p_type == "path":
        var = VAR.VariablePath(key, value, args)
    elif p_type == "list":
        var = _parse_variable_list(key, param, args)
    elif p_type == "structure" or p_type == "struc":
        var = _parse_variable_structure(key, param, args)
    elif p_type == "map_plate" or p_type == "mp":
        var = _parse_mp_element(key, value, param, args)
    else:
        var = VAR.Variable(key, value, args)
    return var, key

def parse_param(param_dict, param, parted_dict = {}):
    p_part = param.get('part')
    if p_part != None:
        _parse_parted_param(param_dict, param, parted_dict, p_part)
    else:
        variable, key = _create_variable(param)
        param_dict[key] = variable

def _create_config_dict(root, tag):
    #config = OrderedDict()
    config = {}
    for parameter in root:
        parse_param(config, parameter)
    return config

def _create_queue_task(queue):
    task_list = []
    for task in queue.findall('TASK'):
        task_name = task.get('class')
        if task_name == "TASK_QUEUE" or task_name == "TASK_IF" or task_name.startswith("TASK_PARALLELIZE"):
            task = _create_queue_task(task)
        elif task_name == "TASK_FOR":
            task = _create_for_task(task)
        else:
            task = _create_task(task)
        task_list.append(task)
    pipeline = _create_task(queue, task_list)
    return pipeline

def _parse_for_variables(variab):
    variables_list = []
    for variable_set in variab.findall('VARIABLE'):
        parameters = _get_settings_dict(variable_set, "parameters")
        param_var = VAR.VariableStructure("variables", parameters)
        variables_list.append(param_var)
    var = VAR.VariableList("variables_list", variables_list)
    return var

def _create_for_task(queue):
    variables = queue.find('VARIABLES')
    ref_name = variables.get('value')
    if str(ref_name) == "None":
        var = _parse_for_variables(variables)
    else:
        var = VAR.VariableReference("variable_list", ref_name)
    task_request = queue.find('TASK')
    task_name = task_request.get('class')
    if task_name == "TASK_QUEUE" or task_name.startswith("TASK_PARALLELIZE") or task_name.startswith("TASK_SYNCHRONOUSLY"):
        task_do = _create_queue_task(task_request)
    elif task_name == "TASK_FOR":
        task_do = _create_for_task(task_request)
    else:
        task_do = _create_task(task_request)  
    task = TK.TASK_FOR({},
                       {},
                       {'variables_list' : var, 'task_to_do' : task_do}) #creating task class objects
    return task

def _get_settings_dict(task, set_type):
    settings = {}
    parted_params = {}
    for parameters_set in task.findall(set_type):
        for param in parameters_set:
            parse_param(settings, param, parted_params)
    _add_variable_parted(settings, parted_params)
    return settings

def _create_task(name, task_list = [], config_dict = {}):
    task_name = name.get('class')
    try:
        task_initialization = getattr(TK, task_name)
    except AttributeError:
        logger.error("Error. %s is unknown.", task_name)
        sys.exit(1) # wrong/non existing task_name -> shutting down program 
    parameters = _get_settings_dict(name, "parameters") # getting dicts of settings and updates
    updates = _get_settings_dict(name, "updates")
    task = {}
    task = task_initialization(parameters, updates,
                               {'task_list' : task_list, 
                                'config_dict' : config_dict}) #creating task class objects
    logger.debug("%s task created.", task_name)
    return task

def parse_xml(input_path, main_setts = True):
    if main_setts == True:
        logger.info("Parsing XML input_settings.")
    else:
        logger.info("Parsing additional config input_settings.")
    try:
        tree = ET.parse(input_path)
    except Exception as e:
        if FM.path_check_existence(input_path):
            logger.error("Input_settings parsing error. Cannot parse %s as XML.", input_path)
            #logger.error(e)
        else:
            logger.error("Given input_settings: %s doesn't exist.", input_path)
        sys.exit(1) # wrong/non existing input settings -> shutting down program 
    root = tree.getroot()
    Config = root[0]
    config_dict = _create_config_dict(Config, Config.tag)
    if main_setts == True:
        main_queue = root[1]
        pipeline = _create_queue_task(main_queue)
        return pipeline, config_dict
    return config_dict
