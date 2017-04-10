#! /usr/bin/python
import logging, sys
import copy
import modules.file_managment as FM

logger = logging.getLogger("Variable module")

class Variable():
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

class VariableReference(Variable):
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
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_variable(self, env):
        # creates variable with merged value
        merged_value = self.get_value(env)
        var = Variable(self.key, merged_value)
        return var

    def get_value(self, env, args = {}):
        order = sorted(self.value.keys())
        values_list = []
        for key in order:
            v_part = self.value[key].get_value(env)
            values_list.append(v_part)
        merged_value = "".join(values_list)
        logger.debug("Merged variable %s: %s", self.key, merged_value)
        return merged_value

class VariableList(Variable):
    """
    Parameters with type 'list' are represented in  xml settings
    as following:
    <parameter key = "<KEY>" type = "list">
        <parameter value = "<VALUE>" type = "<TYPE>">
        <parameter value = "<VALUE>" type = "<TYPE>">
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
        converted_list = self.get_value(env)
        var = Variable(self.key, converted_list)
        return var
        
    def get_value(self, env, args = {}):
        out_list = []
        for element in self.value:
            out_list.append(element.get_value(env))
        return out_list

class VariableMP(Variable):
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_variable(self, env):
        pass

    def get_value(self, env, args = {}):
        pass

    def get_param_value(mp_dict, well_name, param):
        """
        Gets values for a given well and parameter.
        """
        value = mp_dict[well_name][param]
        return value

    def get_param_values(mp_dict, param):
        """
        Gets all values for a given param 
        from map_plate dictionary.
        """
        values = []
        for well in mp_dict:
            values.append(mp_dict[well][param])
        return values

    def get_param_unique_values(mp_dict, param): 
        """
        Gets all unique values for a given param 
        from map_plate dictionary.
        """
        values = get_param_values(mp_dict, param)
        unique = list(set(values))
        return unique

    def get_params_names(mp_dict): # get all key names from map_plate dictionary
        names = []
        key_0 = list(mp_dict.keys())[0]
        names = list(mp_dict[key_0].keys()) 
        #if we assume that number of information between wells is constant
        return names

    def get_well_params(mp_dict, well):
        """ 
        Gives all parameters values for a given well
        """
        values = []
        for param in mp_dict[well]:
            values.append(mp_dict[well][param])
        return values
