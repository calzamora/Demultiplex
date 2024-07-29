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