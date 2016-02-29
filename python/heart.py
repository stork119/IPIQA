#! /usr/bin/python
import modules.file_managment as FM
import scripts.editdata as ED
import logging.config

import logging
import argparse
import multiprocessing
import time 
import os

class Utilities():
  
    def moving_data(self, in_path, out_path, sleep_time, file_list, que):
        for i in range(len(file_list)):
            try:
                out_path = FM.copy_data_constantly(file_list[i], out_path, sleep_time) # FM = file_managment module
                que.put(out_path)
            except IOError as e:
                print('Error: %s' % e.strerror)
        print(que.get())

    def editing_data(self):
        for i in range(3):
            out_path = "12"
            b = ED.example(out_path)
            print(b)  

def main():
"""
Logging section.
"""
    log_filename = ((time.strftime("%Y_%m_%d_")  + "_" + time.strftime("%H_%M")) ) + ".log" # setup log filename
    logging.config.fileConfig('logging.conf', defaults={'logfilename': log_filename}, disable_existing_loggers=False) #disable_existing_loggers=True, putting name of every module in logging.conf would be needed, False if we gonna make it unnecesarry
    logger = logging.getLogger(__name__)
    logger.info("Starting program...")
"""
Arg parse section.
"""
    parser = argparse.ArgumentParser( description='\n (...Example description...)' )
    parser.add_argument( '-i',
                metavar='<inputpath>', 
                type=str, 
                required=True, 
                nargs=1, 
                help='Input path' )
    parser.add_argument( '-o',
                metavar='<outputpath>', 
                type=str, 
                required=True, 
                nargs=1, 
                help='Output path' )
    parser.add_argument( '-st',
                metavar='<sleeptime>',  
                default='3', #default sleep time []
                type=int,
                nargs=1,
                help='Sleep time' )

    args = parser.parse_args()
# Program
    file_list = []
    u = Utilities()
    q = multiprocessing.Queue()
  #  m = multiprocessing.Manager()
  #  q = m.Queue()
  #  manager = Manager()
  
    p1 = multiprocessing.Process(target=u.moving_data, args=(args.i[0], args.o[0], args.st[0], file_list, q))
    p2 = multiprocessing.Process(target=u.editing_data)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
	main()
