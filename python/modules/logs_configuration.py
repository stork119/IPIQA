#! /usr/bin/python
import logging, os, multiprocessing
from time import strftime
import os
from logging.handlers import QueueHandler, QueueListener

def configure(PP_path):
    # Setting up log level
    level = logging.INFO

    log_output_path = (os.path.join(PP_path, "python", "logs", "")).replace("\\", "//")
    log_filename = ((strftime("%Y_%m_%d_")  + "_" + strftime("%H_%M")) ) + ".log" 
    log_file =  log_output_path + log_filename # setup log filename
    # Creating log handlers for stream (handler1) and file (handler2):
    handler1 = logging.StreamHandler()
    handler2 = logging.FileHandler(log_file)
    # Setting up log format:
    base_formater = logging.Formatter("%(asctime)s ; %(name)-20s ; %(levelname)-8s ; %(message)s")
    handler1.setFormatter(base_formater)
    handler2.setFormatter(base_formater)
    #Setting up log level:
    handler1.setLevel(level)
    handler2.setLevel(level)
    
    queue = multiprocessing.Queue()
    q_listener = QueueListener(queue, handler1, handler2)
    q_listener.start()

    logger = logging.getLogger("logs_configuration")
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    logger.setLevel(logging.DEBUG)
    logger.info("Logs initialization...")
    
    return log_filename, log_file, q_listener, queue, handler1, handler2, level
