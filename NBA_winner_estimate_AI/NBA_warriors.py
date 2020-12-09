#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:11:29 2020

@author: yokoishusei
"""
#import time
#from selenium import webdriver
import pandas as pd 
from sklearn.linear_model import LogisticRegression
from pathlib import Path
#import numpy as np
#from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import log_loss, roc_curve, auc
pd.set_option('display.max_rows', None)
pd.options.display.max_columns
pd.options.display.max_rows


years = ["2016", "2017", "2018", "2019", "2020"]
months = ["october","november","december","january","february", "march", "april", "may", "june"]

file_dir = Path(f'/Users/yokoishusei/Library/Mobile Documents/com~apple~CloudDocs/Desktop/My_intern/NBA_winner_estimate_AI/NBA_data')
lis_dfs = []
for file in file_dir.glob("*.csv"):
    if file.name[0:4] == "2015":
        continue
    df = pd.read_csv(file)
    lis_dfs.append(df)
# rename columns
df = pd.concat(lis_dfs).rename(columns={'Date': 'Date_origin', 'Unnamed: 6': 'Box Score', 'Unnamed: 7': 'OT', 'Visitor/Neutral': "Visitor", "Home/Neutral": "Home"}).reset_index(drop=True).drop('Notes', axis = 1)


# remove rows
f_bool = lambda x: x[0:3] not in ["Dat", "Pla"]
df = df[df["Date_origin"].map(f_bool)].dropna(subset=['PTS', 'PTS.1'])

# add new columns
df["Day_of_Week"] = [d[0:3] for d in df["Date_origin"]]
df["Month"] = [d[5:8] for d in df["Date_origin"]]
df["Date"] = pd.to_datetime(df["Date_origin"], format='%a, %b %d, %Y')
#df["Home*Visiter"] = df["Home"] * df["Visitor"]

# convert column types
df = df.astype({'PTS': 'int64', 'PTS.1': 'int64', 'Attend.': 'int64'})

#extract Warrors' games
df_w = df[df['Visitor'] == "Golden State Warriors"] 
df = df_w.append(df[df['Home'] == "Golden State Warriors"]).reset_index(drop = True)

# create dummy variables
df = pd.get_dummies(df, columns=["Day_of_Week"], sparse=True, drop_first=True)
df = pd.get_dummies(df, columns=["Month"], sparse=True, drop_first=True)
df = pd.get_dummies(df, columns=["Visitor"], sparse=True, drop_first=True)
df = pd.get_dummies(df, columns=["Home"], sparse=True, drop_first=True)

# add target
win = df["PTS.1"] - df["PTS"]
df["Win"] = [1 if d > 0 else 0 for d in win]

train_df = df[df["Date"] < "2019-10-01"]
valid_df = df[df["Date"] >= "2019-10-01"]


lis = ['Date_origin', 'Start (ET)', 'PTS', 'PTS.1', 'Box Score', 'OT',
       'Attend.', 'Date', 'Day_of_Week_Mon', 'Day_of_Week_Sat',
       'Day_of_Week_Sun', 'Day_of_Week_Thu', 'Day_of_Week_Tue',
       'Day_of_Week_Wed', 'Month_Dec', 'Month_Feb', 'Month_Jan', 'Month_Jun',
       'Month_Mar', 'Month_May', 'Month_Nov', 'Month_Oct', 'Win']



train_x = train_df.drop(lis, axis = 1)
valid_x = valid_df.drop(lis, axis = 1)

train_y = train_df["Win"]
valid_y = valid_df["Win"]


lr = LogisticRegression()
lr.fit(train_x, train_y)
valid_df["res"] = lr.predict(valid_x)
res_proba = lr.predict_proba(valid_x)
valid_df["proba"] = [p[0] for p in res_proba]

log_loss(valid_df["Win"], valid_df["proba"])
fpr, tpr, thresholds = roc_curve(valid_df["Win"], valid_df["proba"])
auc(fpr, tpr)



