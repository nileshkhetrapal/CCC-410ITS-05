
#The goal of this script is to identify the top 10% of the most anomalous logs in a given log file.
#The script will take a log file as input and output a file with the top 10% of the most anomalous logs.
#If the input file has less than 10 logs then it'll output only one log.
#The script will use the CP-APR algorithm to find the most anomalous log.
from __future__ import division
from __future__ import print_function

import argparse
#from pyCP_APR import pyCP_APR
#sys.path.insert(0, '/pyCP_APR/pyCP_APR/')
import pandas as pd
import csv
import re
import tensorflow
import numpy as np
from collections import Counter
import base64
import scipy.io as spio

import os
import sys

# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.insert(1, 'C:/Users/nilesh/Downloads/SWTK/pyod-master/pyod')
from pyod.models.auto_encoder import AutoEncoder
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
from pyod.models.ecod import ECOD
from pyod.utils.example import visualize


from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def main():
    parser = argparse.ArgumentParser(description='Finds the weirdest line in the file')
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()
    input_file = args.input
    file = ("dSample.txt")
    output_file = args.output
    #Read the text file and create tensors from it
    #List comprehension to create a CSV file from the text file
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines] #remove whitespace
        #Split the lines into words, words inside brackets are considered one word
        #create regex to split the lines into words based on either space or []
        #  but keep words inside [] together
        
        #lines = [re.split(r'(\[.*?\])', line) for line in lines]
        #lines = [re.split(r'(\().*?\))', line) for line in lines]
        lines = [line.split() for line in lines] #split the lines into words based on spaces
        lines = [line for line in lines if len(line) > 0] #remove empty lines
        lines = [line for line in lines if line[0] != '#'] #remove comments
        lines = [line for line in lines if line[0] != ''] #remove empty lines
        
        #Read the lists to CSV
        csv_file = file + ".csv"
        with open(csv_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(lines)
        #read_file = pd.read_csv ([print(line) for line in lines])
        

        #Convert the CSV file's values to Numbers
        num_words = 10000
        tokenizer = Tokenizer(num_words=num_words, oov_token="<OOV>")
        tokenizer.fit_on_texts(lines)
        x_train = tokenizer.texts_to_sequences(lines)
        bruh = np.array(x_train)
        print(bruh)

        #Padding and Truncating the data
        #The length of the logs needs to be the same for the algorithm to work
        #The algorithm will truncate the logs that are longer than the max length
        #The algorithm will pad the logs that are shorter than the max length
        #The max length is the average length of the logs + 2 standard deviations
        max_length = (np.mean([len(x) for x in x_train]) + 2*np.std([len(x) for x in x_train]))
        x_train = pad_sequences(x_train, maxlen=max_length, padding='post', truncating='post')
        breauh = np.array(x_train)
        print(breauh)

        #Create x_train and 
        y_train = np.array([0]*len(x_train))
        print(y_train)
        
        #Convert the numpy array to a tensor
        tensor = tensorflow.convert_to_tensor(x_train, dtype=tensorflow.int32)
        print(tensor)
         # train ECOD detector
        clf_name = 'ECOD'
        clf = ECOD()

        # you could try parallel version as well.
        # clf = ECOD(n_jobs=2)
        clf.fit(tensor)
        # get the prediction labels and outlier scores of the training data
        y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
        print('y_train_pred', y_train_pred)
        y_train_scores = clf.decision_scores_ # raw outlier scores
         # evaluate and print the results
        print("\nOn Training Data:")
        #evaluate_print(clf_name, y_train, y_train_scores)

        
        #Use y_train_pred to find the anomalous lines in the file
        #The anomalous lines will be the lines that have a 1 in y_train_pred
        counter = 0
        with open (file, 'w' ) as f:
            lines = f.readlines()
            if y_train_pred[counter] == 1:
                print(lines)
                with open (output_file, 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(lines)
            counter = counter + 1
        #For each line in the array, if the last value is 1, then it's an outlier and it should be outputted to weird array
        '''weird = []
        for line in breauh:
            if line[-1] == 1:
                weird.append(line)
        print(weird)
        #Output the weird array to a file
        with open('weird.txt', 'w') as f:
            for line in weird:
                f.write(line)
        #print(weird)

    # visualize the results
        #visualize(clf_name, x_train, y_train, x_test, y_test, y_train_pred, y_test_pred, show_figure=True, save_figure=False)

        #Run the CP-APR algorithm on the tensor
        #The CP-APR algorithm will return the most anomalous log
        #The CP-APR algorithm will return the index of the most anomalous log
        
        #model = pyCP_APR.CP_APR(n_iter=100, verbose=10, method='torch', device='cpu')
        #result = model.fit(coords=tensor, values = np.ones(x_train.shape[0]))
        #print(result)
        #model.fit(tensor)
        #print(model.anomaly_score())
        #print(model.anomaly_index())
        #Convert the following pseudocode to python:
        ##Ci , j refers to the jth region (subclass) of the anomaly score i (i takes values r or s).
        #Algorithm 3: Distance measure
        #Input: r, s
        #Sort r and s according to r and assign corresponding indexes
        #Sort s according to s
        #Deine regions (subclasses) by setting the percentiles of each class for r and s
        #Calculate mean and standard deviation for each region for r and s
        #for i = r, s do
        #for j, k =all combinations of regions do
        #Compute ω(j, k) for all points in Ci,j and Ci,k
        #Compute sign function, sдn, between Ci,j and Ci,k
        #Calculate coeicients as ω · sдn
        #Input coeicients to the placeholder matrix in the corresponding coordinates
        #end
        #end
        #Compute ⟨r, s⟩ω coeicient from placeholder matrix
        #Algorithm 4: Gaussian Equivalence Criterion (GEC)
        #Input: r,p
        #Compute ||r ||2 with the Distance measure algorithm using as input (r,r)
        #Compute ||s ||2 with the Distance measure algorithm using as input (s, s)
        #Compute ⟨r, s⟩ with the Distance measure algorithm using as input (r, s)
        #Calculate the GEC value, ϕ, as:
        #ϕ =
        #⟨r, s⟩
        #||r ||||s ||
        #Output: ϕ
        def distance_measure(r, s):
            #Sort r and s according to r and assign corresponding indexes
            r = sorted(r)
        
            #Sort s according to s
            #Deine regions (subclasses) by setting the percentiles of each class for r and s
            #Calculate mean and standard deviation for each region for r and s
            #for i = r, s do
            #for j, k =all combinations of regions do
            #Compute ω(j, k) for all points in Ci,j and Ci,k
            #Compute sign function, sдn, between Ci,j and Ci,k
            #Calculate coeicients as ω · sдn
            #Input coeicients to the placeholder matrix in the corresponding coordinates
            #end
            #end
            #Compute ⟨r, s⟩ω coeicient from placeholder matrix
            pass
        '''



main()

def get_num_occurances(data_dict, target):
		for key, value in data_dict.items():
			if value == target:
				first_key = key
		counter = Counter(data_dict.values())[target]
