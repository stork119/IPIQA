#! /usr/bin/python
import getdata 
import editdata

import logging
import argparse
from multiprocessing import Process, Queue

def main():
# Logs settings (+ example log)
    logging.basicConfig(level=logging.DEBUG, 
			filename="logfile", 
			format="%(asctime)-15s %(levelname)-8s %(message)s")
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

    GD = getdata.GetData()
    ED = editdata.EditData() 
    out_path = GD.get_file(args.i[0], args.o[0], args.st[0]) #checking out if the file exist and copy it -> working for file, not working for directory (not yet!)
    b = ED.example(out_path)
    print(b)
        



"""

"""

if __name__ == "__main__":
	main()
