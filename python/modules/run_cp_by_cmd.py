#! /usr/bin/python
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_cp(cp_path, input_file, output_file, pipeline):
    command = '"' + cp_path + 'Cellprofiler.exe"' + ' -c -r -i "' + input_file +   '" -o "' + output_file + '" -p "' + pipeline + '"'
    p=subprocess.Popen(command, shell=True)
    p.wait()

