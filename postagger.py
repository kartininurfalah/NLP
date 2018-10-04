#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 07:41:19 2018

@author: kartini
"""

import csv
import itertools

# =============================================================================
# Parameter
# =============================================================================
dataKorpusTrain = [] 
dataKorpusTest = []
dataKorpusAsli = []
# =============================================================================
# Function to read dataKorpus
# =============================================================================
def readFile(file,dataKorpus):
    with open(file) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        # for row in rd[:1000]:
        for row in rd:
            dataKorpus.append(row)
readFile("Indonesian_Manually_Tagged_Corpus.tsv", dataKorpusAsli)
dataTrain = dataKorpusAsli[0:10]        
dataKorpusTrain=dataKorpusAsli[0:1000]        
dataKorpusTest = dataKorpusAsli[1000:1020]

korpusTrainConcate = []
print(dataKorpusTrain[999][0])
for i in range(999):
    print(dataKorpusTrain[i][0])
    # print(i)
    # for j in (len(i)):
    #     print(j)
# def readFileTrain(file,dataKorpus):  
#     with open(file) as fd:
#         rd = csv.reader(fd, delimiter="\t", quotechar='"')
#         # for row in rd[:1000]:
#         for row in itertools.islice(rd, 1000):
#             dataKorpus.append(row)
#             print(row)

# def readFileTest(file,dataKorpus):  
#     with open(file) as fd:
#         rd = csv.reader(fd, delimiter="\t", quotechar='"')
#         # for row in rd[:1000]:
#         for row in (rd, [1000:1019]):
#             dataKorpus.append(row)
#             print(row)
# readFile("Indonesian_Manually_Tagged_Corpus.tsv", dataKorpusTrain )    
# readFile("Indonesian_Manually_Tagged_Corpus.tsv", dataKorpusTest )

