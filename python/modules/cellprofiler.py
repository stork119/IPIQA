#! /usr/bin/python
import subprocess
import logging
import os.path
import sys

logger = logging.getLogger(__name__)

def run_cp_by_cmd(cp_path, input_file, output_file, pipeline):
    if not check_pipeline(pipeline):
        return
    command = '"' + cp_path + 'Cellprofiler.exe"' + ' -c -r -i "' + input_file +   '" -o "' + output_file + '" -p "' + pipeline + '"'
    p=subprocess.Popen(command, shell=True)
    p.wait()

def check_pipeline(pipeline):
    pip_form = pipeline[-6:]
    if os.path.isfile(pipeline) and pip_form == "cppipe":
        #logger.debug("Pipeline path: %s exists.", pipeline)
        return True
    else:
        logger.error("Given pipeline path: %s doesn't exist or the file format is incorrect.", pipeline)
        return False
        
        
# cd Documents/GitHub/PathwayPackage/python/
# py WorkflowEngige.py -s "C://Users//Agnieszka//Documents//GitHub//PathwayPackage//input_output//settings_04_21.xml"