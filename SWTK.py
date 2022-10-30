# -*- coding: utf-8 -*-
#Storyline:
# The goal of this script is to create a toolkit for some basic miscellanous tools that can be used from the commandline.
#The script will import all the tools from their separate files and run them as function calls
#The script will have 3 tools: FindWeird, Upload2Cloud, and NLPdecrypter

import argparse
import linecache
from weirdFinder import AD
#import upload2Cloud as u2c
#import nlpDecrypter as nlp


def main():
    parser = argparse.ArgumentParser(description='A toolkit for miscellanous tools')
    parser.add_argument('-fw', '--findWeird', help='Finds the weirdest lines in txt file')
    parser.add_argument('-u2c', '--upload2Cloud', help='Uploads a string to a pastebin like service and returns the link of the paste')
    parser.add_argument('-nlp', '--nlpDecrypter', help='Decrypts a string using NLP')
    args = parser.parse_args()
    #findWeird = args.findWeird
    findWeird = "bSample"
    upload2Cloud = args.upload2Cloud
    nlpDecrypter = args.nlpDecrypter
    output_file = "output.txt"
    if findWeird:
        outputF = AD(findWeird, output_file)
    #if upload2Cloud:
        #output = u2c.main(upload2Cloud)
    #if nlpDecrypter:
        #output = nlp.main(nlpDecrypter)
    print(output)
main()
