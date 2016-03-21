#! /usr/bin/python
import logging, multiprocessing, time, os
import modules.logs_configuration as LC
import modules.xml_parser as p
from modules.queue import QUEUE
from modules.task import TASK
#import logging.config


def main():
    
    PP_path = os.path.abspath('..')
    LC.configure(PP_path)
    logger = logging.getLogger(__name__)
    dict_global = {}
    logger.info("Starting program...")
    input_path= (os.path.join(PP_path, "input_output", "input_settings.xml")).replace("\\", "//") # setting up path to input settings (in xml format)
    config_dict, task_list, task_list_para = p.parse(input_path)
    print(config_dict)
    """cofig_dict, task_list = p.parse(input_path)
    for element in task_list:
        if isinstance(task, list):
            dict_global = QUEUE.multiproc(dict_global, element, settings_dict)
        else:
            dict_global = element.TASK.execute(dict_global)"""
    
if __name__ == "__main__":
    main()
