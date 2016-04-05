#! /usr/bin/python
import logging, multiprocessing, time, os
import argparse

import modules.logs_configuration as LC
import modules.xml_parser as p
from modules.task import TASK


def main():
    #Logging section.
    PP_path = os.path.abspath('..')
    LC.configure(PP_path)
    logger = logging.getLogger(__name__)
    logger.info("Starting program...")
    #Arg parse section.
    parser = argparse.ArgumentParser( description='\n (...Example description...)' )
    parser.add_argument( '-s',
                metavar='<settingspath>', 
                type=str, 
                required=True, 
                nargs=1, 
                help='Input_settings path' )
    args = parser.parse_args()
    #Setting up pipeline.
    pipeline = p.parse(args.s[0])
    """Default input_settings path.
    input_path= (os.path.join(PP_path, "input_output", "settings2.xml").replace("\\", "//")) # setting up path to input settings (in xml format)
    pipeline= p.parse(input_path)"""
    #pipeline.execute()
if __name__ == "__main__":
    main()
