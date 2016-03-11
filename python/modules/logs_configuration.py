#! /usr/bin/python
import logging
from time import strftime
import logging.config

def configure():
    log_output_path = "C://Users//Agnieszka//Documents//GitHub//PathwayPackage//python//logs//"
    log_filename =  log_output_path + ((strftime("%Y_%m_%d_")  + "_" + strftime("%H_%M")) ) + ".log" # setup log filename
    logging.config.fileConfig('logging.conf', defaults={'logfilename': log_filename}, disable_existing_loggers=False) #disable_existing_loggers=True, putting name of every module in logging.conf would be needed, False if we gonna make it unnecesarry
    logger = logging.getLogger(__name__)
    logger.info("Logs initialization...")
