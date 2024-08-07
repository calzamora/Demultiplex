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
    parser.add_argument("-Q", help="Quality Score Cut Off") #type: str
    parser.add_argument("-I", help="Index Table") #type: str
    parser.add_argument("-O", help="output directory") #type: str
    return parser.parse_args()

args = get_args()

read_1 = args.R1
index_1 = args.R2
index_2 = args.R3
read_2 = args.R4
cut_off = int(args.Q)
indexes = args.I
output = args.O
#the key is the nt and the value is the W-C cannonical pair
comp_dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C','N': 'N'}
hopped_dict = {}
matched_dict = {}
R1_writing_dict = {}
R2_writing_dict = {}
index_set = set()
unknown_counter = 0 
# seq = "ATGCN"

#define function to reverse compliment 
def rev_comp(seq: str):
    '''this function returns a reverse copliments a sequence of upper case bases including Ns'''
    rev_seq = seq[::-1]
    RC = ""
    for base in rev_seq: 
        RC += comp_dict[base]
    return(RC)

#function to append the index to the header 
def append_header(record: str, Index_1: str, Index_2: str):
    '''This function will take in the header of the read list [0], the seq of index 1 and the rev 
    compliment of index 2 [1] and output the header w indexes appended'''
    Index_2 = rev_comp(Index_2)
    return(f"{record} {Index_1}-{Index_2}")
    

#create a set of the indexes: 
with open(indexes) as index_list: 
    index_list.readline() #skips header
    for line in index_list:
        line = line.strip()
        line = line.split("\t")
        barcode = line[4]
        index_set.add(barcode)

#initialize matched dictionary 
#Key: index 
#Value: occurance (right now 0)
for index in index_set:
    matched_dict[index] = 0

#dictionary for writing out READ 1 + 2: 
#key is the index 
# value is the file handle 
for index in index_set:
    R1_writing_dict[index] = open(f"{output}/{index}_R1.fastq", "w")
    R2_writing_dict[index] = open(f"{output}/{index}_R2.fastq", "w")

# create and open unknown files 
unknown_file_R1 = open(f"{output}/unknown_R1.fastq", "w")
unknown_file_R2 = open(f"{output}/unknown_R2.fastq", "w")

# create and open hopped files: 
hopped_file_R1 = open(f"{output}/hopped_R1.fastq", "w")
hopped_file_R2 = open(f"{output}/hopped_R2.fastq", "w")

#this opens each file concurently and reads the first 4 lines into its respective list
with (open(read_1) as fh1,
      open(index_1) as fh2,
      open(index_2) as fh3,
      open(read_2) as fh4):
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
        if R1[0] == "":
            break
        #append the indexes to the headers of R1 and R2
        R1[0] = (append_header(R1[0], I1[1], I2[1]))
        R2[0] = (append_header(R2[0], I1[1], I2[1]))
        # print(R1)
        #if either index is not in set write to unknown file
        if I1[1] not in index_set or rev_comp(I2[1]) not in index_set:
            unknown_counter +=1
            unknown_file_R1.write(R1[0]+'\n'+R1[1]+'\n'+R1[2]+'\n'+R1[3]+'\n')
            unknown_file_R2.write(R2[0]+'\n'+R2[1]+'\n'+R2[2]+'\n'+R2[3]+'\n')
        #if indexes are in set check if they fall above qual score cut off
        elif I1[1] and rev_comp(I2[1]) in index_set:
            I1_mean_score = bi.qual_score(I1[3])
            I2_mean_score = bi.qual_score(I2[3])
            #if they dont write to unknown 
            if I1_mean_score < cut_off or I2_mean_score < cut_off:
                unknown_file_R1.write(R1[0]+'\n'+R1[1]+'\n'+R1[2]+'\n'+R1[3]+'\n')
                unknown_file_R2.write(R2[0]+'\n'+R2[1]+'\n'+R2[2]+'\n'+R2[3]+'\n')
            #if they do check if indexes match
            elif I1_mean_score >= cut_off and I2_mean_score >= cut_off:
                #if so write to matched file
                if I1[1] == rev_comp(I2[1]):
                    R1_file = R1_writing_dict[I1[1]] #set equal to R1 file handle 
                    R1_file.write(R1[0]+'\n'+R1[1]+'\n'+R1[2]+'\n'+R1[3]+'\n')
                    R2_file = R2_writing_dict[I1[1]] #set equal to R2 file handle 
                    R2_file.write(R2[0]+'\n'+R2[1]+'\n'+R2[2]+'\n'+R2[3]+'\n')
                    #iterate matched index counting dictionary 
                    index = I1[1]
                    matched_dict[index] += 1
                #if not iterate unmatched dict and write to hopped
                elif I1[1] != rev_comp(I2[1]):
                    index_combo = I1[1], rev_comp(I2[1])
                    # print(index_combo)
                    if index_combo in hopped_dict:
                        hopped_dict[index_combo] += 1
                    if index_combo not in hopped_dict:
                        hopped_dict[index_combo] = 1
                    hopped_file_R1.write(R1[0]+'\n'+R1[1]+'\n'+R1[2]+'\n'+R1[3]+'\n')
                    hopped_file_R2.write(R2[0]+'\n'+R2[1]+'\n'+R2[2]+'\n'+R2[3]+'\n')

#close files
for index in index_set:
    R1_writing_dict[index].close()
    R2_writing_dict[index].close()

unknown_file_R1.close()
unknown_file_R2.close()

hopped_file_R1.close()
hopped_file_R2.close()

#calculate the number of hopped reads 
hopped = 0 
for key in hopped_dict:
    hopped += hopped_dict[key]

#cacluate total number of matched reads 
matched = 0
for key in matched_dict:
    matched += matched_dict[key] 

#calculate total number of reads: 
total = unknown_counter + hopped + matched

#print percent of reads frome ach sample 
print(f"Percentage of Reads from each sample:\n")
for index in matched_dict:
    print(f"{index}: {(matched_dict[index]/total) * 100}%\n")

print(f"Overall Amount of Index Swapping:\n {(hopped/total)*100}%\n")
# with open("output_stats.md", "w") as fh1:

print(f"Percentage of Unknown Reads:\n {(unknown_counter/total)*100}")
    





