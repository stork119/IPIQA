#! /usr/bin/python
import modules.task
from multiprocessing import Pool
#from functools import partial


class QUEUE():
    
    def execute(self, element, dict_global): 
        #task_name = (type(task).__name__)
        element.task.TASK.execute(dict_global) # or executing = getattr(tk, "execute"), executing()

            
    def multiproc(self, dict_global, task_list, settings_dict):
        cores = settings_dict["number_of_cores"]
        #pool = Pool(processess = cores)
        pool = Pool(processess = 2)
        for task in task_list:
            pool.apply_async(self.execute, (task, dict_global),) #partial_execute = partial(self.execute, dict_global=dict_global), apply_async(partial_execute, task)
        pool.close()
        pool.join()
        return dict_global


