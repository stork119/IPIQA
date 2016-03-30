#! /usr/bin/python
import subprocess

def run_cp(cp_path, input_file, output_file, pipeline):
    command = '"' + cp_path + '" -i "' + input_file + '" -p "' + pipeline +  '" -o "' + output_file + '" -c - r'
    p=subprocess.Popen(command, shell=True)
    p.wait()

