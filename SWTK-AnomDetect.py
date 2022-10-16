
#The goal of this script is to identify the top 10% of the most anomalous logs in a given log file.
#The script will take a log file as input and output a file with the top 10% of the most anomalous logs.
#If the input file has less than 10 logs then it'll output only one log.
#The script will use the CP-APR algorithm to find the most anomalous log.

import argparse
import pyCP_APR
import pandas as pd
import csv
import re
#import tensorflow as tf
import numpy as np
from collections import Counter

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
        df = pd.read_csv('ex1.csv', sep='delimiter', header=None, on_bad_lines='skip')
        df = df.apply(pd.to_numeric, errors='ignore')
        df.to_csv('ex1.csv', index=False)
        print(df)
        print(df.to_numpy())
        #Encoding the data:
        # using dict comp (finally lol) 30% faster



        #
        tensor1 = tf.convert_to_tensor(df.to_numpy())
        print(tensor1)
        #new_dict = {}
        #df = pd.DataFrame(logCsv)
        #print(df)
        #tensors = [pyCP_APR.Tensor(line) for line in lines]
        #print(tensors)
main()

def get_num_occurances(data_dict, target):
		for key, value in data_dict.items():
			if value == target:
				first_key = key
		counter = Counter(data_dict.values())[target]