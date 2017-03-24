#! /usr/bin/python
from collections import OrderedDict
import modules.file_managment as FM
import modules.cellprofiler as cpm
import modules.csv_managment as CSV_M
import modules.map_plate as map_plate
import modules.r_connection as R_connection
import modules.ffc as ffc
from time import sleep
import multiprocessing 
import logging
import os

logger = logging.getLogger("Task module")

class TASK():

    dict_task = {}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args = {}):
        self.parameters_by_value = parameters_by_value
        self.parameters_by_name = parameters_by_name
        self.updates_by_value = updates_by_value
        self.updates_by_name = updates_by_name
        #self.logger = logging.getLogger(self.__class__.__name__) - doesn't work with parallelize

    def execute(self, dict_global):
        dict_local = dict_global.copy()
        logger.debug("dict_local before update: %s", dict_local.keys())
        dict_local = self.update_dict(dict_local, dict_local, self.parameters_by_value, self.parameters_by_name) #check out if its working 
        logger.debug("dict_local after update: %s", dict_local.keys())
        logger.info("Executing: %s", self.__class__.__name__) #information what task is being executed
        dict_setts = self.parse_task_arguments(dict_local)
        self.execute_specify(dict_local, dict_setts)
        logger.debug("dict_local after execute_specify: %s", dict_local.keys()) #dunno if its needed
        logger.debug("dict_global before update: %s", dict_global.keys())
        dict_global = self.update_dict(dict_global, dict_local, self.updates_by_value, self.updates_by_name)
        logger.debug("dict_global after update: %s", dict_global.keys())
        return dict_global

    def parse_task_arguments(self, dict_local):
        dict_setts = {}
        for key in self.dict_task:
            try: 
                value = dict_local[key]
            except:
                try:
                    value = self.dict_task[key]["default"]
                except:
                    if self.dict_task[key]["required"]:
                        logger.error("Required parameter %s is missing for %s.", key, str(self.__class__.__name__))
                        exit()
            dict_setts[key] = value
        return dict_setts

    def update_dict(self, dict_out, dict_in, list_by_value, list_by_name):
        for k, v in list_by_value.items(): #update by value
            dict_out[k] = v
            logger.debug("Dict_out new key (updated by value): %s", k)
        for k, v in list_by_name.items(): #update by name
            logger.debug("Dict_in (by names) key, value: %s, %s", k, v)
            try:
                value = dict_in[v]
            except:
                logger.error("Dictionary update_by_name error. Given key (%s) doesn't exist in dictionary", v)
            dict_out[k] = value
            logger.debug("Dict_out new key, value (updated by name): %s, %s", k, v)
        logger.debug("Dict_out before concatenation: %s", dict_out.keys())
        try:
            dict_out = self.concatenation_name_nr(dict_out)
        except:
            logger.error("Dictionary concatenation error. Dictionary: %s concatenation failed.", dict_out.keys())
        logger.debug("Dict_out after concatenation: %s", dict_out.keys())        
        return dict_out

    def concatenation_name_nr(self, dict_out):      
        #concatenation name.number
        key_list = []
        for k, v in dict_out.items():
            if "." in k:
                key = k.split(".")
                key_list.append(key[0])
        logger.debug("List of names to concatenate: %s", key_list)
        if len(key_list) > 1:
            temp_dict = dict_out.copy()
            temp_dict2 = OrderedDict(sorted(dict_out.items()))
            key_list = list(set(key_list))      
            for i in range(len(key_list)):
                value = []
                for k, v in temp_dict2.items():
                    if key_list[i] + "." in k:
                        value.append(str(v))
                        del temp_dict[k] # deleting name.number from temporary dictionary
                value = "".join(value)
                temp_dict[key_list[i]] = value
            dict_out = temp_dict.copy()
        return dict_out

class TASK_FOR(TASK):

    dict_task = {}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.variables_list = args['variables_list']
        self.task_do = args['task_do']
        
    def execute_specify(self, dict_local, dict_setts):
        for variable in self.variables_list:
            dict_local_for = self.update_dict(dict_local, dict_local, variable['parameters_by_value'], variable['parameters_by_name'])
            self.task_do.execute(dict_local_for)

class TASK_QUEUE(TASK):
 
    dict_task = {}
 
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.task_list = args['task_list']

    def execute_specify(self, dict_local, dict_setts):
        for task in self.task_list:
            dict_local = task.execute(dict_local)


class TASK_CHECK_COMPLETNESS(TASK): # [!] not supported

    dict_task = {"experiment_finished" : {"required" : True, "default" : True},
                 "input_path" : {"required" : True}, 
                 "required_files" : {"requred" : False},
                 "sleep_time" : {"requred" : True}}
    # [!] class requires changes after merge with branch map_plate

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        in_path = dict_setts["input_path"]
        try:
            job_done = str(dict_setts["experiment_finished"])
            job_done = job_done.lower()
            if job_done == "no" or job_done ==  "0" or job_done == "false" or job_done == False:
                required_files = (dict_setts["required_files"]).split(",")
                sleep_time = int(dict_setts["sleep_time"])
                FM.dir_check_completeness(in_path, required_files, sleep_time)
        except:
            pass

class TASK_DOWNLOAD(TASK):

    dict_task = {"input_path" : {"required" : True}, 
                 "output_path" : {"requred" : True}}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        logger.info("TASK_DOWNLOAD from input: %s to output :%s", dict_setts["input_path"], dict_setts["output_path"]) 
        FM.dir_copy(dict_setts["input_path"], dict_setts["output_path"])


class TASK_REMOVE(TASK):

    dict_task = {"input_path" : {"required" : True}}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        FM.dir_remove(dict_setts["input_path"])

   
class TASK_QUANTIFY(TASK):

    dict_task = {"cp_path" : {"required" : True},
                 "input_path" : {"required" : True},
                 "output_path" : {"required" : True},
                 "pipeline" : {"required" : True}}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        cpm.run_cp_by_cmd(dict_setts["cp_path"], dict_setts["input_path"], 
                          dict_setts["output_path"], dict_setts["pipeline"])
   
class TASK_MERGE_SUBDIR_CSV(TASK):
 
    dict_task = {"input_path" : {"required" : True},
                 "output_path" : {"required" : True},
                 "csv_names_list" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","},
                 "column_name" : {"required" : True, "default" : "well.name"}}
 
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        csv_names = (dict_setts["csv_names_list"]).split(",")
        main_subdir_list = FM.dir_get_paths(dict_setts["input_path"])
        for csv_name in csv_names:
            subdir_list = CSV_M.filter_subdir_list(main_subdir_list, csv_name) #filtering directiories containing given csv file
            data = CSV_M.merge_subdir_csv(csv_name, subdir_list, dict_setts["delimiter"], dict_setts["column_name"])
            extension = FM.file_get_extension(csv_name)
            len_ext = len(extension)
            name = csv_name[:-(len_ext)]
            dict_local[name] = data
            #Saving data
            out_path = FM.path_join(dict_setts["output_path"], csv_name)
            if FM.path_check_existence(out_path):
                logger.warning("File %s already exists. Removing old data.", out_path)
                FM.dir_remove(out_path)
            CSV_M.write_csv(out_path, dict_setts["delimiter"], data) #if we would like to write_csv somewhere...


class TASK_PARALLELIZE(TASK):

    dict_task = {"input_path" : {"required" : True},
                 "number_of_cores" : {"required" : True, "default" : "1"}, 
                 "sleep_time" : {"required" : True}}
    # [!] number_of_cores is temporary coded as string
    # [!] class requires changes after merge with branch map_plate

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.task_list = args['task_list']
        self.config_dict = args['config_dict']

    def execute_specify(self, dict_local, dict_setts):
        dir_list, folders_number = self.parsing_elements_list(dict_local, dict_setts)
        processes_number = int(dict_setts["number_of_cores"])
        sleep_time = int(dict_setts["sleep_time"])
        new_dirs = dir_list
        pool = multiprocessing.Pool(processes_number)
        while True:
            if len(new_dirs) > 0:
                args = ((dict_local, element) for element in new_dirs) #or just pass task, because we're able to get task_list and settings_dict from init if both functions will stay here
                pool.map_async(self._execute_queue, args)
            if len(dir_list) >= folders_number:
                break
            sleep(sleep_time)
            input_path = str(dict_setts["input_path"])
            new_dir_list = FM.dir_get_names(input_path)
            new_dirs = [i for i in new_dir_list if i not in dir_list]
            dir_list = new_dir_list
        pool.close()
        pool.join()

    def _execute_queue(self, args):
        dict_local, element = args
        dict_local["folder_name"] = element
        for task in self.task_list:
            task.execute(dict_local)

   
class TASK_PARALLELIZE_LIST(TASK_PARALLELIZE): # list of objects (folders)

    dict_task = {"input_path" : {"required" : True},
                 "number_of_cores" : {"required" : True, "default" : "1"}, 
                 "sleep_time" : {"required" : True},
                 "folders_list" : {"required" : True}}
    # [!] number_of_cores is temporary coded as string
    # [!] class requires changes after merge with branch map_plate

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def parsing_elements_list(self, dict_local, dict_setts):
        paths = []
        input_path = str(dict_setts["input_path"])
        folder_list = (dict_setts["folders_list"]).split(",")
        for folder in folder_list:
            path = FM.path_join(input_path, folder)
            paths.append(path)
        folders_number = len(paths)
        return paths, folders_number


class TASK_PARALLELIZE_PATH(TASK_PARALLELIZE): #all objects (folders) in given directory (path)

    dict_task = {"input_path" : {"required" : True},
                 "number_of_cores" : {"required" : True, "default" : "1"}, 
                 "sleep_time" : {"required" : True},
                 "folders_number" : {"required" : True}}
    # [!] number_of_cores is temporary coded as string
    # [!] class requires changes after merge with branch map_plate

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.config_dict = args['config_dict']

    def parsing_elements_list(self, dict_local, dict_setts):
        folders_number = int(dict_setts["folders_number"])
        input_path = str(dict_setts["input_path"])
        dir_list = FM.dir_get_names(input_path)
        return dir_list, folders_number

class TASK_MAP_PLATE(TASK):

    dict_task = {"input_path_csv" : {"required" : True},
                 "input_path_metadata" : {"required" : True}, 
                 "output_path" : {"required" : True},
                 "csv_names_list" : {"required" : True},
                 "exp_id" : {"required" : True, "default" : "1"},
                 "delimiter_csv" : {"required" : True, "default" : ","},
                 "delimiter_mp" : {"required" : True, "default" : "\t"},
                 "exp_part" : {"required" : True, "default" : "1"},
                 "exp_parts" : {"required" : True, "default" : "1"}}
    # [!] class will be removed after merge with branch map_plate

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        input_path_csv = dict_local["input_path_csv"]
        input_path_metadata = dict_local["input_path_metadata"]
        output_path = dict_local["output_path"]
        csv_names = (dict_local["csv_names_list"]).split(",")
        try:
            exp_id = dict_local["exp_id"]
        except:
            exp_id = 1
        try:
            delimiter_csv = dict_local["delimiter_csv"]
        except:
            delimiter_csv = ","
        try:
            delimiter_mp = dict_local["delimiter_mp"]
        except:
            delimiter_mp = "\t"
        try:
            exp_part_id = dict_local["exp_part"]
            exp_parts = dict_local["exp_parts"]
        except:
            exp_part_id = "1" 
            exp_parts = "1"
        map_plate.combine(input_path_csv, input_path_metadata, output_path, csv_names, exp_id, exp_part_id, exp_parts, delimiter_mp, delimiter_csv)

class TASK_R(TASK):

    dict_task = {"r_function_name" : {"required" : True},
                 "r_script_path" : {"required" : True}}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        external_params = ["r_function_name", "r_script_path"]
        logger.info("Executing R function %s from %s", dict_setts["r_function_name"], dict_setts["r_script_path"]) 
        # PLACEHOLDER for adding more external params
        param_dict = R_connection.prepare_param_dict(dict_local, self.parameters_by_value, self.parameters_by_name, external_params)
        output_dict = R_connection.execute_r_script(param_dict, dict_setts["r_script_path"], dict_setts["r_function_name"])
        dict_local.update(output_dict)
        
class TASK_FFC_CREATE(TASK):

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        # Check if user set input an output paths
        output_dict = ffc.create_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)

class TASK_FFC_READ(TASK):

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        # Check if user set input an output paths
        try:
            output_dict = ffc.read_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        except:
            output_dict = ffc.create_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)

class TASK_FFC_APPLY(TASK):

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        # Check if user set input an output paths
        output_dict = ffc.apply_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)
   
   
class TASK_FFC_READ_APPLY(TASK):
 
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        # Check if user set input an output paths
        output_dict = ffc.read_apply_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)
        
class TASK_READ_DATAFRAME_FROM_CSV(TASK):

    dict_task = {"input_path" : {"required" : True},
                 "filename" : {"required" : True},
                 "dict_key_name" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","}}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        input_path = FM.path_join(dict_setts["input_path"], dict_setts["filename"])
        data = R_connection.read_dataframe_from_csv(input_path, dict_setts["delimiter"])
        dict_local[dict_setts["dict_key_name"]] = data

class TASK_WRITE_DATAFRAME_TO_CSV(TASK):

    dict_task = {"output_path" : {"required" : True},
                 "filename" : {"required" : True},
                 "dict_key_name" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","}}
    
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        output_path = FM.path_join(dict_setts["output_path"], dict_setts["filename"])
        data = dict_local[dict_setts["dict_key_name"]]
        R_connection.write_dataframe_to_csv(output_path, data, dict_setts["delimiter"])

class TASK_MERGE_CSV(TASK):

    dict_task = {"input_path_1" : {"required" : True},
                 "input_path_1" : {"required" : True},
                 "csv_names_list" : {"required" : True},
                 "output_path" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","}}

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local, dict_setts):
        in_path_list = []
        in_path_list.append(dict_setts["input_path_1"])
        in_path_list.append(dict_setts["input_path_2"])
        csv_names = (dict_setts["csv_names_list"]).split(",")
        for csv_name in csv_names:
            data = CSV_M.simple_merge(csv_name, in_path_list, dict_setts["delimiter"])
            #Saving data
            out_path = FM.path_join(dict_setts["output_path"], csv_name)
            if FM.path_check_existence(out_path):
                logger.warning("File %s already exists. Removing old data.", out_path)
                FM.dir_remove(out_path)
            CSV_M.write_csv(out_path, dict_setts["delimiter"], data) #if we would like to write_csv somewhere...
            # PLACEHOLDER adding data to dictionary 
