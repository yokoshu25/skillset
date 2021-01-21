#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import re
from instapy import InstaPy
import schedule
import time
import random



tags = ['統計学', 'statistics','stats','データサイエンス','datascience','data','データ','鬼滅の刃','統計']



def job():
    try:

        session = InstaPy(username="user_name", password="password", headless_browser=True)
        session.login()
        tag = random.choice(tags)
        session.like_by_tags([tag], amount=10)
        session.end()

    except:
        import traceback
        print(traceback.format_exc())
        
        
        

def makelog():
    try:
        url_id = []
        keep_phrases = ['Image from: b\'', '  Link: b\'']
        
        with open('/path/to/.log/', 'r') as f:
            f = f.readlines()
        
        for lines in f:
            for phrase in keep_phrases:
                if phrase in lines:
                    url_id.append(lines)
                    break
        date = list()
        user_id = list()
        link = list()
        df = pd.DataFrame() 
        
        
        for line in url_id:
            if bool(re.search(r'Link: b\'',line)):
                a = re.search(r'Link: b\'',line)
                link.append(line[a.span()[1]:len(line)-2])
                date.append(line[6:25])
            elif bool(re.search(r'Image from: b\'',line)):
                a = re.search(r'Image from: b\'',line)
                user_id.append(line[a.span()[1]:len(line)-2])
        
        df = pd.DataFrame(list(zip(date, user_id, link)), columns =['date', 'user_id', 'link'])
        df.to_csv('/path/to/log.csv', header = True, index=False)

    except:
        import traceback
        print(traceback.format_exc())
        
        

schedule.every().day.at("15:20").do(job)
schedule.every().day.at("21:29").do(job)
schedule.every().day.at("00:00").do(makelog)


while True:
    schedule.run_pending()
    time.sleep(5)
    




