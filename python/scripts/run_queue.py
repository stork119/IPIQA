#! /usr/bin/python
#import modules.task
import multiprocessing
from time import sleep


class QUEUE():
    
    def execute(self, args):
        settings_dict, dict_global, element = args 
        #task_name = (type(task).__name__)
        #element.task.TASK.execute(dict_global) # or executing = getattr(tk, "execute"), executing()
        for i in range(2):
            print(element)
            sleep(.5)
            
    def multiproc(self, dict_global, task_list, settings_dict):
        pass
      
def main():
    
    settings_dict = {"number_of_cores":"2", "zaza":"123"}
    number_processes = int(settings_dict["number_of_cores"])
    print(number_processes)
    dict_global = {}
    task_list = ["1", "2", "3", "4", "5"]
    Q = QUEUE()
    pool = multiprocessing.Pool(number_processes)
    print("inizjalizacja")
    args = ((settings_dict, dict_global, task) for task in task_list)
    results = pool.map_async(Q.execute, args)
    pool.close()
    pool.join()
    print("koniec")
    
#cd Documents/GitHub/PathwayPackage/python/modules
if __name__ == "__main__":
    main()
