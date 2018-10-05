#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 09:55:08 2018

@author: kartini
"""

import numpy
import io
from itertools import permutations

def read_dataset(fname):
    sentences = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    while idx_line < len(content):
        sent = []
        tag = []
        print('idx_line =')
        print(idx_line)
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                sent.append(content_part[0])
                tag.append(content_part[1])
            idx_line = idx_line + 1
        sentences.append(sent)
        tags.append(tag)
        idx_line = idx_line+2        
    return sentences, tags

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
    }

def transform_to_dataset(sentences, tags):
    X, y = [], []
 
    for sentence_idx in range(len(sentences)):
        for index in range(len(sentences[sentence_idx])):
            X.append(features(sentences[sentence_idx], index))
            y.append(tags[sentence_idx][index])
 
    return X, y

sentences,tags = read_dataset('dataset_postagger.txt')
print(sentences[0])
print(tags[0])


def read_file_init_table(fname):
    tag_count = {}
    tag_count['<start>'] = 0
    word_tag = {}
    tag_trans = {}
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    is_first_word = 0
    
    while idx_line < len(content):
        prev_tag = '<start>'
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                if content_part[1] in tag_count:
                    tag_count[content_part[1]] += 1
                else:
                    tag_count[content_part[1]] = 1
                    
                current_word_tag = content_part[0]+','+content_part[1]
                if current_word_tag in word_tag:
                    word_tag[current_word_tag] += 1
                else:    
                    word_tag[current_word_tag] = 1
                    
                if is_first_word == 1:
                    current_tag_trans = '<start>,'+content_part[1]
                    is_first_word = 0
                else:
                    current_tag_trans = prev_tag+','+content_part[1]
                    
                if current_tag_trans in tag_trans:
                    tag_trans[current_tag_trans] += 1
                else:
                    tag_trans[current_tag_trans] = 1                    
                prev_tag = content_part[1]   
                
            else:
                tag_count['<start>'] += 1
                is_first_word = 1
            idx_line = idx_line + 1

        idx_line = idx_line+1       
    return tag_count, word_tag, tag_trans

tag_count, word_tag, tag_trans = read_file_init_table('dataset_postagger.txt')
print(tag_count)
print(word_tag)
print(tag_trans)

def create_trans_prob_table(tag_trans, tag_count):
    print(tag_trans)
    trans_prob = {}
    for tag1 in tag_count.keys():
        for tag2 in tag_count.keys():
            #print('tag1 = ')
            #print(tag1)
            trans_idx = tag1+','+tag2
            #print('trans_idx = ')
            #print(trans_idx)
            if trans_idx in tag_trans:
                #print(trans_idx)
                trans_prob[trans_idx] = tag_trans[trans_idx]/tag_count[tag1]
    return trans_prob

trans_prob = create_trans_prob_table(tag_trans, tag_count)
print(trans_prob)

def create_emission_prob_table(word_tag, tag_count):
    emission_prob = {}
    for word_tag_entry in word_tag.keys():
        print('---')
        print(word_tag_entry)
        word_tag_split = word_tag_entry.split(',')
        current_word = word_tag_split[0]
        current_tag = word_tag_split[1]
        # print(current_word)
        emission_key = current_word+','+current_tag
        print(emission_key)
        print(len(emission_key))
        if (emission_key == ','):
            emission_key = (word_tag_entry)
            current_word = ','
            current_tag = 'Z'
        
        elif (len(word_tag_split) > 2):
            x = word_tag_split[:-1]
            current_word = ''.join(x)
            current_tag = word_tag_split[-1]
    
        print('ek:', emission_key)
        print('ct:', current_tag)
        print('cw: ',current_word)
        
        emission_prob[emission_key] = word_tag[word_tag_entry]/tag_count[current_tag]    
    return emission_prob
emission_prob = create_emission_prob_table(word_tag, tag_count)
print(emission_prob)

def viterbi(trans_prob, emission_prob, tag_count, sentence):
    #initialization
    viterbi_mat = {}
    tag_sequence = []
    
    sentence_words = sentence.split()
    
    currentTag = '<start>'
    getScoreMax = 1
    for i, currentWord in enumerate (sentence_words):
        viterbi_mat[currentWord] = getScoreMax
        allScore = []
        if (i == len(sentence_words) - 1):
            break
        for j, nilaiEmission in enumerate(emission_prob.keys()):
            # print (currentTag)
            score = 0
            next_word = nilaiEmission.split(',')[0]
            next_tag = nilaiEmission.split(',')[1]
            
            if (next_word == sentence_words[i+1]):
                print(currentWord, ' ', next_word, ' ', currentTag, ' ', next_tag)
                try:
                    print('Transition Prob: ', trans_prob[currentTag + ',' + next_tag])
                    score = getScoreMax * emission_prob[nilaiEmission] * trans_prob[currentTag + ',' + next_tag]
                except:
                    print('Transition Prob: ', 0)
                    score = getScoreMax * emission_prob[nilaiEmission] * 0
            allScore.append({'score':score, 'current_tag': currentTag, 'tag': next_tag})
        
        getScore = [x['score'] for x in allScore]
        print(getScore)
        getIndexMax = getScore.index(max(getScore))           
        getScoreMax = max(getScore)
        currentTag = allScore[getIndexMax]['tag']
        tag_sequence.append(currentTag)
    
    return viterbi_mat, tag_sequence

senetence ="<start> kera untuk amankan"
getViterbi = viterbi(trans_prob, emission_prob, tag_count, senetence)

print(getViterbi)

def baseline(word_tag, sentence):
    new_tag_word = []
    wordsSplit = sentence.split()
    
    for i, word in enumerate(wordsSplit):
        tagWord = []
        for j, current_word_tag in enumerate(word_tag.keys()):
            if (word == current_word_tag.split(',')[0].lower()):
                tagWord.append({'word': word, 'tag': current_word_tag.split(',')[1], 'count': word_tag[current_word_tag] })
        print('tw', tagWord) 
        getCount = [x['count'] for x in tagWord]
        try:
            getIndex = getCount.index(max(getCount))
            getMaxCount = max(getCount)
            
            currentTag = tagWord[getIndex]['tag']
            new_tag_word.append({'tag': currentTag, 'word': word, 'count': getMaxCount})
        except:
            new_tag_word.append({'tag': 'NN', 'word': word, 'count': 0})
    return new_tag_word
    
sentence = "kera untuk amankan"
base = baseline(word_tag, sentence)
print(base) 

sentences,tags = read_dataset('data_uji_postagger.txt')
print(sentences[0])
print(tags[0])  
tag_count, word_tag, tag_trans = read_file_init_table('data_uji_postagger.txt')
print(tag_count)
print(word_tag)
print(tag_trans)
senetence ="<start> kera untuk amankan"
getViterbi = viterbi(trans_prob, emission_prob, tag_count, senetence)

print(getViterbi)
sentence = "kera untuk amankan"
base = baseline(word_tag, sentence)
print(base)