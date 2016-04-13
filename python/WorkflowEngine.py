#! /usr/bin/python
import logging, multiprocessing, time, os
import argparse

import modules.logs_configuration as LC
import modules.xml_parser as p
#from modules.task import TASK


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
    logger.debug("Input settings source: %s", args.s[0])
    pipeline, config_dict = p.parse(args.s[0])
    """Default input_settings path.
    input_path= (os.path.join(PP_path, "input_output", "settings.xml").replace("\\", "//")) # setting up path to input settings (in xml format)
    logger.debug("Input settings source: %s", input_path)
    pipeline, config_dict = p.parse(input_path)"""
    pipeline.execute(config_dict)
if __name__ == "__main__":
    main()
