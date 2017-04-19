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

class VariablePath(Variable):
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})
        self.value = FM.path_unify(value)

class VariableParted(Variable):
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
            values_list.append(v_part)
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
