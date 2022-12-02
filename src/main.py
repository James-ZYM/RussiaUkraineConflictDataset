import os
import pandas as pd
import csv
from data import *


cwd = os.path.dirname(os.path.abspath(__file__))

dirs = [os.path.join(".." , "Comments")]
file_list = get_files(current_path = cwd, data_dirs = dirs)

file_list_sub = file_list[:10]

data, exception_files = file_to_df(file_list_sub)

os.makedirs('../data', exist_ok=True) 
data.to_csv('../data/formatted_data.csv') 
exception_files.to_csv('../data/exception_files.csv')


outfile = os.path.join("..", "data", "exception_files.txt")
with open(outfile, "w") as f:
    for item in exception_files:
        # write each item on a new line
        f.write("%s\n" % item)