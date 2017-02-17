#!/bin/bash

# This script enables to test IPIQA functions with standard input configuration_settings provided in tests/configuration_settings/ directory.

v="release"
printf "\n"
while getopts ":v:" opt; do
  case $opt in
    v)
      printf "Tests for version: $OPTARG"
      v=${OPTARG}
      ;;
    \?)
      printf "Invalid option: -$OPTARG.
      Type -v <IPIQA version> to perform tests dedicated to previous releases.
      Execute script without any additional arguments to perform tests for current release."
      exit 1
      ;;
    :)
      printf "Option -$OPTARG requires to define tests version."
      exit 1
      ;;
  esac
done

path="../tests/"$v"/configuration_settings/*.xml"

count=`ls $path 2>/dev/null | wc -l`
if [ $count != 0 ]
then 
for filename in $path
do
        printf "\nExecuting test pipeline:\n"$filename
        printf "\n\n"
        py -3 WorkflowEngine.py -s $filename
done
else
printf "\nSystem was unable to locate tests configuration settings in given location: "$path
fi 

