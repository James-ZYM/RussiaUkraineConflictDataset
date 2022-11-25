import os
import pandas as pd
import csv
import re

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
            reader = csv.reader(f)
            for row in reader:
                text1 = row[14] # body
                #text2 = row[15] # body_sha_1 
                subreddit = row[41] # 40 for those where body = False
                timestamp = row[47]
                data_list = [text1, subreddit, timestamp]
                list.append(data_list)
                #list.append(text2)
        data = pd.DataFrame(list)
    return data
    