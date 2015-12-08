#! /usr/bin/python
import scripts.file_managment as FM
import scripts.editdata as ED

import logging
import argparse
import multiprocessing
import time 
import os

class Utilities():
  
    def moving_data(self, in_path, out_path, sleep_time, file_list, que):
        for i in range(len(file_list)):
            try:
                out_path = FM.copy_data_const(file_list[i], out_path, sleep_time) # FM = file_managment module
                que.put(out_path)
            except IOError as e:
                print('Error: %s' % e.strerror)
        print(que.get())

    def editing_data(self):
        for i in range(3):
            out_path = "12"
            b = ED.example(out_path)
            print(b)  
            
    def create_logfile(self, log_filename):
        output_path = os.path.dirname(os.path.realpath(__file__)) + "/logs/" + log_filename
        FM.copy_data("logfile_temp", output_path)

def main():
  
    log_filename = ((time.strftime("%Y_%m_%d_")  + "_" + time.strftime("%H_%M")) ) + ".log" # setup log filename
# Logs settings (+ example log)
    logging.basicConfig(level=logging.DEBUG, 
		    filename="logfile_temp", 
		    format="%(asctime)-2s \t %(levelname)-4s \t %(message)s") #logs' settings
    logging.info("Starting program...")

#Arg parse section
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
		default='3', #default sleep time [stop working somehow]
                type=int,
                nargs=1,
		help='Sleep time' )

    args = parser.parse_args()
# Program 
    file_list = ["123.txt", "12.txt", "proba.txt"]
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
    u.create_logfile(log_filename) # creating final logfile placeholder



if __name__ == "__main__":
	main()
