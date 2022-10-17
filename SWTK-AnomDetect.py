
#The goal of this script is to identify the top 10% of the most anomalous logs in a given log file.
#The script will take a log file as input and output a file with the top 10% of the most anomalous logs.
#If the input file has less than 10 logs then it'll output only one log.
#The script will use the CP-APR algorithm to find the most anomalous log.

import argparse
from pyCP_APR import pyCP_APR
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

def main():
    parser = argparse.ArgumentParser(description='Finds the weirdest log in the file')
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()
    input_file = args.input
    file = ('ex1.txt')
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
        with open('ex1.csv', 'w') as f:
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
        max_length = int(np.mean([len(x) for x in x_train]) + 2*np.std([len(x) for x in x_train]))
        x_train = pad_sequences(x_train, maxlen=max_length, padding='post', truncating='post')
        breauh = np.array(x_train)
        print(breauh)

        #Convert the numpy array to a tensor
        tensor = tensorflow.convert_to_tensor(x_train, dtype=tensorflow.int32)
        print(tensor)

        #Run the CP-APR algorithm on the tensor
        #The CP-APR algorithm will return the most anomalous log
        #The CP-APR algorithm will return the index of the most anomalous log
        
        model = pyCP_APR.CP_APR(n_iter=100, verbose=10, method='torch', device='cpu')
        result = model.fit(coords=x_train, values = np.ones(x_train.shape[0]))
        print(result)
        #model.fit(tensor)
        #print(model.anomaly_score())
        #print(model.anomaly_index())

main()

def get_num_occurances(data_dict, target):
		for key, value in data_dict.items():
			if value == target:
				first_key = key
		counter = Counter(data_dict.values())[target]