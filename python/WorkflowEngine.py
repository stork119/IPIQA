#! /usr/bin/python
import logging, os.path
import argparse
import modules.file_managment as FM
import modules.logs_configuration as LC
import modules.xml_parser as XML_P

def main():
    PP_path = os.path.abspath('..')
    """Setting up logs."""
    LC.configure(PP_path)
    logger = logging.getLogger(__name__)
    logger.info("Starting program...")
    """Arg parse section."""
    parser = argparse.ArgumentParser(description = '\n ...Example description...')
    parser.add_argument('-s',
                metavar = '<settingspath>', 
                type = str, 
                required = True, 
                nargs = 1, 
                help = 'Path to file with input_settings (in XML format).')
    args = parser.parse_args()
    """Setting up pipeline."""
    logger.debug("Input settings source: %s", args.s[0])
    if os.path.isabs(args.s[0]):
        input_settings = FM.path_unification(args.s[0])
    else:
        input_settings = FM.join_paths(PP_path, "input_output" , args.s[0])
    pipeline, config_dict = XML_P.parse(input_settings)
    print(config_dict)
    #pipeline.execute(config_dict)
if __name__ == "__main__":
    main()
