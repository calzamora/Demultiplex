#!/usr/bin/env python
#script will take in:
#READ FILE
#READ LENGTH
#OUTPUT graph name
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("-f", help="specify the filename") #type: str
    parser.add_argument("-l", help="read length") #type: str
    parser.add_argument("-o", help="output graph name") #type: str
    return parser.parse_args()

args = get_args()

file = args.f 
read_len = args.l
output_name = args.o

#initialize a list to hold the SUM of each position quality score

pos_sum_list = []

# loop through through each q score line of the file and use convert phred to add the score to the i position of list 

with open (file) as fh1:
    for indexnum, contents in enumerate(fh1): #this asigns the index location to indexnum and the actual score to contents
            if (indexnum)%4 == 3: # starting at index 3 count by 4 in order to only get q scores
                # print(linenum)