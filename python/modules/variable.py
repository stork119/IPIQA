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
    """
    VariableMP might represent
    a) whole map_plate, where
        value =  map_plate structure
    b) single map_plate element (i.e. well), where
        value = map_plate name

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

    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})
        self.mp_dict = value
        
    def get_mp_dict(self):
        return self.mp_dict

        print('Python version does not meet software requirments. '
        'Install python 3.5 or 3.6 to run IPIQA.')

    def get_value(self, env):
        args_keys = (self.args).keys()
        if "well" in args_keys:
            try:
                self.mp_dict = env[self.value].get_mp_dict()
            except:
                logger.error("Following map_plate: %s is missing in environment."
                             "Can't assign map_plate element %s", 
                             self.value, self.key)
            if "param" in args_keys:
                return self.get_param_value(self.args["well"], self.args["param"])
            else:
                return self.get_well_params(self.args["well"])
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
        """
        value = self.mp_dict[well_name][param]
        return value

    def get_param_values(self, param):
        """
        Gets all values for a given param 
        from map_plate dictionary.
        """
        values = []
        for well in self.mp_dict:
            values.append(self.mp_dict[well][param])
        return values

    def get_param_unique_values(self, param): 
        """
        Gets all unique values for a given param 
        from map_plate dictionary.
        """
        values = get_param_values(self.mp_dict, param)
        unique = list(set(values))
        return unique

    def get_params_names(self): # get all key names from map_plate dictionary
        names = []
        key_0 = list(self.mp_dict.keys())[0]
        names = list(self.mp_dict[key_0].keys()) 
        #if we assume that number of information between wells is constant
        return names

    def get_well_params(self, well):
        """ 
        Gives all parameters values for a given well
        """
        values = []
        for param in self.mp_dict[well]:
            values.append(self.mp_dict[well][param])
        return values
