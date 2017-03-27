TASK_NAME - variable_key - is_required(TRUE/FALSE) - default_value - description
TASK_FOR - >< - >< - >< - Task do not have predefined variables
TASK_QUEUE - >< - >< - >< - Task do not have predefined variables
TASK_CHECK_COMPLETNESS - experiment_finished - TRUE - "True" - define if the experiment is finished
TASK_CHECK_COMPLETNESS - input_path - TRUE - >< - path to the verified dir
TASK_CHECK_COMPLETNESS - required_files - TRUE - [] - list of needed data to verify dir completness
TASK_CHECK_COMPLETNESS - sleep_time - TRUE - >< - time between veryfing file presence
TASK_DOWNLOAD - input_path - TRUE - >< - path to the downloaded file
TASK_DOWNLOAD - output_path - TRUE - >< - path to save file
TASK_REMOVE- input_path - TRUE - >< - path to the removed file
TASK_QUANTIFY - cp_path - TRUE - >< - path to cellprofiler software
TASK_QUANTIFY - input_path - TRUE - >< - path to input data
TASK_QUANTIFY - output_path - TRUE - >< - path to save output data
TASK_QUANTIFY - pipeline - TRUE - >< - path to cellprofiler pipeline
TASK_MERGE_SUBDIR_CSV - input_path - TRUE - >< - path to input data
TASK_MERGE_SUBDIR_CSV - output_path - TRUE - >< - path to save output data
TASK_MERGE_SUBDIR_CSV - csv_names_list - TRUE - >< - path to output data
TASK_MERGE_SUBDIR_CSV - delimiter - TRUE - "," - delimiter used in csv files
TASK_MERGE_SUBDIR_CSV - column_name - TRUE - "well.name" - name of the column with dir names of merged csv
TASK_PARALLELIZE - input_path - TRUE - >< - path to subdirectories on which parallelize taks would be performed
TASK_PARALLELIZE - number_of_cores - TRUE - "1" - number of threads to use
TASK_PARALLELIZE - sleep_time - TRUE - >< - time between collecting subdirs list
TASK_PARALLELIZE_LIST - input_path - TRUE - >< - path to subdirectories on which parallelize taks would be performed
TASK_PARALLELIZE_LIST - number_of_cores - TRUE - "1" - number of threads to use
TASK_PARALLELIZE_LIST - sleep_time - TRUE - >< - time between collecting subdirs list
TASK_PARALLELIZE_LIST - folders_list - TRUE - >< - list of subdir names on which parallelize taks would be performed
TASK_PARALLELIZE_PATH - input_path - TRUE - >< - path to subdirectories on which parallelize taks would be performed
TASK_PARALLELIZE_PATH - number_of_cores - TRUE - "1" - number of threads to use
TASK_PARALLELIZE_PATH - sleep_time - TRUE - >< - time between collecting subdirs list
TASK_PARALLELIZE_PATH - folders_number - TRUE - >< - number of subdirs on which parallelize taks would be performed
TASK_R - r_function_name - TRUE - >< - name of R function to execute
TASK_R - r_script_path - TRUE - >< - path to R script containing the used function
TASK_READ_DATAFRAME_FROM_CSV - input_path - TRUE - >< - path to input file
TASK_READ_DATAFRAME_FROM_CSV - filename - TRUE - >< - filename of input file
TASK_READ_DATAFRAME_FROM_CSV - dict_key_name - TRUE - >< - [!]
TASK_READ_DATAFRAME_FROM_CSV - delimiter - TRUE - "," - delimiter used in csv files
TASK_WRITE_DATAFRAME_FROM_CSV - output_path - TRUE - >< - path to save output file
TASK_WRITE_DATAFRAME_FROM_CSV - filename - TRUE - >< - filename of output file
TASK_WRITE_DATAFRAME_FROM_CSV - dict_key_name - TRUE - >< - [!]
TASK_WRITE_DATAFRAME_FROM_CSV - delimiter - TRUE - "," - delimiter used in csv files
