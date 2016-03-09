#! /usr/bin/python

class QUEUE():
    
    def execute(self, dict_global, task_list): # task_list passing by _init_ or function argument?
        for task in task_list:
            task.TASK.execute(dict_global)
