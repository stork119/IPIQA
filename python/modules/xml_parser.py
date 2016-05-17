#! /usr/bin/python
import xml.etree.ElementTree as ET
from collections import OrderedDict
import logging
import modules.task as t
import modules.file_managment as FM
#from importlib import import_module

logger = logging.getLogger(__name__)

def create_task(name, task_list = [], config_dict = {}):
    task_name = name.get('class')
    try:
        task_initialization = getattr(t,task_name)
    except:
        logger.error("Error. %s is unknown.", task_name)
        return
    parameters_by_value = get_settings_dict(name, "parameters_by_value") # getting dicts of settings and updates
    parameters_by_name = get_settings_dict(name, "parameters_by_name")
    updates_by_value = get_settings_dict(name, "update_by_value")
    updates_by_name = get_settings_dict(name, "update_by_name")
    task = task_initialization(parameters_by_value, 
                 	       parameters_by_name, 
			       updates_by_value, 
			       updates_by_name,
                               {'task_list' : task_list, 'config_dict' : config_dict}) #creating task class objects
    logger.debug("%s task created.", task_name)
    return task
   
def create_queue_task(queue, config_dict):
    task_list = []
    for request in queue.findall('TASK'):
        task_name = request.get('class')
        if task_name == "TASK_QUEUE" or task_name == "TASK_PARALLELIZE":
            task = create_queue_task(request, config_dict)
        else:
            task = create_task(request)
        task_list.append(task)
    #print(task_list)
    if queue.get('class') == "TASK_PARALLELIZE":
        pipeline = create_task(queue, task_list, config_dict)
    else:
        pipeline = create_task(queue, task_list)
    return pipeline

  
def get_settings_dict(task, setup):
    temp_dict = OrderedDict()
    for parameters in task.findall(setup):
        temp_dict.update(make_config_dict(parameters, 
					  task.get('class'), 
					  setup)) # passing the name of the task and type of setup (parameter/update), which might be usefull for logs/debugging
    return temp_dict
  
def make_config_dict(root, tag, setup = ""):
    temp_dict = OrderedDict()
    for attribute in root:
        key = attribute.get('key')
        value = attribute.get('value')
        #if "path" in key:
        value = FM.path_unification(value)
        temp_dict[key] = (value)
        logger.debug("[%s]:[%s] added to %s %s dictionary.", key, value, tag, setup)
    return temp_dict

def parse(input_path, relative_path):
    logger.info("Parsing XML input_settings.")
    try:
        tree = ET.parse(input_path)
    except:
        try:
            tree = ET.parse(relative_path)
        except:
            logger.error("Wrong input_settings path.")
            pipeline = None
            config_dict = None
            return pipeline, config_dict
    root = tree.getroot()
    Config = root[0]
    config_dict = make_config_dict(Config, Config.tag) # passing the 'name' of dictionary (config), which might be usefull for logs/debugging 
    """for request in root.findall('TASK'):
        task_name = request.get('class')
        if task_name == "TASK_QUEUE":
            pipeline = create_queue_task(request, config_dict)"""
    main_queue = root[1]
    pipeline = create_queue_task(main_queue, config_dict)
    return pipeline, config_dict
    
