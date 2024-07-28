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


