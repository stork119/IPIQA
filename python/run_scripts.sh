#!/bin/bash
settings_path=$1*xml
settings_path="$(echo ${settings_path} | tr '\\' '/')"
count=`ls $settings_path 2>/dev/null | wc -l`

if [ $count != 0 ]
then 
for filename in $settings_path
do
         printf "\nExecuting pipeline:\n"$filename
        printf "\n\n"
        py -3 WorkflowEngine.py -s $filename || python WorkflowEngine.py -s $filename
done
else
printf "\nSystem was unable to locate tests configuration settings in given location: "$path
fi 