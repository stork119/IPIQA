#! /usr/bin/python
from collections import OrderedDict
import modules.file_managment as FM
import modules.flow_control as FC
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

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args = {}):
        self.parameters_by_value = parameters_by_value
        self.parameters_by_name = parameters_by_name
        self.updates_by_value = updates_by_value
        self.updates_by_name = updates_by_name
        #self.logger = logging.getLogger(self.__class__.__name__) - doesn't work with parallelize

    def execute(self, dict_global):
        dict_local = dict_global.copy()
        logger.debug("dict_local before update: %s", (dict_local.keys()))
        dict_local = self.update_dict(dict_local, dict_local, self.parameters_by_value, self.parameters_by_name) #check out if its working 
        logger.debug("dict_local after update: %s", dict_local.keys())
        logger.info("Executing: %s", self.__class__.__name__) #information what task is being executed
        self.execute_specify(dict_local)
        logger.debug("dict_local after execute_specify: %s", dict_local.keys()) #dunno if its needed
        logger.debug("dict_global before update: %s", dict_global.keys())
        dict_global = self.update_dict(dict_global, dict_local, self.updates_by_value, self.updates_by_name)
        logger.debug("dict_global after update: %s", dict_global.keys())
        return dict_global

    def update_dict(self, dict_out, dict_in, list_by_value, list_by_name):
        for k, v in list_by_value.items(): #update by value
            dict_out[k] = v
            logger.debug("Dict_out new key, value (updated by value): %s, %s", k, v)
        for k, v in list_by_name.items(): #update by name
            logger.debug("Dict_in (by names) key, value: %s, %s", k, v)
            try:
                value = dict_in[v]
            except:
                logger.error("Dictionary update_by_name error. Given key (%s) doesn't exist in dictionary", v)
            dict_out[k] = value
            logger.debug("Dict_out new key, value (updated by name): %s, %s", k, value)
        logger.debug("Dict_out before concatenation: %s", dict_out.keys())
        try:
            dict_out = self.concatenation_name_nr(dict_out)
        except:
            logger.error("Dictionary concatenation error. Dictionary: %s concatenation failed.", dict_out)
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
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.variables_list = args['variables_list']
        self.task_do = args['task_do']
        
    def execute_specify(self, dict_local):
        for variable in self.variables_list:
            dict_local_for = self.update_dict(dict_local, dict_local, variable['parameters_by_value'], variable['parameters_by_name'])
            self.task_do.execute(dict_local_for)

class TASK_QUEUE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.task_list = args['task_list']

    def execute_specify(self, dict_local):
        for task in self.task_list:
            dict_local = task.execute(dict_local)

class TASK_IF(TASK):
    """
    Required args:
    - argument_1 [first argument to compare (from local_dict)]
    - comparison [type of comparison i.e. "equal" or "<"]

    Optional args
    - <arg2>, which can be parsed as:
        1) - argument_2 [second argument to compare (from local_dict)]
        2) <value from map_plate> which requires:
            - mp_dict [map_plate disctionary name (default: map_plate)]
            - mp_well [well id, i.e. 'A01']
            - mp_param [param name i.e. 'exp_part']
    """
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.task_list = args['task_list']

def execute_specify(self, dict_local):
    arg1 = dict_local["argument_1"] #[!] code need to be change to allow parsing both args from mp_dict
    comparison = dict_local["comparison"].lower() 
    try:
        arg2 = dict_local["argument_2"]
        if FC.compare_args(arg1, arg2, comparison) == True:
            self._execute_queue(dict_local)
        return
    except:
        pass
    try:
        mp_dict = dict_local["mp_dict"]
    except:
        mp_dict = "map_plate"
    try:
        mp_well = dict_local["mp_well"]
        mp_param = dict_local["mp_param"]
        arg2 = mp_dict[mp_well][mp_param]
    except:
        logger.error("Cannot get value from map_pate for given " 
        "dictionary, well and parameter.")
        return
    if FC.compare_args(arg1, arg2, comparison) == True:
        self._execute_queue(dict_local)
    return

    def _execute_queue(self, dict_local):
        for task in self.task_list:
            task.execute(dict_local)

class TASK_CHECK_COMPLETNESS(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        in_path = dict_local["input_path"]
        try:
            job_done = str(dict_local["experiment_finished"])
            job_done = job_done.lower()
            if job_done == "no" or "0" or "false":
                required_files = (dict_local["required_files"]).split(",")
                sleep_time = dict_local["sleep_time"]
                FM.dir_check_completeness(in_path, required_files, sleep_time)
        except:
            pass

class TASK_DOWNLOAD(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        in_path = dict_local["input_path"]
        out_path = dict_local["output_path"]
        logger.info("TASK_DOWNLOAD from input: %s to output :%s", in_path, out_path) 
        FM.dir_copy(in_path, out_path)


class TASK_REMOVE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        in_path = dict_local["input_path"]
        FM.dir_remove(in_path)

   
class TASK_QUANTIFY(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        cp_path = dict_local["cp_path"]
        in_path = dict_local["input_path"]
        out_path = dict_local["output_path"]
        pipeline = dict_local["pipeline"]
        #cpm.check_pipeline(pipeline)
        cpm.run_cp_by_cmd(cp_path, in_path, out_path, pipeline)
   
class TASK_MERGE_SUBDIR_CSV(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        in_path = dict_local["input_path"]
        output_path = dict_local["output_path"]
        main_subdir_list = FM.dir_get_paths(in_path)
        csv_names = (dict_local["csv_names_list"]).split(",")
        try:
            delimiter = dict_local["delimiter"]
        except:
            delimiter = "," #choose separator
        for csv_name in csv_names:
            subdir_list = CSV_M.filter_subdir_list(main_subdir_list, csv_name) #filtering directiories containing given csv file
            data = CSV_M.merge_subdir_csv(csv_name, subdir_list)
            extension = FM.file_get_extension(csv_name)
            len_ext = len(extension)
            name = csv_name[:-(len_ext)]
            dict_local[name] = data
            #Saving data
            out_path = FM.path_join(output_path, csv_name)
            if FM.path_check_existence(out_path):
                logger.warning("File %s already exists. Removing old data.", out_path)
                FM.dir_remove(out_path)
            CSV_M.write_csv(out_path, delimiter, data) #if we would like to write_csv somewhere...


class TASK_PARALLELIZE(TASK):

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.task_list = args['task_list']
        self.config_dict = args['config_dict']

    def execute_specify(self, dict_local):
        elements_list, ele_number = self.parsing_elements_list(dict_local)
        processes_number = int(dict_local["number_of_cores"])
        sleep_time = int(dict_local["sleep_time"])
        new_elements = elements_list
        pool = multiprocessing.Pool(processes_number)
        while True:
            if len(new_elements) > 0:
                args = ((dict_local, element) for element in new_elements) #or just pass task, because we're able to get task_list and settings_dict from init if both functions will stay here
                pool.map_async(self._execute_queue, args)
            if len(elements_list) >= ele_number:
                break
            sleep(sleep_time)
            new_elements_list = self.parsing_elements_list(dict_local)[0] # in MP case (ONLY) we could just call _create_ele_lis; TO DO
            new_elements = [i for i in new_elements_list if i not in elements_list]
            elements_list = new_elements_list
        pool.close()
        pool.join()

    def _execute_queue(self, args):
        dict_local, elements = args
        dict_local.update(elements)
        for task in self.task_list:
            task.execute(dict_local)

class TASK_PARALLELIZE_MP(TASK_PARALLELIZE): #all objects (folders) for given map_plate setup
    """
    [!] TO DO - Add comments
    """
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.config_dict = args['config_dict']

    def parsing_elements_list(self, dict_local): #implementing with tag
        input_path = str(dict_local["input_path"])
        try:
            used_value = dict_local["used_value"]
        except:
            used_value = "tag" 
        try:
            prefix = dict_local["prefix"]
        except:
            prefix = ""
        try:
            sufix = dict_local["sufix"]
        except:
            sufix = ""
        try:
            exp_part = dict_local["exp_part"]
        except:
            exp_part = "1"
        try:
            mp_name = dict_local["mp_name"]
        except:
            mp_name = "map_plate"
        mp_dict = dict_local[mp_name]
        active_wells_keys = FC.get_active_wells(mp_dict, exp_part) #get active wells keys for mp_dict 
        ele_number = len(active_wells_keys)
        params = FC.get_wells_base_params(mp_dict, active_wells_keys, prefix, sufix, exp_part)
        elements_list = FC.create_ele_list(input_path, params, used_value)
        return elements_list, ele_number

class TASK_PARALLELIZE_LIST(TASK_PARALLELIZE): # list of objects (folders) # [!] NOT SUPPORTED

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def parsing_elements_list(self, dict_local):
        paths = []
        input_path = str(dict_local["input_path"])
        folder_list = (dict_local["folders_list"]).split(",")
        for folder in folder_list:
            path = FM.path_join(input_path, folder)
            paths.append(path)
        folders_number = len(paths)
        return paths, folders_number


class TASK_PARALLELIZE_PATH(TASK_PARALLELIZE): #all objects (folders) in given directory (path)

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.config_dict = args['config_dict']

    def parsing_elements_list(self, dict_local):
        folders_number = int(dict_local["folders_number"])
        dir_names = FM.dir_get_names(input_path)
        dir_list = [{"folder_name" : i} for i in dir_names]
        return dir_list, folders_number

class TASK_SYNCHRONOUSLY(TASK):

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.task_list = args['task_list']
        self.config_dict = args['config_dict']

    def execute_specify(self, dict_local):
        dir_list, folders_number = self.parsing_elements_list(dict_local)
        processes_number = int(dict_local["number_of_cores"])
        sleep_time = int(dict_local["sleep_time"])
        new_dirs = dir_list
        while True:
            if len(new_dirs) > 0:
                for element in new_dirs:
                    args = (dict_local, element)
                    self._execute_queue(args)
            if len(dir_list) >= folders_number:
                break
            sleep(sleep_time)
            input_path = str(dict_local["input_path"])
            new_dir_list = FM.dir_get_names(input_path)
            new_dirs = [i for i in new_dir_list if i not in dir_list]
            dir_list = new_dir_list

    def _execute_queue(self, args):
        dict_local, element = args
        dict_local["folder_name"] = element
        for task in self.task_list:
            task.execute(dict_local)

   
class TASK_SYNCHRONOUSLY_LIST(TASK_SYNCHRONOUSLY): # list of objects (folders)

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def parsing_elements_list(self, dict_local):
        paths = []
        input_path = str(dict_local["input_path"])
        folder_list = (dict_local["folders_list"]).split(",")
        for folder in folder_list:
            path = FM.path_join(input_path, folder)
            paths.append(path)
        folders_number = len(paths)
        return paths, folders_number


class TASK_SYNCHRONOUSLY_PATH(TASK_SYNCHRONOUSLY): #all objects (folders) in given directory (path)

    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)
        self.config_dict = args['config_dict']

    def parsing_elements_list(self, dict_local):
        folders_number = int(dict_local["folders_number"])
        input_path = str(dict_local["input_path"])
        dir_list = FM.dir_get_names(input_path)
        return dir_list, folders_number

class TASK_READ_MAP_PLATE(TASK):
    """
    Required args:
    - input_path [path to map_plate csv files]

    Optional args:
    - delimiter [delimiter used in map_plate csv, by default ',']
    - mp_name [name for map_plate output 
            (variable assigned to dictionary containing all experiment settings), 
            by default 'map_plate']
    """
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        input_path = dict_local["input_path"]
        try:
            delimiter = dict_local["delimiter"]
        except:
            delimiter = ","
        try:
            mp_name = dict_local["mp_name"]
        except:
            mp_name = "map_plate"
        dict_local[mp_name] = map_plate.parse_mp(input_path, delimiter)

class TASK_APPLY_MAP_PLATE(TASK):
    """
    Required args:
    - input_path [path to input csv files]
    - output_path [path to output files]
    - csv_names_list [list of files to apply map_plate]
    
    Optional args:
    - delimiter [delimiter used in csv files, by default ',']
    - mp_name [name of dicitonary with all collected map_plate info, 
                by default 'map_plate']
    """
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        input_path = dict_local["input_path"]
        output_path = dict_local["output_path"]
        csv_names = (dict_local["csv_names_list"]).split(",")
        try:
            delimiter = dict_local["delimiter"]
        except:
            delimiter = ","
        try:
            mp_name = dict_local["mp_name"]
        except:
            mp_name = "map_plate"
        mp_dict = dict_local[mp_name]
        compare_column = "well.name" # temporary hardcoded [to discuss name and form]
        map_plate.apply_mp(input_path, output_path, delimiter, mp_dict, csv_names, compare_column)


class TASK_MAP_PLATE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
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
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        r_function_name = dict_local["r_function_name"]
        r_script_path = dict_local["r_script_path"]
        external_params = ["r_function_name", "r_script_path"]
        logger.info("Executing R function %s from %s", r_function_name, r_script_path) 
        # PLACEHOLDER for adding more external params
        param_dict = R_connection.prepare_param_dict(dict_local, self.parameters_by_value, self.parameters_by_name, external_params)
        output_dict = R_connection.execute_r_script(param_dict, r_script_path, r_function_name)
        dict_local.update(output_dict)
        
class TASK_FFC_CREATE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        # Check if user set input an output paths
        output_dict = ffc.create_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)

class TASK_FFC_READ(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        # Check if user set input an output paths
        try:
            output_dict = ffc.read_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        except:
            output_dict = ffc.create_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)

class TASK_FFC_APPLY(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        # Check if user set input an output paths
        output_dict = ffc.apply_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)
   
   
class TASK_FFC_READ_APPLY(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        # Check if user set input an output paths
        output_dict = ffc.read_apply_camcor(dict_local, self.parameters_by_value, self.parameters_by_name)
        dict_local.update(output_dict)
        
class TASK_READ_DATAFRAME_FROM_CSV(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        path = dict_local["input_path"]
        filename = dict_local["filename"]
        input_path = FM.path_join(path, filename)
        dict_key_name = dict_local["dict_key_name"]
        try:
            delimiter = dict_local["delimiter"]
        except:
            delimiter = ","
        data = R_connection.read_dataframe_from_csv(input_path, delimiter)
        dict_local[dict_key_name] = data

class TASK_WRITE_DATAFRAME_TO_CSV(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name,  args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        path = dict_local["output_path"]
        filename = dict_local["filename"]
        output_path = FM.path_join(path, filename)
        dict_key_name = dict_local["dict_key_name"]
        data = dict_local[dict_key_name]
        try:
            delimiter = dict_local["delimiter"]
        except:
            delimiter = ","
        R_connection.write_dataframe_to_csv(output_path, data, delimiter)

class TASK_MERGE_CSV(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        in_path_list = []
        in_path_list.append(dict_local["input_path_1"])
        in_path_list.append(dict_local["input_path_2"])
        csv_names = (dict_local["csv_names_list"]).split(",")
        output_path = dict_local["output_path"]
        try:
            delimiter = dict_local["delimiter"]
        except:
            delimiter = "," #choose separator
        for csv_name in csv_names:
            data = CSV_M.simple_merge(csv_name, in_path_list, delimiter)
            #Saving data
            out_path = FM.path_join(output_path, csv_name)
            if FM.path_check_existence(out_path):
                logger.warning("File %s already exists. Removing old data.", out_path)
                FM.dir_remove(out_path)
            CSV_M.write_csv(out_path, delimiter, data) #if we would like to write_csv somewhere...
            # PLACEHOLDER adding data to dictionary 

class TASK_COPY_CSV(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, dict_local):
        in_path_list = []
        in_path_list.append(dict_local["input_path"])
        csv_names = (dict_local["csv_names_list"]).split(",")
        output_path = dict_local["output_path"]
        try:
            delimiter = dict_local["delimiter"]
        except:
            delimiter = "," #choose separator
        for csv_name in csv_names:
            data = CSV_M.simple_merge(csv_name, in_path_list, delimiter)
            #Saving data
            out_path = FM.path_join(output_path, csv_name)
            if FM.path_check_existence(out_path):
                logger.warning("File %s already exists. Removing old data.", out_path)
                FM.dir_remove(out_path)
            CSV_M.write_csv(out_path, delimiter, data) #if we would like to write_csv somewhere...
            # PLACEHOLDER adding data to dictionary 
