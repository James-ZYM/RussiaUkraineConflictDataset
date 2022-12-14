
import os
import pandas as pd
import csv
from data import *
import pickle

# running this script took 7.65 hrs on all comments (9225973 rows) on 64 CPUs
cwd = os.path.dirname(os.path.abspath(__file__))

dirs = [os.path.join(".." , "raw")]
file_list = get_files(current_path = cwd, data_dirs = dirs)

file_list_sub_com = []
file_list_sub_sub = []

substring = "Comments"
for file in file_list:
    if substring in file:

        file_list_sub_com.append(file)
print('number of comment csv-files:' + str(len(file_list_sub_com)))

substring2 = "Submissions"

for file2 in file_list:
    if substring2 in file2:

        file_list_sub_sub.append(file2)
print('number of submission csv-files:' + str(len(file_list_sub_sub)))

'''
for file in file_list_sub:
    print(file)
    try:
        split_file_name = os.path.normpath(file)
        split_file_name = split_file_name.split(os.sep)
        df_init = pd.read_csv(file)

        if split_file_name[2] == 'Comments':
            if df_init['body'].empty == True:
                print('This is empty:' + file)
        
    except pd.errors.EmptyDataError:
        pass
'''


