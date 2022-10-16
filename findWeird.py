###
#The purpose of this software is to provide a simple way to find the weirdest line of the log.
#The way it should work is take a file as input from the commandline and return an output file in the run directory.
#The output file will have all the logs sorted by weirdness from the weirdest log being on top to the most normal log being at the bottom.
###
import argparse
import linecache
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import csv
import tensorflow_decision_forests as tfdf
def main():
    parser = argparse.ArgumentParser(description='Finds the weirdest log in the file')
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()
    input_file = args.input
    file = ('ex1.txt')
    num_lines = sum(1 for line in open('ex1.txt'))
    print(num_lines)
    ppFile = open("pp.csv", "w")
    for Line in range(num_lines):
        content = linecache.getline('ex1.txt', Line)
        writer = csv.writer(ppFile)
        writer.writerow(content)
    output_file = args.output
    print("pp.csv")
    #for Line in len(file):
    #    print (content[Line])
    le = preprocessing.LabelEncoder()
main()
#Step 1 : SPELL to break the log down into parameters and keys
#Step 2: 
#uCare@Pwn3rzs
#