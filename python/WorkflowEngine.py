#! /usr/bin/python
import logging, multiprocessing, time, os
import modules.logs_configuration as LC
import modules.xml_parser as p
#import logging.config


def main():
    
    LC.configure()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting program...")
    input_path = "C://Users//Agnieszka//Documents//GitHub//PathwayPackage//input_output//input_settings.xml"
    config_dict, task_list, task_list_para = p.parse(input_path)
    print(config_dict)
    
if __name__ == "__main__":
    main()
