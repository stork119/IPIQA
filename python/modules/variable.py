#! /usr/bin/python
import logging, sys
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
        ref_value = self.get_value(env)
        var = Variable(self.key, ref_value)
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
        contains_path = False
        for key, variable in self.value.items():
            try:
                p_type = variable.get_args()["type"]
                if p_type == "path":
                    contains_path = True
            except:
                pass
        if contains_path:
            merged_value = FM.path_join(*values_list)
        else:
            merged_value = "".join(values_list)
        return merged_value

class VariableList(Variable):
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
