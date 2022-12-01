import os
import pandas as pd
import csv
import re
from langdetect import detect

def get_files(current_path, data_dirs: list):
    os.chdir(current_path)
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
    exceptions = []
    for file in file_list:
        try:
            with open(file, 'r') as f:
                split_file_name = file.split("/")
                r = split_file_name[3].split(".")
                reader = csv.reader(f)
                for row in reader:
                    if row == 0:
                        pass
                    else:
                        text1 = row[14] # body
                        text2 = row[15] # body_sha_1
                        subreddit = r[0]
                        post_type = split_file_name[1]
                        date = split_file_name[2]
                        try:
                            language = detect(text1)
                        except:                                              
                            language = "none"
                    data_list = [text1, text2, subreddit, post_type, date, language]
                    list.append(data_list)
        except Exception as e: exceptions.append((file, str(e)))
    data = pd.DataFrame(list)
    data.columns = ["body", "body_sha1", "subreddit", "post_type", "date", "language"]
    temp_data = data.loc[(data['body'] == "True") | (data['body'] == "False")]
    temp_data = temp_data.drop(columns = "body")
    temp_data = temp_data.rename(columns = {'body_sha1':'body'})
    data = data.drop(columns="body_sha1")
    final_data = pd.concat([temp_data, data])
    final_data['index1'] = final_data.index
    final_data = final_data.drop_duplicates(subset='index1')
 

    return final_data, exceptions