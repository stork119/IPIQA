#! /usr/bin/python
import logging, multiprocessing, time, os
import modules.logs_configuration as LC
import modules.xml_parser as p
from modules.queue import multiproc 
from modules.task import TASK as tk
#import logging.config


def main():
    
    LC.configure()
    logger = logging.getLogger(__name__)
    
    dict_global = {}
    logger.info("Starting program...")
    input_path = "C://Users//Agnieszka//Documents//GitHub//PathwayPackage//input_output//input_settings.xml"
    #config_dict, task_list, task_list_para = p.parse(input_path)
    cofig_dict, task_list = p.parse(input_path)
    for element in task_list:
        if isinstance(task, list):
            dict_global = multiproc(dict_global, element, settings_dict)
        else:
            dict_global = element.tk.execute(dict_global)
    
if __name__ == "__main__":
    main()
