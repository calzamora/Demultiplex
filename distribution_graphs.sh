#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 8

/usr/bin/time -v ./dist_qscore.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -l 101 -o read_001

/usr/bin/time -v ./dist_qscore.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -l 8 -o index_001

/usr/bin/time -v ./dist_qscore.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -l 8 -o index_002

/usr/bin/time -v ./dist_qscore.py -f //projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -l 101 -o read_002