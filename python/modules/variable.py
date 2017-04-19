#! /usr/bin/python
import logging, sys
import copy
import modules.file_managment as FM

logger = logging.getLogger("Variable module")

class Variable():
    """
    Parameters without type are represented in  xml settings
    as following:
    <parameter key = <KEY> value = <VALUE>/>
    
    i.e.
    <parameter key = "filename_1" value = "input_file_1"/>
    """
    def __init__(self, key, value, args = {}):
        self.key = key
        self.value = value
        self.args = args

    def get_value(self, env, args = {}):
        return self.value

    def get_variable(self, env):
        return self

    def set_value(self, value, args = {}):
        self.value = value
        return

    def get_args(self):
        return self.args

    def create_dict(self, env):
        return {self.key : self.get_variable(env)}

class VariablePath(Variable):
    """
    Parameters with type 'path' are represented in  xml settings
    as following:
    <parameter key = <KEY> value = <VALUE> type = "path" />
    
    i.e.
    <parameter key = "path21" value = "C://input_file_1" type = "ref"/>
    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})
        self.value = FM.path_unify(value)


class VariableReference(Variable):
    """
    Parameters with type 'reference' are represented in  xml settings
    as following:
    <parameter key = <KEY> value = <VALUE> type = "ref" />
    
    i.e.
    <parameter key = "input_path" value = "path21" type = "ref"/>
    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_ref_key(self):
        return self.value

    def get_variable(self, env):
        # creates variable with reference value
        var = copy.deepcopy(env[self.value])
        return var

    def get_value(self, env, args = {}):
        return env[self.value].get_value(env, args)

class VariableParted(Variable):
    """
    Parameters with type 'part' are represented in  xml settings
    as following:
    <parameter key = <KEY> value = <VALUE> type = <TYPE> part = <PART>/>
    
    i.e.
    <parameter key = "input_path" value = "C://" type = "path" part = "1"/>
    <parameter key = "input_path" value = "filename_1" type = "ref" part = "2"/>
    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def _check_paths_presence(self, var_dict):
        """
        Verifies if there is any path in Variable's parts.
        """
        for key, variable in var_dict.items():
            if isinstance(variable, VariablePath):
                return True
        return False

    def get_value(self, env, args = {}):
        return self._get_converted_value(env, args = {})[0]

    def get_variable(self, env):
        # creates variable with merged value
        merged_value, contains_path = self._get_converted_value(env)
        if contains_path:
            var = VariablePath(self.key, merged_value)
        else:
            var = Variable(self.key, merged_value)
        return var

    def _get_converted_value(self, env, args = {}):
        """
        Gets converted value (depending on paths presence).
        Returns converted value and boolean 
        (contains_path = True/False).
        """
        order = sorted(self.value.keys())
        values_list = []
        for key in order:
            v_part = self.value[key].get_value(env)
            values_list.append(str(v_part))
        contains_path = self._check_paths_presence(self.value)
        if contains_path:
            merged_value = FM.path_join(*values_list)
        else:
            merged_value = "".join(values_list)  
        logger.debug("Merged variable %s: %s", self.key, merged_value)
        return merged_value, contains_path

class VariableList(Variable):
    """
    Parameters with type 'list' are represented in  xml settings
    as following:
    <parameter key = <KEY> type = "list">
        <parameter value = <VALUE> type = <TYPE> />
        <parameter value = <VALUE> type = <TYPE> />
    </parameter>
    
    i.e.
    <parameter key = "csv_data" type = "list">
        <parameter value = "Nuclei.csv">
        <parameter value = "ShrinkedNuclei.csv">
    </parameter>
    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_variable(self, env):
        converted_list = []
        raw_list = self.value
        for var in raw_list:
            new_var = var.get_variable(env)
            converted_list.append(new_var)
        variable = VariableList(self.key, converted_list)
        return variable
        
    def get_value(self, env, args = {}):
        out_list = []
        for element in self.value:
            out_list.append(element.get_value(env))
        return out_list
      
    def get_raw_value(self):
        return self.value

class VariableStructure(Variable):
    """
    Variable structure (list of dictionaries)
    presents as following example:
        structure = [{<param_key> : Variable,
                            <param_key2> : Variable2},
                     {<param_key> : Variable,
                            <param_key2> : Variable2},
                            <...> }, 
        where each list item represents set of parameters from xml.

    Parameters with type 'structure' are represented in  xml settings
    as following:
    <parameter key = <KEY> type = "structure">
            <parameter key = <KEY> value = <VALUE> type = <TYPE>/>
            <parameter key = <KEY> value = <VALUE> type = <TYPE>/>
    <parameter>
    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_variable(self, env):
        converted_dict = {}
        raw_dict = self.value
        for key, var in raw_dict.items():
            converted_dict[key] = var.get_variable(env)
        variable = VariableStructure(self.key, converted_dict)
        return variable
        
    def get_value(self, env, args = {}):
        converted_dict = {}
        for key, variable in values_set.items():
            converted_dict[key] = variable.get_value(env)
        return converted_dict

    def create_dict(self, env):
        return self

class VariableMP(Variable):
    """
    VariableMP might represent
    a) whole map_plate, where
        value =  map_plate structure
    b) single map_plate element (i.e. well), where
        value = map_plate name (containing given map_plate element)

    a) 
    Map_plate structure (dictionary of ordered dictionaries)
    presents as following example:
        map_plate = { 'A01' : OrderedDict([('id', 'A01'),
                                        ('exp_part', '1'),
                                        ('name', 'A01'),
                                        <...>]),
                     'B01' : OrderedDict([('id', 'B01'),
                                        ('exp_part', '2'),
                                        ('name', 'A01'),
                                        <...>]),
                    <...> },
        where:
        map_plate.keys()- experimental wells
        mp_plate[well_id]- dicionary of all experimental settings
                            for given well

    VariableMP representing whole map_plate is created during 
    TASK_READ_MAP_PLATE.
    
    Variable can be refered in  xml settings
    as following:
    <parameter key = <KEY> value = <MP_NAME> type = "ref">

    b)
    Parameters with type 'map_plate', referring to chosen map_plate element
    are represented in  xml settings as following example:
    <parameter key = <KEY> value/mp_name = <MP_NAME> type = "map_plate">
        <parameter key = "well" value = "mp_key" type = "ref">
        <parameter key = "param" value = "stimulation.1.1">
    </parameter>
    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})
        self.mp_dict = value
        
    def get_mp_dict(self):
        return self.mp_dict

    def get_value(self, env):
        args_keys = (self.args).keys()
        if "well" in args_keys:
            well = self.args["well"].get_value(env)
            try:
                self.mp_dict = env[self.value].get_mp_dict()
            except:
                logger.error("Following map_plate: %s is missing in environment."
                             "Can't assign map_plate element %s", 
                             self.value, self.key)
            if "param" in args_keys:
                param = self.args["param"].get_value(env)
                return self.get_param_value(well, param)
            else:
                return self.get_well_params(well)
        else:
            return self

    def get_variable(self, env):
        args_keys = (self.args).keys()
        if any(i in args_keys for i in ["well", "param"]):
            var = Variable(self.key, self.get_value(env))
            return var
        else:
            return self

    def get_wells_ids(self):
        return list(self.mp_dict.keys())

    def get_param_value(self, well_name, param):
        """
        Gets value for a given well and parameter.
        Returns string.
        """
        value = self.mp_dict[well_name][param]
        return value

    def get_param_values(self, param):
        """
        Gets all values for a given param 
        from map_plate dictionary.
        Returns list.
        """
        values = []
        for well in self.mp_dict:
            values.append(self.mp_dict[well][param])
        return values

    def get_param_unique_values(self, param): 
        """
        Gets all unique values for a given param 
        from map_plate dictionary.
        Returns list.
        """
        values = get_param_values(self.mp_dict, param)
        unique = list(set(values))
        return unique

    def get_params_names(self):
        """
        Gets all key names from map_plate dictionary.
        Returns list.
        """
        names = []
        key_0 = list(self.mp_dict.keys())[0]
        names = list(self.mp_dict[key_0].keys()) 
        #if we assume that number of information between wells is constant
        return names

    def get_well_params(self, well):
        """ 
        Gives all parameters values for a given well.
        Returns list.
        """
        values = []
        for param in self.mp_dict[well]:
            values.append(self.mp_dict[well][param])
        return values

