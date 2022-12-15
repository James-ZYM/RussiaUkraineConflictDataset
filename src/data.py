import os
import pandas as pd
import csv
import re
import fasttext
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
    for folder in data_dirs:
        folder_dirs = os.listdir(folder)
        for dir in folder_dirs:
            path1 = os.path.join(folder, dir)
            date_dirs = os.listdir(path1)
            for subdir in date_dirs:
                path = os.path.join(path1, subdir)
                files = os.listdir(path)        
                for file in files:
                    file_path = os.path.join(path, file)
                    file_list.append(file_path)
    return file_list


def make_df(file_list: list, save, ft_model) -> pd.DataFrame and list:

    start = time.time()
    
    exceptions = []
    dfs = []

    for file in file_list:
        print(file)
        try:
            split_file_name = os.path.normpath(file)
            split_file_name = split_file_name.split(os.sep)
            df_init = pd.read_csv(file)

            if split_file_name[2] == 'Comments':
                df_dict = creating_series(split_file_name[2], split_file_name, df_init, ft_model)

            elif split_file_name[2] == 'Submissions':
                df_dict = creating_series(split_file_name[2], split_file_name, df_init, ft_model)

            dfs.append(pd.DataFrame(df_dict))
            
        except pd.errors.EmptyDataError:
            exceptions.append(file)
            pass
    
    #final_df = pd.concat(dfs, ignore_index=False)
    final_df = pd.concat(dfs, ignore_index=True)
    final_df = final_df.drop(final_df[final_df.document == "[removed]"].index)
    final_df = final_df.drop(final_df[final_df.document == "[deleted]"].index)
    final_df = final_df.drop(final_df[final_df.document == "author_premium"].index)
    final_df['document'] = final_df['document'].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)

    final_df.dropna(inplace=True)
    
    if save: 
        outfile_csv = os.path.join("..", "data", "test_df.csv")
        outfile_pickle = os.path.join("..", "data", "test_df.pkl")
        final_df.to_csv(outfile_csv) 
        final_df.to_pickle(outfile_pickle)

        outfile_txt = os.path.join("..", "data", "exception_files_test_df.txt")
        with open(outfile_txt, "w") as f:
            for path in exceptions:
                # write each item on a new line
                f.write("%s\n" % path)

    end = time.time()
    print(f"Data preprocessing took: {(end-start)/60} mins")

    return final_df

def creating_series(document_type: str, split_name: list, df_init: pd.DataFrame, ft_model):

    if document_type == 'Submissions':
        type_string = 'submission'
        doc_col = 'title'

    elif document_type == 'Comments':
        type_string = 'comment'
        doc_col = 'body'

    documents = df_init[doc_col].rename(type_string)
    doc_type =  pd.Series([type_string] * len(documents))
    sub_reddit = pd.Series([split_name[4].split('.')[0]] * len(documents), name = 'sub_reddit') # change index
    date = pd.Series([split_name[3].split('.')[0]] * len(documents), name = 'date') # change index
    language, confidence = detect_language(documents, ft_model)
    df_dict = {'document':documents, 'sub_reddit': sub_reddit, 'date': date, 'type' : doc_type, 'language': language, 'confidence': confidence}
    
    return df_dict

def detect_language(documents: pd.Series, ft_model):
    ft_language = []
    confidence = []
    for doc in documents:
        try:
            doc = re.sub(r'\n', ' ', doc)
        except:
            pass
        try:
            predictions = ft_model.predict(doc)
            lang = re.sub(r'__label__', '', predictions[0][0])
            conf = predictions[1][0]
        except:
            lang = "none"
            #conf = Nan

        ft_language.append(lang)
        confidence.append(conf)
        
    ft_language = pd.Series(ft_language, name = 'ft_language')
    confidence = pd.Series(confidence, name = 'confidence')
    
    return ft_language, confidence    


def file_to_df(file_list: list) -> pd.DataFrame and list:

    """
        Args:
        file_list (list): list of strings containing all file names with their path

    Returns:
        pd.DataFrame: 
        list: list of lists with filenames of the files that did not read into the pd.DataFrame and the corresponding error.
    """
    list_file = []
    i = 0
    exceptions = []
    for file in file_list:
        i += 1 
        try:
            # open file and append a list of two text columns, the subreddit column, the post type and the date to list
            with open(file, 'r') as f:
                split_file_name = os.path.normpath(file)
                split_file_name.split(os.sep)
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
                    list_file.append(data_list)
                # some print to see progress
                if subreddit == "war":
                    print(f'Finished processing file number {i} of {len(file_list)}!')
                    print(f'So far I have identified {len(exceptions)} exception files.', '\n')
        # if file is unable to read append it to list of exceptions
        except Exception as e: exceptions.append([file, str(e)])
    
    # create pd.DataFrame
    data = pd.DataFrame(list_file)
        # rename columns
    data.columns = ["body", "body_sha1", "subreddit", "post_type", "date"]
        # temp data to be able to merge the two text columns
    temp_data = data.loc[(data['body'] == "True") | (data['body'] == "False")]
    temp_data = temp_data.drop(columns = "body")
    temp_data = temp_data.rename(columns = {'body_sha1':'body'})
    data = data.drop(columns="body_sha1")
    final_data = pd.concat([temp_data, data])
        # remove duplicate rows (from entries where text was in body_sha1)
    final_data['index1'] = final_data.index
    final_data = final_data.drop_duplicates(subset='index1')
    
    # detect language of comment
        # record start time
    start = time.time()
    i = 0
    print("Beginning language detection...", "\n")
    final_data['language'] = pd.Series(dtype='str')
    for row in range(len(final_data)):
        i += 1
        try:
            final_data.iloc[row, 5] = detect(final_data.iloc[row, 0])
        except: 
            final_data.iloc[row, 5] = "none"
        if i % 100000 == 0: 
            print(f'Finished detecting language in {i} out of {len(final_data)} cases!')
        # record end time
    end = time.time()
 
    # print the difference between start and end time in secs
    print(f"The time of execution of the language detection was : {(end-start)/60} mins")
    
    # drop rows where comment has been removed and NAs
    final_data = final_data.drop(final_data[final_data.body == "[removed]"].index)
    final_data = final_data.drop(final_data[final_data.body == "author_premium"].index)
    final_data.dropna()

    return final_data, exceptions