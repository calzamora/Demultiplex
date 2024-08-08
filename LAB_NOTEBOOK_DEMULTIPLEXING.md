# Demultiplexinng Assignment the first 
## Part 1: Q score distribition PER NUCLEOTIDE
### Question 1 initial data exploraion
create a interactive sesh : 
```
srun --account=bgmp --partition=bgmp --time=1:00:00 --pty bash
```

Working dir: 
```
/projects/bgmp/calz/bioinfo/Bi622/Demultiplex
```

Data lives: 
```
/projects/bgmp/shared/2017_sequencing/
```

File names: 
```
1294_S1_L008_R1_001.fastq.gz
1294_S1_L008_R2_001.fastq.gz
1294_S1_L008_R3_001.fastq.gz
1294_S1_L008_R4_001.fastq.gz
```

Data Exploration : 
In order to determine which were bio reads and which were indexes: 
```
$ zcat 1294_S1_L008_R1_001.fastq.gz | head
$ zcat 1294_S1_L008_R2_001.fastq.gz | head
$ zcat 1294_S1_L008_R3_001.fastq.gz | head
$ zcat 1294_S1_L008_R4_001.fastq.gz | head
```
Length of reads per file: 
use awk to list the length of each line out of head
```
zcat 1294_S1_L008_R4_001.fastq.gz | head | awk '{print length(), $0}'
zcat 1294_S1_L008_R4_002.fastq.gz | head | awk '{print length(), $0}'
zcat 1294_S1_L008_R4_003.fastq.gz | head | awk '{print length(), $0}'
zcat 1294_S1_L008_R4_004.fastq.gz | head | awk '{print length(), $0}'
```
Which encoding? phred 64 or 33?
I am going to grep the 4th line for any characters that are ONLY present in +33 
such as # and $ and < 
```
zcat 1294_S1_L008_R1_001.fastq.gz | head -20 | grep "<"
zcat 1294_S1_L008_R1_002.fastq.gz | head -20 | grep "<"
zcat 1294_S1_L008_R1_003.fastq.gz | head -20 | grep "<"
zcat 1294_S1_L008_R1_004.fastq.gz | head -20 | grep "<"
```

Table: 
| FILE NAME | R1_001.fastq.gz | R2_001.fastq.gz | R3_001.fastq.gz | R4_001.fastq.gz |
| ---: | ---: | ---: | :---: | :---: |
| CONTENTS | read1 | index1 | index2 | read2 |
| READ LENGTH | 101 | 8 | 8 | 101 |
| PHRED ENCODING | +33 | +33 | +33 | +33 |

### Question 2: per base distribution of Q scores - Average @ each positin - per NT mean distribution histogram 

ok i want to be able to test my code on smaller files so I'm going to create test files of 800 lines similar to the test files given in PS 4: 

```
zcat 1294_S1_L008_R1_001.fastq.gz | head -800 >> /projects/bgmp/calz/bioinfo/Bi622/Demultiplex/R1_001_TEST.fastq 
zcat 1294_S1_L008_R2_001.fastq.gz | head -800 >> /projects/bgmp/calz/bioinfo/Bi622/Demultiplex/R2_001_TEST.fastq 
zcat 1294_S1_L008_R3_001.fastq.gz | head -800 >> /projects/bgmp/calz/bioinfo/Bi622/Demultiplex/R3_001_TEST.fastq 
zcat 1294_S1_L008_R4_001.fastq.gz | head -800 >> /projects/bgmp/calz/bioinfo/Bi622/Demultiplex/R4_001_TEST.fastq 
```

how will i store this date? - similar to ps4
initialize a list of the LENGTH of the reads (101 for the biological reads, 8 for indexes) 
    iterate through the file and ADD (+=) to the i position of the list so I end with a list of the SUM of the Q score at each position 

initialie a secnd list to store the MEAN of each position 
    iterate through the first list and divide by (number of lines /4)

#ok break point cause the coffee shop is closing : 

WHERE I AM: 

py script successfully gives me means of each poition in a list ON TEST FILE

WHAT I STILL NEED TO DO : 

generate plot 
test on each test file
run on big script

And we're back: 

seems like its plotting succesfully so yay! Im gunna start the slurm script and test it on the mini files 

#### SLURM SCRIPT: 
/projects/bgmp/calz/bioinfo/Bi622/Demultiplex/distribution_graphs.sh

```
#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 8
```

test on the small file : 
```
$ sbatch distribution_graphs.sh
Submitted batch job 7704972
```

ok looks like that worked, I think I'm going to run all the big files in one even tho it'll take a bit longer so that I dont have a ton of slurm scripts so let me try that with the small files : 

```
$ sbatch distribution_graphs.sh
Submitted batch job 7704974
```
ok sick seems like its working gunna switch it all to the real files: 

```
$ sbatch distribution_graphs.sh
Submitted batch job 7704976
```
ok lets see how long that takes to run 
yikes error: code freezze: 
[out](slurm-7704976.out)

talked to leslie - I need to download gzip and use with gzip.open and use the "rt" read format in the python 

rerun: 
```
$ sbatch distribution_graphs.sh 
Submitted batch job 7757271
 YAY that worked!!

 ok so I updtaed the answers file and so all that I have to do this week is create the test files 

 #### test files: 
 creating test files with 4 records in the order of : 

 MATCHED 
 HOPPED
 UNK INDEX
 LOW QUAL INDEX
 INDEX WITH Ns

 leslie noted to use indexes in the actual set of known indexes so that I dont have to make a new list of known indexes. 

 NOTE: I'm going to have to revisit the qual score cutoff question - leaning toward cutting based on PER BASE qual score rather than mean qual score. 

 known indexes im using for this : 
GTAGCGTA rev comp: CATCGCAT

AACAGCGA rev comp: TTGTCGCT

Ok Im going to MANUALLY make the expected output files now : 
8 total: 
GTAGCGTA_matched_R1.fastq
GTAGCGTA_matched_R2.fastq
AACAGCGA_matched_R1.fastq
AACAGCGA_matched_R2.fastq
unknown_R1.fastq
unknown_R2.fastq
hopped_R1.fastq
hopped_R2.fastq

** adding in an extra record for MATCHED second index so that i have an output to that file

ok im just going to try to figure out how many Ns are present in the indexes 

#Assignment the Third#
My test file are a bit fucked I need the indexes to be in this order : 
 MATCHED 
 HOPPED
 UNK INDEX
 LOW QUAL INDEX
 INDEX WITH Ns

 the matched is fine 

 Ok so I need to make it so that the script outputs the statistics to an output file called output_read_stats.txt

 I think its ready to run so im going to create a slurm script: Assignment-the-third/demultiplex_slurm.sh

 I'm running ti forst on 30 so that I can compare w lauren and it'll go faster
 ```
 $ sbatch ./demultiplex_slurm.sh
Submitted batch job 8372232
 ```
whoops lol forgot to do gzip: 
[slurm out](Assignment-the-third/slurm-8372232.out)

add gzip to open:
```
$ sbatch ./demultiplex_slurm.sh
Submitted batch job 8372236
```
lol errored out again cause i didnt open as "rt"
[slurm out ](Assignment-the-third/slurm-8372236.out)

tested it on my zipped test files and it worked so running agian on the big files
```
$ sbatch ./demultiplex_slurm.sh
Submitted batch job 8372430
```

loops like its running yay

[slurm out](Assignment-the-third/slurm-8372430.out)
 ok ok so it ran correctly but the output stats didnt match lauren and Zack so i rechecked how im calculating and noticed that wasnt counting the unknown files that get written out becuase of the quality score cut off rip 

 so I added that counter itterater and rerunning: 

 ```
 $ sbatch ./demultiplex_slurm.sh
Submitted batch job 8374787
 ```

 whoops forgot to empy the directery 
 ok yay that it worked! 
 [CUT off 30 slurm](Assignment-the-third/slurm-8374787.out)

 [cut off 30 out directory](Assignment-the-third/30_cutoff)
 [cut off 30 stats](Assignment-the-third/output_read_stats_30.txt)

 I"m going to rerun it at 20 , 25, and 35 

 ```
 10:11 PM calz Assignment-the-third $ sbatch 20-dm.sh 
Submitted batch job 8388226
10:18 PM calz Assignment-the-third $ sbatch 25-dm.sh 
Submitted batch job 8388227
10:18 PM calz Assignment-the-third $ sbatch 30-dm.sh 
Submitted batch job 8388228
 ```

 Oh I just realized that this is gunna overewrite the stats files beause thats hard coded so i'm just gunna att a dynamic naming thing w the argparse so cancel those 
 ```
 10:23 PM calz Assignment-the-third $ scancel 8388226
10:23 PM calz Assignment-the-third $ scancel 8388227
10:23 PM calz Assignment-the-third $ scancel 8388228
 ```

make that change and rerun: 
```
10:23 PM calz Assignment-the-third $ sbatch 20-dm.sh 
Submitted batch job 8388695
10:26 PM calz Assignment-the-third $ sbatch 25-dm.sh 
Submitted batch job 8388696
10:26 PM calz Assignment-the-third $ 
10:26 PM calz Assignment-the-third $ sbatch 30-dm.sh 
Submitted batch job 8388697
```
move all out slurms to old_slurm

ok yay those all worked: 
[slurm 20](Assignment-the-third/old_slurm/slurm-8388695.out)
[slurm 25](Assignment-the-third/old_slurm/slurm-8388696.out)
[slurm 30](Assignment-the-third/old_slurm/slurm-8388697.out)