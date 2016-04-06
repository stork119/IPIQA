#! /usr/bin/python
import os.path
import os, stat
from time import sleep
import shutil # for function copy_data
"""
Checking out if the director and file exist ["C:/path/to/file"].
"""
def if_exist(path):
    if (os.path.exists(path)):
        return True
    print("%s path doesn't exist.", path)
    return False
"""
Getting all subdirs names of a given directory.
"""
def get_dir_names(input_path):
    if not if_exist(input_path):
        print("Error. Can't get subdirs names list for a given path: %s.", input_path)
        return False
   # subdir_path = []
    subdir_names = []
    for path, subdir, files in os.walk(input_path):
        for name in subdir:
       #     subdir_path.append(os.path.join(path, name)) # get list of path to each subdir
            subdir_names.append(str(name))
    return subdir_names
    
    
def get_filepaths(input_path):
    if not if_exist(input_path):
        print("Error. Can't get subfiles names list for a given path: %s.", input_path)
        return False
   # subdir_path = []
    subfile_names = []
    for path, subdir, files in os.walk(input_path):
        for name in files:
       #     subdir_path.append(os.path.join(path, name)) # get list of path to each subdir
            subfile_names.append(os.path.join(path, name))
    return subfile_names
"""
Functions for coping objects.
"""
def copy_directory_constantly(in_path, out_path, sleep_time):
    while True:
        if os.path.exists(in_path):
            copy_directory(in_path, out_path)
            return
        else:
            sleep(sleep_time)
    
  
def copy_directory(in_path, out_path):
    dir_name = (in_path.split("/"))[-1]
    copied_dir_path = out_path + dir_name
    print(copied_dir_path)
    if not os.path.exists(copied_dir_path):
        os.makedirs(copied_dir_path)
    else:
        print("Directory already exists.")
        #return
    files_paths_list = get_filepaths(in_path)
    print(files_paths_list)
    for f in files_paths_list:
        copy_data(f, copied_dir_path)
  
def copy_data(in_path, out_path):
    if if_exist(in_path):
        try:
            shutil.copy(in_path, out_path)
            return out_path
        except shutil.Error as e: #same path
            print(e)
        except IOError as e:
            print('Error: %s' % e.strerror)
    else:
        print("Object \"" + in_path + "\" not found.")
        
def copytree2(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def copy_data_constantly(in_path, out_path, sleep_time): #sleep_time is given in seconds and it's meant to be higher than 0.
    while True:
        if if_exist(in_path):
            try:
                shutil.copy(in_path, out_path)
                return out_path
            except shutil.Error as e: #same path
                print(e)
            except IOError as e:
                print('Error: %s' % e.strerror)
        else:
            print("Object \"" + in_path + "\" have not been found yet. Searching will be continued.")
            sleep(sleep_time)
