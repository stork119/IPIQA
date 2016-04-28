#! /usr/bin/python

class TASK():
    def __init__(self, parameters_by_value, args = {}):
        self.parameters_by_value = parameters_by_value

class TASK_PARALLELIZE(TASK):
   # has got object queue
    def __init__(self, parameters_by_value, args):
        TASK.__init__(self, parameters_by_value, args)
        self.task_list = args['task_list']
        self.config_dict = args['config_dict']

    def execute_specify(self, dict_local):
        print("TASK PARALLELIZE MAIN")
        self.specify_specify()
            
class TASK_PARALLELIZE_LIST(TASK_PARALLELIZE):
   # has got object queue
    def __init__(self, parameters_by_value, args):
        TASK_PARALLELIZE.__init__(self, parameters_by_value, args)
    
    def specify_specify(self):
        print("1234")
value = {}
args = {"task_list":"ugabuga", "config_dict":"zaraza"}
dict_local = {}
a = TASK_PARALLELIZE_LIST(value, args)
a.execute_specify(dict_local)