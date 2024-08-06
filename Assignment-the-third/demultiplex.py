#!/usr/bin/env python

import gzip 
import argparse
import bioinfo as bi
import numpy as np 

#this script should take in the 4 read files and the index table, the quality score cutoff and the output directory

def get_args():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("-R1", help="Read file 1 ") #type: str
    parser.add_argument("-R2", help="Read file 2") #type: str
    parser.add_argument("-R3", help="Read file 3") #type: str
    parser.add_argument("-R4", help="Read file 4") #type: str
    parser.add_argument("-I", help="Index Table") #type: str
    parser.add_argument("-O", help="output directory") #type: str
    return parser.parse_args()

args = get_args()

read_1 = args.R1
index_1 = args.R2
index_2 = args.R3
read_2 = args.R4
indexes = args.I
output = args.O
#the key is the nt and the value is the W-C cannonical pair
comp_dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C','N': 'N'}
hopped_dict = {}
R1_writing_dict = {}
R2_writing_dict = {}
index_set = set()
unknown_counter = 0 
# known = True
# matched = True


seq = "ATGCN"

#define function to reverse compliment 
def rev_comp(seq: str):
    '''this function returns a reverse copliments a sequence of upper case bases including Ns'''
    rev_seq = seq[::-1]
    # print(rev_seq)
    RC = ""
    for base in rev_seq: 
        RC += comp_dict[base]
    return(RC)

#function to append the index to the header 
def append_header(record: str, I1: str, I2: str):
    '''This function will take in the header of the read list [0], the seq of index 1 and the rev 
    compliment of index 2 [1] and output the header w indexes appended'''
    return(f"{record} {I1}-{I2}")
    

#create a set of the indexes: 
with open(indexes) as index_list: 
    index_list.readline() #skips header
    for line in index_list:
        line = line.strip()
        line = line.split("\t")
        barcode = line[4]
        index_set.add(barcode)
# print(index_set)

#dictionary for writing out READ 1 + 2: 
#key is the index and the value is the file handle 
for index in index_set:
    R1_writing_dict[index] = open(f"{index}_R1.fastq", "w")
    R2_writing_dict[index] = open(f"{index}_R2.fastq", "w")

# create and open unknown files 
unknown_file_R1 = open("unknown_R1.fastq", "w")
unknown_file_R2 = open("unknown_R2.fastq", "w")

# create and open hopped files: 
hopped_file_R1 = open("hopped_R1.fastq", "w")
hopped_file_R2 = open("hopped_R2.fastq", "w")

#this opens each file concurently and reads the first 4 lines into its respective list
with (gzip.open(read_1) as fh1,
      gzip.open(index_1) as fh2,
      gzip.open(index_2) as fh3,
      gzip.open(read_2) as fh4):
    while True:
        R1 = []
        I1 = []
        I2 = []
        R2 = []
        for i in range (4):
            R1.append(fh1.readline().strip())
            I1.append(fh2.readline().strip())
            I2.append(fh3.readline().strip())
            R2.append(fh4.readline().strip())
        #append the indexes to the headers of R1 and R2
        R1[0] = (append_header(R1[0], I1[1], rev_comp(I2[1])))
        R2[0] = (append_header(R2[0], I1[1], rev_comp(I2[1])))
        if I1[1] not in index_set or rev_comp(I2[1]) not in index_set:
            unknown_counter +=1
            unknown_file_R1.write(R1[0]+'\n'+R1[1]+'\n'+R1[2]+'\n'+R1[3]+'\n')
            unknown_file_R2.write(R2[0]+'\n'+R2[1]+'\n'+R2[2]+'\n'+R2[3]+'\n')
        elif I1[1] and rev_comp(I2[1]) in index_set:
            mean_score = bi.qual_score(I1[3])
            print(mean_score)
            


            



        break





