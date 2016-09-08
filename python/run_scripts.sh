#!/bin/bash
settings_path=$1

for filename in $settings_path*.xml
do
        printf "\nExecuting pipeline:\n"$filename
        printf "\n\n"
        py WorkflowEngine.py -s $filename
done

#PATH=$PATH:/C:/Users/Pathway/AppData/Local/Programs/Python/Python35-32/
