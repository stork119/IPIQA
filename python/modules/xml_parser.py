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
       
class VariableReference(Variable):
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_ref_key(self):
        return self.value

    def get_reference(self, env): # function name requires changes
        ref_value = self.get_value(env)
        var = Variable(self.key, ref_value)
        return var

    def get_value(self, env, args = {}):
        return env[self.value].get_value(env, args)

def parse_param(param_dict, param):
    key = param.get('key')
    value = param.get('value')
    try:
        p_type = param.get('type')
    except:
        p_type = "string"
    if p_type == "ref" or p_type == "reference":
        var = VariableReference(key, value)
    else:
        var = Variable(key, value)
    param_dict[key] = var

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

def _create_for_task(queue): #[from old xml_parser]
    variables = queue.find('VARIABLES')
    variables_list = []
    for request in variables.findall('VARIABLE'):
        parameters = _get_settings_dict(request, "parameters")
        variables_list.append(parameters)
    task_request = queue.find('TASK')
    task_name = task_request.get('class')
    if task_name == "TASK_QUEUE" or task_name.startswith("TASK_PARALLELIZE") or task_name.startswith("TASK_SYNCHRONOUSLY"):
        task_do = _creaste_queue_task(task_request)
    elif  task_name == "TASK_FOR":
        task_do = _create_for_task(task_request)
    else:
        task_do = _create_task(task_request)  
    task = TK.TASK_FOR({},
                       {},
                       {'variables_list' : variables_list, 'task_to_do' : task_do}) #creating task class objects
    return task

def _get_settings_dict(task, set_type):
    settings = {}
    for parameters_set in task.findall(set_type):
        for param in parameters_set:
            parse_param(settings, param)
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




