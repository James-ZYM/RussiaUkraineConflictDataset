import os
import pandas as pd
import csv
import re
from data import *

import os
cwd = os.path.dirname(os.path.abspath(__file__))
#cwd = os.getcwd()
#print(cwd)

file_list = get_files(cwd)

file_list_sub = file_list[:3]

data = file_to_df(file_list_sub)

print(data)
