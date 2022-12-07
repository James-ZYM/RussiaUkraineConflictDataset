import os
import pandas as pd
import csv
from data import *
import pickle

# running this script took 7.65 hrs on all comments (9225973 rows) on 64 CPUs

def main():

    cwd = os.path.dirname(os.path.abspath(__file__))

    dirs_sub = [os.path.join(".." , "raw")]
    file_list_sub = get_files(current_path = cwd, data_dirs = dirs_sub)

    file_list_sub = file_list_sub[-3:-1]

    make_df(file_list_sub, save = 1)

if __name__ == "__main__":
    main()