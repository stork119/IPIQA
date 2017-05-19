#! /usr/bin/python
import logging, os.path, sys
import argparse
import modules.file_managment as FM
import modules.logs_configuration as LC
import modules.xml_parser as XML_P
import modules.variable as VAR
from time import sleep

def main():
    PP_path = os.path.abspath('..')
    """Setting up logs."""
    logs_path, q_listener, queue, handler1, handler2 = LC.configure(PP_path)
    logger = logging.getLogger("IPIQA")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    logger.info("Starting program...")
    """Arg parse section."""
    parser = argparse.ArgumentParser(description = '\n PathwayPackage [PP] is '
    'an integration platform for instantaneous processing and analysis of '
    'confocal/fluorescent microscopy images software. \n[...]')
    parser.add_argument('-s',
                metavar = '<settingspath>', 
                type = str, 
                required = True, 
                nargs = 1, 
                help = 'Path to input_settings (in XML format).')
    parser.add_argument('-a',
                metavar = '<argument>', 
                type = str, 
                default=False,
                nargs = 2, 
                help = 'Parameter <key> <value> that would be add '
                'to config dictionary. I.e. -a number_of_cores 4')
    parser.add_argument('-m',
                metavar = '<multiplesettings>', 
                type = str, 
                default=False,
                nargs = 1, 
                help = 'Option allows to process multiple '
                'configuration settings.')
    parser.add_argument('-c',
                metavar = '<config>', 
                type = str, 
                default=False,
                nargs = 1, 
                help = 'Path to additional file containing '
                'configuration settings (in XML format).')
    args = parser.parse_args()
    """Setting up pipeline."""
    logger.debug('Input settings source: %s', args.s[0])
    if os.path.isabs(args.s[0]): #relative or absolute path
        settings_path = FM.path_unify(args.s[0])
    else:
        settings_path = FM.path_join(PP_path, 
                                     'configuration_settings' ,
                                     args.s[0])
    if args.a != False: # optional argument
        add_variable = VAR.Variable((args.a[0]), (args.a[1])) # [!]
        additional_arg = {(args.a[0]) : add_variable}
    else:
        additional_arg = {}
    if args.c != False: # optional (additional) config
        config_dict2 = XML_P.parse_xml(args.c[0],
                                       main_setts = False)
    else:
        c_def_path = FM.path_join(PP_path, 
                     'config',
                     'IPIQA.xml')
        config_dict2 = XML_P.parse_xml(c_def_path,
                                       main_setts = False)
    if args.m != False: # single or multiple settings
        settings_list = FM.file_get_paths(settings_path)
    else:
        settings_list = [settings_path]
    for setts in settings_list:
        logger.info('Current xml settings: %s', setts)
        pipeline, config_dict = XML_P.parse_xml(setts)
        # config_dict overwrite (additional) config_dict2 settings
        config_dict2.update(config_dict) 
        config_dict = config_dict2
        config_dict.update(additional_arg)
        FM.parse_exec_info(PP_path, logs_path, setts, config_dict)
        pipeline.execute(config_dict)

if __name__ == '__main__':
    version = sys.version_info[:2]
    if not version >= (3,5):
        print('Python version does not meet software requirments. '
        'Install python 3.5 or 3.6 to run IPIQA.')
        exit()
    main()
