#This will only work for windows for now
import argparse
import os
import sys
import time

#Get username
username = os.getlogin()
#Check if anomaly_detection.exe is in the temp directory
#If anomaly_detection.exe is not in the temp directory, download it from the repository,compile it and place it in the temp directory
if not os.path.isfile("C:\\Users\\" + username + "\\AppData\\Local\\Temp\\anomaly_detection.exe"):
    print("anomaly_detection.exe is not in the temp directory. Downloading it from the repository...")
    os.system("curl -L https://github.com/Redempt/anomaly_analysis/releases/download/Dev_Only/anomaly_detection.exe -o anomaly_detection.exe")
    print("anomaly_detection.exe was downloaded successfully.")
    print("Moving anomaly_detection.exe to the temp directory...")
    os.system("move anomaly_detection.exe C:\\Users\\" + username + "\\AppData\\Local\\Temp\\anomaly_detection.exe")
    print("Done.")

#Get the arguments from the user
parser = argparse.ArgumentParser(description='Anomaly detection script')
parser.add_argument('-i', '--input', help='Input file path')

#Create a function to run anomaly_detection.exe with the -a flag and the input file piped in.
def run_anomaly_detection():
    #Read the input file on a line by line basis and store in a list
    with open(args.input, 'r') as f:
        lines = f.readlines()
    #Create a dictionary to store the lines and their anomaly score
    anomaly_dict = {}
    #Put the lines in the dictionary
    for line in lines:
        anomaly_dict[line] = 0
    #Run anomaly_detection.exe with the -a flag and the input file piped in.
    #The Parse the output and identify the anomaly score of the lines and sort them by the anomaly score
    print("Running anomaly_detection.exe with the default parameters...")
    #print(args.input)
    #os.system("C:\\Users\\nilesh\\Documents\\Capstone\\Test\\anomaly_detection.exe" + args.input + " -a")
    output = os.popen("C:\\Users\\" + username + "\\AppData\\Local\\Temp\\anomaly_detection.exe " + args.input + " -a").read()
    print("Done.")
    #Take anomaly scores and put them in the dictionary with their corresponding Line_Number
    for line in output.splitlines():
        line = line.split(':')
        anomaly_dict[lines[int(line[0]) - 1]] = float(line[1])
    #print("dictionary:", anomaly_dict)
    #Sort the dictionary by the anomaly score
    anomaly_dict = dict(sorted(anomaly_dict.items(), key=lambda item: item[1]))
    #print("Sorted dictionary:", anomaly_dict)
    #Print the sorted dictionary to the screen
    for key, value in anomaly_dict.items():
        print(key)
    print("The file is sorted by the anomaly score.")
    sys.exit()

def main():
    global args
    args = parser.parse_args()
    #Check if the input file exists
    if os.path.isfile(args.input):
        print("Input file exists.")
        #Check if the input file is empty
        if os.stat(args.input).st_size == 0:
            print("Input file is empty.")
            sys.exit()
        else:
            print("Input file is not empty.")
            run_anomaly_detection()
    else:
        print("Input file does not exist.")
        sys.exit()

main()
