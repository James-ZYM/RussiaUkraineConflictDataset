import os
import pandas as pd
import csv
import re
from data import *

file_list = get_files()

file_list_sub = file_list[:3]

data = file_to_df(file_list_sub)

