import os
import pandas as pd
import csv
import re
from langdetect import detect

def get_files():
    data_dirs = [os.path.join(".." , "Comments"), os.path.join(".." ,"Submissions")]
    file_list = []
    for dir in data_dirs:
        date_dirs = os.listdir(dir)
        
        for subdir in date_dirs:
            path = os.path.join(dir, subdir)
            files = os.listdir(path)
            
            for file in files:
                file_path = os.path.join(path, file)
                file_list.append(file_path)
    return file_list

def file_to_df(file_list):
    list = []
    for file in file_list:
        with open(file, 'r') as f:
        split_file_name = file.split("/")
        r = split_file_name[3].split(".")
        reader = csv.reader(f)
        for row in reader:
            text1 = row[14] # body
            text2 = row[15] # body_sha_1
            subreddit = r[0]
            post_type = split_file_name[1]
            date = split_file_name[2]
            data_list = [text1, text2, subreddit, post_type, date]
                list.append(data_list)
        data = pd.DataFrame(list)
    return data