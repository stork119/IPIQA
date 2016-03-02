#! /usr/bin/python
import collections

class TASK():
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        self.parameters_by_value = parameters_by_value
        self.parameters_by_name = parameters_by_name
        self.updates_by_value = updates_by_value
        self.updates_by_name = updates_by_name
      
      
    def execute(self, dict_global):
        dict_local = dict_global.copy()
        dict_local = dict(self.update_dict(dict_local, dict_local, self.parameters_by_value, self.parameters_by_name))
        #sth
        #execute_specific(dict_local)
        dict_global = dict(self.update_dict(dict_global, dict_local, self.updates_by_value, self.updates_by_name))
        return dict_global
      
    def update_dict(self, dict_out, dit_in, list_by_value, list_by_name):
        for i in (list_by_value): #update by value
            dict_out[i] = dict_in[i]
        for i in (list_by_name)): #update by name
            v = dict_in[i]
            dict_out[i] = dict_in[v]
        #concatenation name.number
        key_list = []
        temp_dict = dict(dict_out)
            for k, v in dict_out.items():
            if "." in k:
                key = k.split(".")
                key_list.append(key[0])
        key_list = list(set(key_list))      
        for i in range(len(key_list)):
            value = ""
            for k, v in dict_out.items():
                if key_list[i] + "." in k:
                    value = value + v
                    del temp_dict[k] # deleting name.number from temporary dictionary
                temp_dict[key_list[i]] = value # the more 'proper' way to do this would be put this phrase out of 'if' condition (to do not assign the value for the key few times), but in that case we would lose the order of dictionary
        dict_out = dict(temp_dict) 
        print(dict_out)
        return dict_out


    
"""
dict_global = collections.OrderedDict()
dict_global = {}
dict_global = collections.OrderedDict(sorted(dict_global.items()))
"""