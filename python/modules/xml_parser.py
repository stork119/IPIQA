#! /usr/bin/python
import logging, sys
import xml.etree.ElementTree as ET
import modules.file_managment as FM
import modules.task as TK

logger = logging.getLogger("Environment module")
#logger = logging.getLogger("XML parser")

class Variable():
    def __init__(self, key, value, args = {}):
        self.key = key
        self.value = value
        self.args = args

    def get_value(self, env, args = {}):
        return self.value

    def set_value(self, value, args = {}):
        self.value = value
        return
     
    def get_variable(self, env):
        return self

class VariableReference(Variable):
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_ref_key(self):
        return self.value

    def get_variable(self, env):
        # creates variable with reference value
        ref_value = self.get_value(env)
        var = Variable(self.key, ref_value)
        return var

    def get_value(self, env, args = {}):
        return env[self.value].get_value(env, args)

class VariableList(Variable):
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_variable(self, env):
        # creates variable with merged value
        merged_value = self.get_value(env)
        var = Variable(self.key, merged_value)
        return var

    def get_value(self, env, args = {}):
        order = sorted(self.value.keys())
        values_list = []
        for key in order:
            v_part = self.value[key].get_value(env)
            values_list.append(v_part)
        return "".join(values_list)

def _parse_parted_param(param_dict, param, parted_dict, p_part):
    key = param.get('key')
    if key not in parted_dict:
        parted_dict[key] = {}
    variable = _create_variable(param)[0]
    parted_dict[key][p_part] = variable

def _add_variable_list(settings, parted_params):
    for key, params_set in parted_params.items():
        variable = VariableList(key, parted_params[key])
        settings[key] = variable

def _create_variable(param):
    key = param.get('key')
    value = param.get('value')
    p_type = param.get('type')
    if p_type == "ref" or p_type == "reference":
        var = VariableReference(key, value)
    else:
        var = Variable(key, value)
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

def _create_for_task(queue):
    variables = queue.find('VARIABLES')
    variables_list = []
    for variable_set in variables.findall('VARIABLE'):
        parameters = _get_settings_dict(variable_set, "parameters")
        variables_list.append(parameters)
    task_request = queue.find('TASK')
    task_name = task_request.get('class')
    if task_name == "TASK_QUEUE" or task_name.startswith("TASK_PARALLELIZE") or task_name.startswith("TASK_SYNCHRONOUSLY"):
        task_do = _creaste_queue_task(task_request)
    elif task_name == "TASK_FOR":
        task_do = _create_for_task(task_request)
    else:
        task_do = _create_task(task_request)  
    task = TK.TASK_FOR({},
                       {},
                       {'variables_list' : variables_list, 'task_to_do' : task_do}) #creating task class objects
    return task

def _get_settings_dict(task, set_type):
    settings = {}
    parted_params = {}
    for parameters_set in task.findall(set_type):
        for param in parameters_set:
            parse_param(settings, param, parted_params)
    _add_variable_list(settings, parted_params)
    return settings

def _create_task(name, task_list = [], config_dict = {}):
    task_name = name.get('class')
    try:
        task_initialization = getattr(TK, task_name)
    except:
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

def parse_xml(input_path, additional_arg, main_setts = True):
    if main_setts == True:
        logger.info("Parsing XML input_settings.")
    else:
        logger.info("Parsing additional config input_settings.")
    try:
        tree = ET.parse(input_path)
    except:
        if FM.path_check_existence(input_path):
            logger.error("Input_settings parsing error. Cannot parse %s as XML.", input_path)
        else:
            logger.error("Given input_settings: %s doesn't exist", input_path)
        sys.exit(1) # wrong/non existing input settings -> shutting down program 
    root = tree.getroot()
    Config = root[0]
    config_dict = _create_config_dict(Config, Config.tag)
    #config_dict.update(additional_arg) # [!] not supported atm
    if main_setts == True:
        main_queue = root[1]
        pipeline = _create_queue_task(main_queue)
        return pipeline, config_dict
    return config_dict
