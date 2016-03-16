#! /usr/bin/python
import os

def get_dir_names(input_path):
   # subdir_path = []
    subdir_name = []
    for path, subdir, files in os.walk(input_path):
        for name in subdir:
       #     subdir_path.append(os.path.join(path, name)) # get list of path to each subdir
            subdir_name.append(str(name))
    return subdir_name
    
def merge(csv_name, subdir_list, input_path, output_path):
    out_file= open((os.path.join(output_path, csv_name)) ,"a")
    # first file:
    num = 0
    position = subdir_list[0].split()
    position = position[1]
    for line in open((os.path.join(input_path, subdir_list[0], csv_name))):
        if num == 0:
            out_file.write(line.rstrip() + "," + "PositionName" + "\n")
            num = 1
        else:
            out_file.write(line.rstrip() + "," + position + "\n")
    # rest files:
    for subdir in (subdir_list[1:]):
        position = subdir.split()
        position = position[1]
        f = open((os.path.join(input_path, subdir, csv_name)), "r")
        # skip the header
        first_line = f.readline() # first line is header, it is called to put it out of set
        for line in f:
            out_file.write(line.rstrip() + "," + position + "\n")
        f.close()
    out_file.close()
    

def main():

    input_path = ""
    output_path = ""
    csv_names = ['Cells.csv', 'Cytoplasm.csv', 'ExpandedNucleiLess.csv', 'ExpandedNucleiMore.csv', 'Image.csv', 'Nuclei.csv', 'RingCytoplasm.csv', 'ShrinkedNuclei.csv']
    #'Experiment.csv' was not icluded in 'csv_names' list of files, because of different structure
    subdir_list = get_dir_names(input_path)
    for csv_name in csv_names:
        merge(csv_name, subdir_list, input_path, output_path)
       
    

if __name__ == "__main__":
    main()
 