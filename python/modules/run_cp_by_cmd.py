#! /usr/bin/python
import subprocess

pipeline = ""
input_file = ""
output_file = ""
cp_path = ""

command = '"' + cp_path + '" -i "' + input_file + '" -p "' + pipeline +  '" -o "' + output_file + '" -c - r'

p=subprocess.Popen(command, shell=True)
p.wait()

