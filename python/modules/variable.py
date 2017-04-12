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
    <parameter key = "<KEY>" type = "structure">
            <parameter key = "<KEY>" value = "<VALUE>" type = "<TYPE>">
            <parameter key = "<KEY>" value = "<VALUE>" type = "<TYPE>">
    <parameter>
    """
    def __init__(self, key, value, args = {}):
        Variable.__init__(self, key, value, args = {})

    def get_variable(self, env):
        converted_dict = self.get_value(env)
        var = Variable(self.key, converted_dict)
        return var
        
    def get_value(self, env, args = {}):
        converted_dict = {}
        for key, variable in values_set.items():
            converted_dict[key] = variable.get_value(env)
        return converted_dict

