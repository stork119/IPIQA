#! /usr/bin/python
from collections import OrderedDict

class TASK():
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        self.parameters_by_value = parameters_by_value
        self.parameters_by_name = parameters_by_name
        self.updates_by_value = updates_by_value
        self.updates_by_name = updates_by_name
      
      
    def execute(self, dict_global):
        dict_local = dict_global.copy()
        temp_dict = dict_global.copy()
        self.update_dict(dict_local, temp_dict, self.parameters_by_value, self.parameters_by_name)
        self.execute_specify(dict_local)
        self.update_dict(dict_global, dict_local, self.updates_by_value, self.updates_by_name)
      
    def update_dict(self, dict_out, dit_in, list_by_value, list_by_name):
        for k, v in list_by_value.items(): #update by value
            dict_out[k] = v
        for k, v in list_by_name.items(): #update by name
            value = dict_in[v]
            dict_out[k] = value
        self.concatenation_name_nr(dict_out)
            
    def concatenation_name_nr(self, dict_out):      
        #concatenation name.number
        key_list = []
        for k, v in dict_out.items():
            if "." in k:
                key = k.split(".")
                key_list.append(key[0])
        if len(key_list) > 1:
            temp_dict = dict_out.copy()
            temp_dict2 = OrderedDict(sorted(dict_out.items()))
            key_list = list(set(key_list))      
            for i in range(len(key_list)):
                value = ""
                """
                robocze = 0    
                for k, v in temp_dict2.items():
                    if key_list[i] + "." in k:
                        if robocze == 0:
                            robocze = 1
                            temp_dict = OrderedDict((key_list[i],value) if key == k else (key, value) for key, value in dict_out.items())
                        else:
                            del temp_dict[k] # deleting name.number from temporary dictionary
                        value = value + v
                        temp_dict[key_list[i]] = value
                """
                for k, v in temp_dict2.items():
                    if key_list[i] + "." in k:
                        value = value + v
                        del temp_dict[k] # deleting name.number from temporary dictionary
                temp_dict[key_list[i]] = value
            dict_out = temp_dict.copy()
            
class TASK_DOWNLOAD(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def copy(self):
        print("1234")
    
    def execute_specify(self, dict_local):
        pass

class TASK_QUANTIFY(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def execute_specify(self, dict_local):
        pass
        #some specific function for this class like running cell_profiler
        
class TASK_MERGE(TASK):
  
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def execute_specify(self, dict_local):
        pass

class TASK_PARALLELIZE(TASK):
   # has got object queue
    def __init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name):
        TASK.__init__(self, parameters_by_value, parameters_by_name, updates_by_value, updates_by_name)

    def execute_specify(self, dict_local):
        pass
        #some specific function for this class like running cell_profiler
     