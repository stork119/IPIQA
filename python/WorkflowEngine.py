#! /usr/bin/python
import logging, multiprocessing, time, os

import modules.xml_parser as p
import logging.config


def main():

    #Logging section.
    log_output_path = "C://Users//Agnieszka//Documents//GitHub//PathwayPackage//python//logs//"
    log_filename =  log_output_path + ((time.strftime("%Y_%m_%d_")  + "_" + time.strftime("%H_%M")) ) + ".log" # setup log filename
    logging.config.fileConfig('logging.conf', defaults={'logfilename': log_filename}, disable_existing_loggers=False) #disable_existing_loggers=True, putting name of every module in logging.conf would be needed, False if we gonna make it unnecesarry
    logger = logging.getLogger(__name__)
    logger.info("Starting program...")

    input_path = "C://Users//Agnieszka//Documents//GitHub//PathwayPackage//input_output//input_settings.xml"
    config_dict, task_list, task_list_para = p.parse(input_path)
    print(config_dict)
    
if __name__ == "__main__":
    main()
