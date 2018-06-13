#! /usr/bin/python
import subprocess
import logging
import os.path
import sys
#import modules.file_managment as FM

logger = logging.getLogger("IPIQA.cellprofiler")

def run_cp_by_cmd(cp_path, input_file, output_file, pipeline, cp_memory_size):
    if not _pipeline_verification(pipeline):
        return
    command = '"' + cp_path + 'Cellprofiler.exe"' + ' --jvm-heap-size ' + cp_memory_size + ' -c -r -i "' + input_file +   '" -o "' + output_file + '" -p "' + pipeline + '"'
    p=subprocess.Popen(command, shell=True)
    p.wait()

def _pipeline_verification(pipeline):
    #if file_verify_extension(pipeline, extension = "cppipe") and path_check_existence(path):
    #    return True
    #else:
    #    logger.error("Given pipeline path: %s doesn't exist or the file format is incorrect.", pipeline)
    #    return False
    pip_form = pipeline[-6:]
    if os.path.isfile(pipeline) and pip_form == "cppipe":
        #logger.debug("Pipeline path: %s exists.", pipeline)
        return True
    else:
        logger.error("Given pipeline path: %s doesn't exist or the file format is incorrect.", pipeline)
        return False
