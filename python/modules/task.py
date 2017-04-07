#! /usr/bin/python
from collections import OrderedDict
import modules.variable as VAR
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

    dict_task = {}

    def __init__(self, parameters, updates, args = {}):
        self.parameters = parameters
        self.updates = updates
        #self.logger = logging.getLogger(self.__class__.__name__) - doesn't work with parallelize

    def execute(self, env_global):
        env_local = env_global.copy()
        logger.debug("env_local before update: %s", env_local.keys())
        env_local = self.update_env(env_local, env_global, self.parameters)
        logger.debug("env_local after update: %s", env_local.keys())
        logger.info("Executing: %s", self.__class__.__name__) #information what task is being executed
        dict_setts = self.parse_task_arguments(env_local)
        self.execute_specify(env_local, dict_setts)
        logger.debug("env_local after execute_specify: %s", env_local.keys()) #dunno if its needed
        logger.debug("env_global before update: %s", env_global.keys())
        env_global = self.update_env(env_global, env_local, self.updates)
        logger.debug("env_global after update: %s", env_global.keys())
        return env_global

    def parse_task_arguments(self, env_local):
        dict_setts = {}
        for key in self.dict_task:
            try: 
                var = env_local[key]
                value = var.get_value(env_local)
            except:
                try:
                    value = self.dict_task[key]["default"]
                except:
                    if self.dict_task[key]["required"]:
                        logger.error("Required parameter %s is missing for %s.", key, str(self.__class__.__name__))
                        exit()
            dict_setts[key] = value
        return dict_setts

    def update_env(self, dict_out, dict_in, variables):
        for key, variab in variables.items():
            var_out = variab.get_variable(dict_in)
            dict_out[key] = var_out       
        return dict_out

    def convert_to_var_dict(self, dict_in):
        """
        Converts all dictionary's values to the corresponding variable objects:
        i.e. in_dict = {"input_path" : "C:/path/to/file"} ---> 
             out_dict = {"input_path" : Variable("input_path", "C:/path/to/file")}
        """
        dict_out = {}
        for key, value in dict_in.items():
            variable = VAR.Variable(key, dict_in[key])
            dict_out[key] = variable
        return dict_out

class TASK_FOR(TASK):

    dict_task = {}

    def __init__(self, parameters, updates, args):
        TASK.__init__(self, parameters, updates, args)
        self.variables_sets_list = args['variables_list']
        self.task_to_do = args['task_to_do']
        
    def execute_specify(self, env_local, dict_setts):
        env_tmp = env_local.copy()
        for variables_set in self.variables_sets_list:
            env_local_for = self.update_env(env_local, env_tmp, variables_set)
            self.task_to_do.execute(env_local_for)

class TASK_QUEUE(TASK):
 
    dict_task = {}
 
    def __init__(self, parameters, updates, args):
        TASK.__init__(self, parameters, updates, args)
        self.task_list = args['task_list']

    def execute_specify(self, env_local, dict_setts):
        for task in self.task_list:
            env_local = task.execute(env_local)

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
    dict_task = {}

    def __init__(self, parameters, updates, args):
        TASK.__init__(self, parameters, updates, args)
        self.task_list = args['task_list']

    def execute_specify(self, env_local, dict_setts):
        arg1 = env_local["argument_1"] #[!] code need to be change to allow parsing both args from mp_dict
        comparison = env_local["comparison"].lower() 
        try:
            arg2 = env_local["argument_2"]
            if FC.compare_args(arg1, arg2, comparison) == True:
                self._execute_queue(env_local)
            return
        except:
            pass
        try:
            mp_name = env_local["mp_dict"]
        except:
            mp_name = "map_plate"
        try:
            mp_dict = env_local[mp_name]
            mp_well = env_local["mp_well"]
            mp_param = env_local["mp_param"]
            arg2 = mp_dict[mp_well][mp_param]
        except:
            logger.error("Cannot get value from map_plate for given " 
            "dictionary, well and parameter: %s, %s, %s", mp_name, mp_well, mp_param)
            return
        if FC.compare_args(arg1, arg2, comparison) == True:
            self._execute_queue(env_local)
        return

    def _execute_queue(self, env_local):
        for task in self.task_list:
            task.execute(env_local)

class TASK_CHECK_COMPLETNESS(TASK): # [!] not supported

    dict_task = {"experiment_finished" : {"required" : True, "default" : True},
                 "input_path" : {"required" : True}, 
                 "required_files" : {"requred" : False},
                 "sleep_time" : {"requred" : True}}
    # [!] class requires changes after merge with branch map_plate

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
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

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        logger.info("TASK_DOWNLOAD from input: %s to output :%s", dict_setts["input_path"], dict_setts["output_path"]) 
        FM.dir_copy(dict_setts["input_path"], dict_setts["output_path"])


class TASK_REMOVE(TASK):

    dict_task = {"input_path" : {"required" : True}}

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        FM.dir_remove(dict_setts["input_path"])

   
class TASK_QUANTIFY(TASK):

    dict_task = {"cp_path" : {"required" : True},
                 "input_path" : {"required" : True},
                 "output_path" : {"required" : True},
                 "pipeline" : {"required" : True}}

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        cpm.run_cp_by_cmd(dict_setts["cp_path"], dict_setts["input_path"], 
                          dict_setts["output_path"], dict_setts["pipeline"])
   
class TASK_MERGE_SUBDIR_CSV(TASK):
 
    dict_task = {"input_path" : {"required" : True},
                 "output_path" : {"required" : True},
                 "csv_names_list" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","},
                 "column_name" : {"required" : True, "default" : "well.name"}}
 
    def __init__(self, parameters, updates, args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        csv_names = (dict_setts["csv_names_list"]).split(",")
        main_subdir_list = FM.dir_get_paths(dict_setts["input_path"])
        for csv_name in csv_names:
            subdir_list = CSV_M.filter_subdir_list(main_subdir_list, csv_name) #filtering directiories containing given csv file
            data = CSV_M.merge_subdir_csv(csv_name, subdir_list, dict_setts["delimiter"], dict_setts["column_name"])
            extension = FM.file_get_extension(csv_name)
            len_ext = len(extension)
            name = csv_name[:-(len_ext)]
            """
            #Saving data in environment:
            v_out = VAR.Variable(name, data)
            env_local[name] = v_our
            """
            #Saving data
            out_path = FM.path_join(dict_setts["output_path"], csv_name)
            if FM.path_check_existence(out_path):
                logger.warning("File %s already exists. Removing old data.", out_path)
                FM.dir_remove(out_path)
            CSV_M.write_csv(out_path, dict_setts["delimiter"], data)


class TASK_PARALLELIZE(TASK):

    dict_task = {"input_path" : {"required" : True},
                 "number_of_cores" : {"required" : True, "default" : "1"}, 
                 "sleep_time" : {"required" : True}}
    # [!] number_of_cores is temporary coded as string
    # [!] class requires changes after merge with branch map_plate

    def __init__(self, parameters, updates, args):
        TASK.__init__(self, parameters, updates, args)
        self.task_list = args['task_list']
        self.config_dict = args['config_dict']

    def execute_specify(self, env_local, dict_setts):
        elements_list, ele_number = self.parse_elements_list(env_local, dict_setts)
        processes_number = int(dict_setts["number_of_cores"])
        sleep_time = int(dict_setts["sleep_time"])
        new_elements = elements_list
        pool = multiprocessing.Pool(processes_number)
        while True:
            if len(new_elements) > 0:
                args = ((env_local, element) for element in new_elements) #or just pass task, because we're able to get task_list and settings_dict from init if both functions will stay here
                pool.map_async(self._execute_queue, args)
            if len(elements_list) >= ele_number:
                break
            sleep(sleep_time)
            new_elements_list = self.parse_elements_list(env_local, dict_setts)[0] # in MP case (ONLY) we could just call _create_ele_lis; TO DO
            new_elements = [i for i in new_elements_list if i not in elements_list]
            elements_list = new_elements_list
        pool.close()
        pool.join()

    def _execute_queue(self, args):
        env_local, elements = args
        env_local.update(elements)
        for task in self.task_list:
            task.execute(env_local)

class TASK_PARALLELIZE_MP(TASK_PARALLELIZE): #all objects (folders) for given map_plate setup
    """
    Required args:
    - input_path [path to directories on which parallelize taks would be performed]
    [+ arguments for super class TASK_PARALLELIZE: number_of_cores, sleep_time]

    Optional args:
    - used_value [value defying if given dir name reflects well tag or id, by default 'tag']
    - prefix [subdir name prefixes]
                (i.e. 'Well ' for 'Well A0', where 'A01' is well tag)
    - sufix [subdir name sufixes]
    - exp_part [experiment part, by default '1']
    - mp_name [name of structure with all collected map_plate info, 
                by default 'map_plate']
    """
    
    dict_task = {"input_path" : {"required" : True},
                 "number_of_cores" : {"required" : True, "default" : "1"}, 
                 "sleep_time" : {"required" : True},
                 "used_value" : {"required" : True, "default" : "tag"},
                 "prefix" : {"required" : True, "default" : ""},
                 "sufix" : {"required" : True, "default" : ""},
                 "exp_part" : {"required" : True, "default" : "1"},
                 "mp_name" : {"required" : True, "default" : "map_plate"}}
    # [!] number_of_cores is temporary coded as string

    def __init__(self, parameters, updates, args):
        TASK_PARALLELIZE.__init__(self, parameters, updates, args)
        self.config_dict = args['config_dict']

    def parse_elements_list(self, env_local, dict_setts): #implementing with tag
        v_mp_dict = env_local[dict_setts["mp_name"]]
        mp_dict = v_mp_dict.get_value(env_local)
        active_wells_keys = FC.get_active_wells(mp_dict, dict_setts["exp_part"]) #get active wells keys for mp_dict 
        ele_number = len(active_wells_keys)
        params = FC.get_wells_base_params(mp_dict, active_wells_keys, dict_setts["prefix"], dict_setts["sufix"], dict_setts["exp_part"])
        elements_list = FC.create_elements_list(dict_setts["input_path"], params, dict_setts["used_value"])
        var_elements_list = []
        for element in elements_list:
            var_element = self.convert_to_var_dict(element)
            var_elements_list.append(var_element)
        return var_elements_list, ele_number

class TASK_PARALLELIZE_LIST(TASK_PARALLELIZE): # list of objects (folders) # [!] NOT SUPPORTED

    dict_task = {"input_path" : {"required" : True},
                 "number_of_cores" : {"required" : True, "default" : "1"}, 
                 "sleep_time" : {"required" : True},
                 "folders_list" : {"required" : True}}
    # [!] number_of_cores is temporary coded as string

    def __init__(self, parameters, updates, args):
        TASK_PARALLELIZE.__init__(self, parameters, updates, args)

    def parse_elements_list(self, env_local, dict_setts):
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
    
    def __init__(self, parameters, updates, args):
        TASK_PARALLELIZE.__init__(self, parameters, updates, args)
        self.config_dict = args['config_dict']

    def parse_elements_list(self, env_local, dict_setts):
        folders_number = int(dict_setts["folders_number"])
        dir_list = FM.dir_get_names(dict_setts["input_path"])
        var_dir_list = []
        for dir_name in dir_list:
            variable = VAR.Variable("folder_name", dir_name)
            var_dir_list.append({"folder_name" : variable})
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
    dict_task = {"input_path" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","}, 
                 "mp_name" : {"required" : True, "default" : "map_plate"}}

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        mp_out = map_plate.parse_mp(dict_setts["input_path"], dict_setts["delimiter"])
        mp_name = dict_setts["mp_name"]
        v_mp_out = VAR.Variable(mp_name, mp_out)
        env_local[mp_name] = v_mp_out

class TASK_APPLY_MAP_PLATE(TASK):
    """
    Required args:
    - input_path [path to input csv files]
    - output_path [path to output files]
    - csv_names_list [list of files to apply map_plate]
    - mp_key [well id/key to all well parameters in map_plate structure]
    
    Optional args:
    - delimiter [delimiter used in csv files, by default ',']
    - mp_name [name of dicitonary with all collected map_plate info, 
                by default 'map_plate']
    """
    dict_task = {"input_path" : {"required" : True},
                 "output_path" : {"required" : True}, 
                 "csv_names_list" : {"required" : True}, 
                 "mp_key" : {"required" : True}, 
                 "delimiter" : {"required" : True, "default" : ","}, 
                 "mp_name" : {"required" : True, "default" : "map_plate"}}

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        csv_names = (dict_setts["csv_names_list"]).split(",")
        v_mp_dict = env_local[dict_setts["mp_name"]]
        mp_dict = v_mp_dict.get_value(env_local)
        map_plate.apply_mp(dict_setts["input_path"], dict_setts["output_path"], dict_setts["delimiter"], mp_dict, csv_names, dict_setts["mp_key"])

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

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        input_path_csv = env_local["input_path_csv"]
        input_path_metadata = env_local["input_path_metadata"]
        output_path = env_local["output_path"]
        csv_names = (env_local["csv_names_list"]).split(",")
        try:
            exp_id = env_local["exp_id"]
        except:
            exp_id = 1
        try:
            delimiter_csv = env_local["delimiter_csv"]
        except:
            delimiter_csv = ","
        try:
            delimiter_mp = env_local["delimiter_mp"]
        except:
            delimiter_mp = "\t"
        try:
            exp_part_id = env_local["exp_part"]
            exp_parts = env_local["exp_parts"]
        except:
            exp_part_id = "1" 
            exp_parts = "1"
        map_plate.combine(input_path_csv, input_path_metadata, output_path, csv_names, exp_id, exp_part_id, exp_parts, delimiter_mp, delimiter_csv)

class TASK_R(TASK):

    dict_task = {"r_function_name" : {"required" : True},
                 "r_script_path" : {"required" : True}}

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        external_params = list(self.dict_task.keys())
        logger.info("Executing R function %s from %s", dict_setts["r_function_name"], dict_setts["r_script_path"]) 
        # PLACEHOLDER for adding more external params
        param_dict = R_connection.prepare_param_dict(env_local, self.parameters_by_value, self.parameters_by_name, external_params)
        output_dict = R_connection.execute_r_script(param_dict, dict_setts["r_script_path"], dict_setts["r_function_name"])
        out_var_dict = self.convert_to_var_dict(output_dict)
        env_local.update(out_var_dict)
        
class TASK_FFC_CREATE(TASK):

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        # Check if user set input an output paths
        output_dict = ffc.create_camcor(env_local, self.parameters_by_value, self.parameters_by_name)
        out_var_dict = self.convert_to_var_dict(output_dict)
        env_local.update(out_var_dict)

class TASK_FFC_READ(TASK):

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        # Check if user set input an output paths
        try:
            output_dict = ffc.read_camcor(env_local, self.parameters_by_value, self.parameters_by_name)
        except:
            output_dict = ffc.create_camcor(env_local, self.parameters_by_value, self.parameters_by_name)
        out_var_dict = self.convert_to_var_dict(output_dict)
        env_local.update(out_var_dict)

class TASK_FFC_APPLY(TASK):

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        # Check if user set input an output paths
        output_dict = ffc.apply_camcor(env_local, self.parameters_by_value, self.parameters_by_name)
        out_var_dict = self.convert_to_var_dict(output_dict)
        env_local.update(out_var_dict)
   
   
class TASK_FFC_READ_APPLY(TASK):
 
    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        # Check if user set input an output paths
        output_dict = ffc.read_apply_camcor(env_local, self.parameters_by_value, self.parameters_by_name)
        out_var_dict = self.convert_to_var_dict(output_dict)
        env_local.update(out_var_dict)
        
class TASK_READ_DATAFRAME_FROM_CSV(TASK):

    dict_task = {"input_path" : {"required" : True},
                 "filename" : {"required" : True},
                 "dict_key_name" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","}}

    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        input_path = FM.path_join(dict_setts["input_path"], dict_setts["filename"])
        data = R_connection.read_dataframe_from_csv(input_path, dict_setts["delimiter"])
        dict_key = dict_setts["dict_key_name"]
        v_data = VAR.Variable(dict_key, data)
        env_local[dict_key] = v_data

class TASK_WRITE_DATAFRAME_TO_CSV(TASK):

    dict_task = {"output_path" : {"required" : True},
                 "filename" : {"required" : True},
                 "dict_key_name" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","}}
    
    def __init__(self, parameters, updates,  args = {}):
        TASK.__init__(self, parameters, updates, args)

    def execute_specify(self, env_local, dict_setts):
        output_path = FM.path_join(dict_setts["output_path"], dict_setts["filename"])
        v_data = env_local[dict_setts["dict_key_name"]]
        data = v_data.get_value(env_local)
        R_connection.write_dataframe_to_csv(output_path, data, dict_setts["delimiter"])

class TASK_MERGE_CSV(TASK):

    dict_task = {"input_path_1" : {"required" : True},
                 "input_path_1" : {"required" : True},
                 "csv_names_list" : {"required" : True},
                 "output_path" : {"required" : True},
                 "delimiter" : {"required" : True, "default" : ","}}

    def __init__(self, parameters, updates, args = {}):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name, args)

    def execute_specify(self, env_local, dict_setts):
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
