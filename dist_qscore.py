#!/usr/bin/env python
#script will take in:
#READ FILE
#READ LENGTH
#OUTPUT graph name
import argparse
import bioinfo as bi
def get_args():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("-f", help="specify the filename") #type: str
    parser.add_argument("-l", help="read length") #type: str
    # parser.add_argument("-o", help="output graph name") #type: str
    return parser.parse_args()

args = get_args()

file = args.f 
read_len = int(args.l)
# output_name = args.o

#initialize a list to hold the SUM of each position quality score

pos_sum_list = []
for i in range(0,read_len): # iterate through a range of 0 - length of reads given by args parse  
    pos_sum_list.append(0)


# loop through through each q score line of the file and use convert phred to add the score to the i position of list 
num_lines = 0 
with open (file) as fh1:
    for indexnum, contents in enumerate(fh1): #this asigns the index location to indexnum and the actual score to contents
            num_lines += 1 #counter for the sum calc later
            if (indexnum)%4 == 3: # starting at index 3 count by 4 in order to only get q scores
                 for index, score in enumerate(contents.strip('\n')): 
                    converted_score = bi.convert_phred(score)
                    pos_sum_list[index] += converted_score

# print(len(pos_sum_list))
# print(pos_sum_list)

#initialize a list to hold the MEAN of each position 
mean_list = []
for i in range(0,read_len): # iterate through a range of 0 - length of reads given by args parse  
    mean_list.append(0)

#set total = to number of RECORDS in file
total = int(num_lines/4)

for i, sum in enumerate(pos_sum_list): 
     mean = sum/total
     mean_list[i] = mean

# print(mean_list)