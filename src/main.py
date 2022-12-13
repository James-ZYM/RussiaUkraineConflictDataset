import os
import pandas as pd
import csv
from data import *
import pickle

# running this script took 7.65 hrs on all comments (9225973 rows) on 64 CPUs

def main():

    cwd = os.path.dirname(os.path.abspath(__file__))

    dirs = [os.path.join(".." , "raw")]
    file_list = get_files(current_path = cwd, data_dirs = dirs)

    #file_list = file_list[:50] + file_list[1320:1370]
    #file_list = file_list[1320:1322]

    make_df(file_list, save = 1)

if __name__ == "__main__":
    main()