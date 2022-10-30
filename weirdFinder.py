'''
The goal of this script is to serve as an import for the SWTK.py script.
The script will take a txt file as input and output a txt file with the weirdest lines from the input file.
Take the input file and break it down into lines and words and store that in a numpy array.
Pad and truncate the data with the mean and 2 standard deviations of the data.
Split the data into training and testing data.
Use the ECOD model from pyOD to make the predictions on the Data
Match the predictions to the lines in the file and output the lines that are anomalous to a file.
'''
from __future__ import division
from __future__ import print_function
import argparse
import linecache
import pandas as pd
import csv
import re
import tensorflow
import numpy as np
from collections import Counter
import base64
import scipy.io as spio
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split
# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

from pyod.models.ecod import ECOD
import pyod

def AD(findWeird, output_file):
    #Create a variable txtFile to store the input file's name
    txtFile = findWeird + str(".txt")
    #Create a variable OTxtFile to store the output file's name
    OTxtFile = output_file + str(".txt")
    #Take the input file and break it down into lines and words and store that in a numpy array.
    #List comprehension
    with open(txtFile, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        #Split the lines into words
        lines = [line.split() for line in lines]
        lines = [line for line in lines if len(line) > 0] #remove empty lines
        print(lines)
    #Tokenize the data
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    #Convert the text to sequences
    x_train = tokenizer.texts_to_sequences(lines)

    #Pad and truncate the data with the mean and 2 standard deviations of the data.
    max_length = int(np.mean([len(x) for x in x_train]) + 2*np.std([len(x) for x in x_train]))
    x_train = pad_sequences(x_train, maxlen=max_length, padding='post', truncating='post')
    #Split the data into training and testing data.
    x_train, x_test = train_test_split(x_train, test_size=0.8, random_state=42)
    print(x_train)
    print(x_test)
    #Use the ECOD model from pyOD to make the predictions on the Data
    clf = ECOD()
    clf.fit(x_train)
    #get outlier scores
    y_train_scores = clf.decision_scores_
    y_test_scores = clf.decision_function(x_test)
    print(y_train_scores, y_test_scores)
    #Create a variable to store the number of lines in the input file
    num_lines = sum(1 for line in open(txtFile))
    #create a variable bruh to store as many 2's as there are values in y_train_scores
    bruh = [1] * len(y_train_scores)
    #Create a variable with all the values from y_test_scores and bruh
    y_scores = np.concatenate((bruh , y_test_scores))
    print(y_scores)
    #match y_scores to the lines in the file and output the lines whose y_score is lesser than 1
    with open(OTxtFile, 'w') as f:
        for i in range(num_lines):
            if y_scores[i] > 2:
                f.write(str(lines[i]))
                f.write("\n")
    print("Done")
    return

        
