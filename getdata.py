#! /usr/bin/python
import os.path
import time
import logging
import shutil # for function copy_data

class GetData():

    logging.basicConfig(level=logging.DEBUG, filename="logfile", format="%(asctime)-15s %(levelname)-8s %(message)s") #logs' settings

    def get_file(self, in_path, out_path, sleep_time):
        while True:
            if (os.path.exists((in_path))) == True: # Checking out if the director and file exist ["C:/path/to/file"]
                self.copy_data((in_path), out_path)
                return out_path
                break
            else:
                print("File not found.")
                time.sleep(sleep_time)

    def copy_data(self, in_path, out_path):
        try:
            shutil.copy(in_path, out_path)
        except shutil.Error as e: #same path
            logging.error(e)
        except IOError as e:
            print('Error: %s' % e.strerror)
            logging.error(e)


