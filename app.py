# dependencies
import pandas as pd
import re
import os
import json
from pprint import pprint
from functools import reduce
import requests
from dotenv import load_dotenv

# TODO
# make frontend
# deploy app

# load environment variables
load_dotenv()

# regex to parse time format
time_pattern = re.compile(".*T([0-9]{2}):([0-9]{2}):([0-9]{2}).*")

# key for machine ids for time per machine
machine_ids = {
    # ifl machines
    "Lathe": "16",
    "TRAK Mill": "17",
    "Vertical Bandsaw": "20",
    "Horizontal Bandsaw": "21",
    "Belt Sander": "22",
    "Drill Press": "23",
    "Ironworker": "24",
    "Sandblaster": "25",
    "Powder Coater": "26",
    "Okuma (CNC Mill)": "28",
    "Waterjet": "31",

    # rpl machines
    "Nanoscribe": "1",
    "VR3200": "29",
    "Sapphire 3D Kiln": "30",

    # rpc machines
    "Prusa i3 MK3": "2",
    "Zortrax M200 Plus": "3",
    "Raise 3D Pro2 Plus": "4",
    "Fuse 1": "5",
    "Epilog": "6",
    "Wazer": "7",
    "Romer Arm": "8",
    "Form 3": "9",
    "Oscilloscope": "10",
    "Hakko Solder Station": "11",
    "Prusa i3 MK3.9": "12",
    "Form 3 (clear)": "13",
    "Prusa MK4": "14",
    "Nexa3D": "15",
    
    # id 32 ??
}

# http nemo request parameters
base_url = "https://nemo.tw.umd.edu/api/reservations/"
headers = {
    "Content-Type": "application/json",
    "Authorization": os.getenv('NEMO_token')
}

# get http response
response = requests.get(base_url, headers=headers).json()
df = pd.DataFrame(response)
    
# find start and end times in seconds from timestamps, calculate their differential (length)
times = zip(df['start'].tolist(), df['end'].tolist())
differentials = []

for (start, end) in times:
    # match the time
    start_match = re.fullmatch(pattern=time_pattern, string=start)
    end_match = re.fullmatch(pattern=time_pattern, string=end)
    
    # get time in seconds
    start_t = int(start_match.group(1))*3600 + int(start_match.group(2))*60 + int(start_match.group(3))
    end_t = int(end_match.group(1))*3600 + int(end_match.group(2))*60 + int(end_match.group(3))
    
    # convert the different to hours, round to 2 digits after the decimal
    differential = round(number=(end_t - start_t) / 3600, ndigits=2)
    
    # append to list
    differentials.append(differential)

# insert list into dataframe as new column
df['differentials'] = differentials

# time per machine section
timedict = {}

for row in df.itertuples():
    if row.tool in timedict:
        timedict[int(row.tool)] += row.differentials
    else:
        timedict[int(row.tool)] = row.differentials

tpm = []
        
for machine in machine_ids.keys():
    id = int(machine_ids[machine])        
    if id in timedict:
        tpm.append((machine, round(timedict[id], 2)))
    else:
        tpm.append((machine, 0))

pprint(f"reservation time per machine (<machine>, <hours>): {tpm}")
print(f"total reservation time (hours): {round(reduce(lambda x, y: x + y, timedict.values()), 2)}")
print(f"total number of reservations: {df.index.__len__()}")