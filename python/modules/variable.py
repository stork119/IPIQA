#! /usr/bin/python
import logging, sys

logger = logging.getLogger("Variable module")

class Variable():
    def __init__(self, key, value, args = {}):
        self.key = key
        self.value = value
        self.args = args

    def get_value(self, env, args = {}):
        return self.value

    def set_value(self, value, args = {}):
        self.value = value
        return
     
    def get_variable(self, env):
        return self

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

class VariableList(Variable):
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
        return "".join(values_list)
