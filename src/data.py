import os
import pandas as pd
import csv
import re
from langdetect import detect
import time

def get_files(current_path: str, data_dirs: list) -> list:
    """This functions takes the current path and the data directories and returns a list of all filenames.

    Args:
        current_path (str): path of current file location (main)
        data_dirs (list): a list of directories in which to find files (here either Comments, Submissions, or both)

    Returns:
        list: list containing all the file names with their path as strings.
        Example of list element: 'Comments/2022-03-23/RussiaUkraineWar2022.csv'
    """
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

def file_to_df(file_list: list) -> pd.DataFrame and list:
    list = []
    i = 0
    exceptions = []
    for file in file_list:
        i += 1 
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
                    data_list = [text1, text2, subreddit, post_type, date]
                    list.append(data_list)
                if subreddit == "war":
                    print(f'Finished processing file number {i} of {len(file_list)}!')
                    print(f'So far I have identified {len(exceptions)} exception files.', '\n')
        except Exception as e: exceptions.append([file, str(e)])
    data = pd.DataFrame(list)
    data.columns = ["body", "body_sha1", "subreddit", "post_type", "date"]
    temp_data = data.loc[(data['body'] == "True") | (data['body'] == "False")]
    temp_data = temp_data.drop(columns = "body")
    temp_data = temp_data.rename(columns = {'body_sha1':'body'})
    data = data.drop(columns="body_sha1")
    final_data = pd.concat([temp_data, data])
    final_data['index1'] = final_data.index
    final_data = final_data.drop_duplicates(subset='index1')
    
    # detect language of comment
    
    # record start time
    start = time.time()
    print("Almost finished. I just need to detect the languages in your dataset. This should take a good while, so this is a good time to get up and stretch your legs.", "\n", "For reference, this process took ~3 minutes running 10 files on 8 CPUs.")
    final_data['language'] = pd.Series(dtype='str')
    for row in range(len(final_data)):
        try:
            final_data.iloc[row, 5] = detect(final_data.iloc[row, 0])
        except: 
            final_data.iloc[row, 5] = "none"
    # record end time
    end = time.time()
 
    # print the difference between start and end time in milli. secs
    print(f"The time of execution of the language detection was : {end-start} s")
    
    # drop rows where comment has been removed and NAs
    final_data = final_data.drop(final_data[final_data.body == "[removed]"].index)
    final_data = final_data.drop(final_data[final_data.body == "author_premium"].index)
    final_data.dropna()

    return final_data, exceptions