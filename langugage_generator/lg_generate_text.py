#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:46 2020

@author: yokoishusei
"""
from collections import Counter, defaultdict
from tqdm import tqdm
import joblib
from janome.tokenizer import Tokenizer
from collections import Counter, defaultdict
import random

BEGIN = '__BEGIN__'
END = '__END__'


# words = t.tokenize(sentence, wakati=True)
# words = [BEGIN] + words + [END]

# three_words_list =[]
# for i in range(len(words) - 2):
#     three_words_list.append(words[i:i+3])
# three_words_list


def get_three_words_list (sentence):
    t = Tokenizer()
    words = t.tokenize(sentence, wakati=True)
    words = [BEGIN] + words + [END]
    three_words_list =[]
    for i in range(len(words) - 2):
        three_words_list.append(tuple(words[i:i+3]))
    return three_words_list

#sentences = ['おいしいビールを飲もう', 'ビールを飲もう', 'おいしいビールは生']
sentences = ['200円になります', '1000円でいいですか？', 'はい', 'はい', 'はい', '800円のお返しです', 'ありがとうございました。','はい', 'またお越しくださいませ']

three_words_list = []

for sentence in sentences:
    three_words_list += get_three_words_list(sentence)
three_words_count = Counter(three_words_list)
three_words_count

def generate_markov_dict(three_words_count):
    """マルコフ連鎖での文章錬成辞書データを作成"""
    markov_dict = {}
    for three_words, count in three_words_count.items():
        two_words = three_words[:2]
        next_word = three_words[2]
        if two_words not in markov_dict:
            markov_dict[two_words] = {'words': [], 'weights': []}
        markov_dict[two_words]['words'].append(next_word)
        markov_dict[two_words]['weights'].append(count)
    return markov_dict

markov_dict = generate_markov_dict(three_words_count)
markov_dict

def get_first_word_and_count(three_words_count):
    """最初の単語を選択するための辞書データを作成"""
    first_word_count = defaultdict(int)
    
    for three_words, count in three_words_count.items():
        if three_words[0] == BEGIN:
            next_word = three_words[1]
            first_word_count[next_word] += count
    return first_word_count

get_first_word_and_count(three_words_count)

def get_first_words_weights (three_words_count):
    """最初の単語と重みリストの作成"""
    first_word_count = get_first_word_and_count(three_words_count)
    words = []
    weights = []
    for word, count in first_word_count.items():
        words.append(word)
        weights.append(count)
        
    return words, weights 

first_words, first_weights = get_first_words_weights(three_words_count)
first_words, first_weights


def generate_text(first_words, first_weights, markov_dict):
    """入力された辞書データを元に文章を生成する"""
    first_word = random.choices(first_words, weights = first_weights)[0]
    generate_words =[BEGIN, first_word]
    while True:
        pair = tuple(generate_words[-2:])
        words = markov_dict[pair]['words']
        weights = markov_dict[pair]['weights']
        next_word = random.choices(words, weights = weights)[0]
        if next_word == END:
            break
        generate_words.append(next_word)
        
    return ''.join(generate_words[1:])
sentences = joblib.load('kokoro_2.txt')
three_words_list = []


for sentence in tqdm(sentences):
    three_words_list += get_three_words_list(sentence)
three_words_count = Counter(three_words_list)
len(three_words_count)

markov_dict = {}       
markov_dict = generate_markov_dict(three_words_count) 




print(len(markov_dict))
first_words, first_weights = get_first_words_weights(three_words_count)
print(len(first_words))

for _ in range(90):
    sentence = generate_text(first_words, first_weights, markov_dict)
    print(sentence)
    
    
    
    
    
    
    
    
    
    
    