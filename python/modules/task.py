#! /usr/bin/python
from collections import OrderedDict
import modules.file_managment as FM
from modules.run_cp_by_cmd import run_cp as cp_cmd
from modules.csv import merge as merge_csv
from time import sleep
import multiprocessing 
import logging

logger = logging.getLogger(__name__)

class TASK():
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        self.parameters_by_value = parameters_by_value
        self.parameters_by_name = parameters_by_name
        self.updates_by_value = updates_by_value
        self.updates_by_name = updates_by_name
      
      
    def execute(self, dict_global):
        task_name = self.__class__.__name__
        logger.debug("TASK (class) name: %s", task_name)
        dict_local = dict_global.copy()
       # temp_dict = dict_global.copy()
        logger.debug("dict_local before update: %s", (dict_local))
        dict_local = self.update_dict(dict_local, dict_local, self.parameters_by_value, self.parameters_by_name) #check out if its working 
        logger.debug("dict_local after update: %s", dict_local)
        self.execute_specify(dict_local)
        logger.debug("dict_local after execute_specify: %s", dict_local) #dunno if its needed
        logger.debug("dict_global before update: %s", dict_global)
        dict_global = self.update_dict(dict_global, dict_local, self.updates_by_value, self.updates_by_name)
        logger.debug("dict_global after update: %s", dict_global)
        return dict_global
      
    def update_dict(self, dict_out, dict_in, list_by_value, list_by_name):
        for k, v in list_by_value.items(): #update by value
            dict_out[k] = v
            logger.debug("Dict_out new key, value (updated by value): %s, %s", k, v)
        for k, v in list_by_name.items(): #update by name
            logger.debug("Dict_in (by names) key, value: %s, %s", k, v)
            value = dict_in[v]
            dict_out[k] = value
            logger.debug("Dict_out new key, value (updated by name): %s, %s", k, value)
        logger.debug("Dict_out before concatenation: %s", dict_out)
        dict_out = self.concatenation_name_nr(dict_out)
        logger.debug("Dict_out after concatenation: %s", dict_out)        
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

class TASK_QUEUE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, task_list):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)
        self.task_list = task_list
    def execute_specify(self, dict_local):
        for task in self.task_list:
            dict_local = task.execute(dict_local)

class TASK_DOWNLOAD(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def execute_specify(self, dict_local):
        in_path = dict_local["input_path"]
        out_path = dict_local["output_path"]
        FM.copy_directory(in_path, out_path)

class TASK_REMOVE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def execute_specify(self, dict_local):
        in_path = dict_local["input_path"]
        FM.remove_directory(in_path)
        
class TASK_QUANTIFY(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def execute_specify(self, dict_local):
        cp_path = dict_local["cp_path"]
        in_path = dict_local["input_path"]
        out_path = dict_local["output_path"]
        pipeline = dict_local["pipeline"]
        cp_cmd(cp_path, in_path, out_path, pipeline)
        
class TASK_MERGE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def execute_specify(self, dict_local):
        in_path = dict_local["input_path"]
        out_path = dict_local["output_path"]
        subdir_list = FM.get_dir_names(in_path)
        csv_names = (dict_local["csv_names_list"]).split(",")
        for csv_name in csv_names:
            merge_csv(csv_name, subdir_list, in_path, out_path)

class TASK_PARALLELIZE(TASK):
   # has got object queue
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, task_list, config_dict = [], request_list = []):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)
        self.task_list = task_list
        self.config_dict = config_dict
        self.request_list = request_list

    def execute_specify(self, dict_local):
        processes_number = int(self.config_dict["number_of_cores"])
        folders_number = int(dict_local["folders_number"])
        sleep_time = 5 #int(dict_local["sleep_time"])
        pool = multiprocessing.Pool(processes_number)
        input_path = str(dict_local["input_path"])
        dir_list = FM.get_dir_names(input_path)
        args = ((dict_local, element) for element in dir_list) #or just pass task, because we're able to get task_list and settings_dict from init if both functions will stay here
        pool.map_async(self.execute_queue, args)
        while True:
            if len(dir_list) < folders_number:
                sleep(sleep_time)
                new_dir_list = FM.get_dir_names(input_path)
                new_dirs = [i for i in new_dir_list if i not in dir_list]
                if len(new_dirs) > 0:
                    args = ((dict_local, element) for element in new_dirs) #or just pass task, because we're able to get task_list and settings_dict from init if both functions will stay here
                    pool.map_async(self.execute_queue, args)
                    dir_list = new_dir_list
            else:
                break
        pool.close()
        pool.join()

    def execute_queue(self, args):
        dict_local, element = args
        dict_local["folder_name"] = element + "//"
        for task in self.task_list:
            task.execute(dict_local)
