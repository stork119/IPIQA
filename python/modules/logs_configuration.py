#! /usr/bin/python
import logging
from time import strftime
import logging.config
import os, sys

def configure(PP_path):
    log_output_path = (os.path.join(PP_path, "python", "logs", "")).replace("\\", "//")
    log_filename =  log_output_path + ((strftime("%Y_%m_%d_")  + "_" + strftime("%H_%M")) ) + ".log" # setup log filename
    logging.config.fileConfig('logging.conf', defaults={'logfilename': log_filename}, disable_existing_loggers=False) #disable_existing_loggers=True, putting name of every module in logging.conf would be needed, False if we gonna make it unnecesarry
    logger = logging.getLogger("logs configuration")
    logger.info("Logs initialization...")
    return log_filename
