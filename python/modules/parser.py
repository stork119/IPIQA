#! /usr/bin/python
import xml.etree.ElementTree as ET
from collections import OrderedDict
import task as t

def make_task_list(root):
    task_list = []
    for task1 in root.iter('TASK'):
        parameters_by_value = get_settings_dict(task1, "parameters_by_value")
        parameters_by_name = get_settings_dict(task1, "parameters_by_name")
        updates_by_value = get_settings_dict(task1, "update_by_value") # in input_settings we have got parameterS (plural) and update (singular)
        updates_by_name = get_settings_dict(task1, "update_by_name")
        name = task1.get('class')
        if name == "TASK_DOWNLOAD":
            task = t.TASK_DOWNLOAD(parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)
        elif name == "TASK_QUANTIFY":
            task = t.TASK_QUANTIFY(parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)
        else:
            pass
        task_list.append(task)
    return task_list
  
def get_settings_dict(task, setup):
    temp_dict = OrderedDict()
    for parameters in task.findall(setup):
        for feature in parameters:
            key = feature.get('key')
            value = feature.get('value')
            temp_dict[key] = (value)
    return temp_dict
  
def make_config_dict(root):
    temp_dict = OrderedDict()
    for attribute in root:
        key = attribute.get('key')
        value = attribute.get('value')
        temp_dict[key] = (value)
    return temp_dict

def main():

    
    tree = ET.parse('input_settings.xml')
    root = tree.getroot()
    Queue = root[1][1]
    Config = root[0]
    config_dict = make_config_dict(Config)
    task_list = make_task_list(Queue)
       
    

if __name__ == "__main__":
    main()
