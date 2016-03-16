#! /usr/bin/python
import xml.etree.ElementTree as ET
from collections import OrderedDict
import logging
import modules.task as t
#from importlib import import_module

logger = logging.getLogger(__name__)

def make_task_list(root):
    task_list = []
    for name in root.findall('TASK'): #iter include also childern's leaves
        task_name = name.get('class')
        #a = "modules.tasks." + task_name.lower()
        #task_module = __import__(a, globals(), locals(), [], 0)
        #task_initialization = getattr(task_module, task_name)
        try:
            task_initialization = getattr(t,task_name)
        except:
            logger.error("Error. %s is unknown.", task_name)
            return
        parameters_by_value = get_settings_dict(name, "parameters_by_value")
        parameters_by_name = get_settings_dict(name, "parameters_by_name")
        updates_by_value = get_settings_dict(name, "update_by_value") # in input_settings we have got parameterS (plural) and update (singular)
        updates_by_name = get_settings_dict(name, "update_by_name")
        task = task_initialization(parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)
        task_list.append(task)
        logger.debug("%s added to task_list.", task_name)
    return task_list
  
def get_settings_dict(task, setup):
    temp_dict = OrderedDict()
    for parameters in task.findall(setup):
        for feature in parameters:
            key = feature.get('key')
            value = feature.get('value')
            temp_dict[key] = (value)
            logger.debug("[%s]:[%s] added to %s %s dictionary.", key, value, task.get('class'), setup)
    return temp_dict
  
def make_config_dict(root):
    temp_dict = OrderedDict()
    for attribute in root:
        key = attribute.get('key')
        value = attribute.get('value')
        temp_dict[key] = (value)
        logger.debug("[%s]:[%s] added to %s %s dictionary.", key, value, root.tag, attribute.tag)
    return temp_dict

def parse(input_path):
  
    logger.info("Parsing XML input_settings.")
    tree = ET.parse(input_path)
    root = tree.getroot()
    Queue = root[1]
    Queue_para = root[1][0][2]
    Config = root[0]
    config_dict = make_config_dict(Config)
    task_list = make_task_list(Queue)
    task_list_para = make_task_list(Queue_para)
    return config_dict, task_list, task_list_para

