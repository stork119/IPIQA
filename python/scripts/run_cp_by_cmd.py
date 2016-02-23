#! /usr/bin/python
import os

cp_path = ""
pipeline = ""
input_file = ""
output_file = ""
cp_path = ""

cmd = cp_path + " -i " + input_file + " -p " + pipeline " -o " + output_file + " -c - r"

os.system(cmd)