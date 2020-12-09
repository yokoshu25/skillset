# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:41:05 2019

@author: shusei yokoi
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:52:28 2019

@author: shusei yokoi
"""


import time
from selenium import webdriver
import pandas as pd 
from sklearn.linear_model import LogisticRegression
import os
import signal
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, roc_curve, auc

filename = "NBAAwithmoreData-11.csv"
try:
    driver = webdriver.Chrome()
    
    lis_dfs = []
    days = ["20", "19", "18", "17", "16", "15", "14", "13","12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
    for day in days:
        url = f'https://www.si.com/nba/scoreboard?date=2019-11-{day}'
        driver.get(url)
        dfs = pd.read_html(driver.page_source)
        del dfs[0]
        df = pd.concat(dfs)
        lis_dfs.append(df)
        time.sleep(5)
    df = pd.concat(lis_dfs)
    #print(df)
    
    df.to_csv(filename, index = False) 
finally:
    os.kill(driver.service.process.pid,signal.SIGTERM)
    driver.quit()

df = pd.read_csv(filename)
index = [i % 2 for i in range(len(df))]
df.index = index
df = df.rename(columns={'Unnamed: 0': 'Home'})
df_home = df.loc[0,:].reset_index(drop=True)
df_away = df.loc[1,:].reset_index(drop=True)
dm = df_home.copy()
df_home.loc[:,"all_three"] = df_home.iloc[:, 1] + df_home.iloc[:,2] + df_home.iloc[:,3]
df_away.loc[:,"all_three"] = df_away.iloc[:, 1] + df_away.iloc[:,2] + df_away.iloc[:,3]

dm["Visitor"] = df_away["Home"]
dm["diff"] = df_home.loc[:,"all_three"]-df_away.loc[:,"all_three"]
result = df_home.loc[:,"T"]-df_away.loc[:,"T"]
dm["target"] = [1 if d > 0 else 0 for d in result]

X_train, X_val, y_train, y_val = train_test_split(dm, dm["target"], train_size=0.6, random_state=1)
lr = LogisticRegression()
lr.fit(X_train["diff"].values.reshape(-1, 1), y_train)
X_val["res"] = lr.predict(X_val["diff"].values.reshape(-1, 1))
res_proba = lr.predict_proba(X_val["diff"].values.reshape(-1, 1))
X_val["proba"] = [p[1] for p in res_proba]

log_loss(X_val["target"], X_val["proba"])
fpr, tpr, thresholds = roc_curve(X_val["target"], X_val["proba"])
auc(fpr, tpr)

lr.predict_proba([[1], [10], [20]])
lr.predict_proba([[-3], [3]])


