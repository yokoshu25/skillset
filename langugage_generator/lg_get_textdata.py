#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:20:53 2020

@author: yokoishusei
"""

import sys
sys.setrecursionlimit(10000)
import joblib
import time
from tqdm import tqdm
import re


f = open('kokoro.txt', 'r', encoding='shift_jis')
file = f.read()

text = re.split('[、。\n]', file)
f.close()

sentences = []

for sentence in text:
    if len(sentence) > 6 and sentence[6] == 'し':
        sentences.append(sentence)
        

joblib.dump(sentences, "kokoro_2.txt", compress=3)


