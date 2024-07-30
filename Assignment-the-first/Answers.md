# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:
[dist_qscores.py](../dist_qscore.py)

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 `|` 101 | +33 |
| 1294_S1_L008_R2_001.fastq.gz | index1 | 8 | +33 |
| 1294_S1_L008_R3_001.fastq.gz | index2 | 8 | +33 |
| 1294_S1_L008_R4_001.fastq.gz | read2 | 101 | +33 |

2. Per-base NT distribution
    Use markdown to insert your 4 histograms here.
    ![INDEX_001](../index_001.png)
    ![INDEX_002](../index_002.png)
    ![READ_001](../read_001.png)
    ![READ_002](../read_002.png)
    
## Part 2
1. Define the problem

The problem for de-multiplexing is that the 4 intitial read files that are given contain reads from 24 seperate cell lines which were each prepped with different barcodes. The goal is to take these 4 files and output 52 files. 2 unknown (FW and RV reads in which the index aka barcode is either not in the barcde library OR is too low of a qual score) - 2 unmatched (FW and RV reads in which the indexes ARE in the library but do not match indicating that index hopping occured) - and 48 matched files (24 FW reads for each indes and 24 RV reads for each index)

2. Describe output

52 files. 2 unknown (FW and RV reads in which the index aka barcode is either not in the barcde library OR is too low of a qual score) - 2 unmatched (FW and RV reads in which the indexes ARE in the library but do not match indicating that index hopping occured) - and 48 matched files (24 FW reads for each indes and 24 RV reads for each index)

3. Upload your [R1_test](../R1_001_TEST.fastq) [R2_test](../R2_001_TEST.fastq) [R3_test](../R3_001_TEST.fastq) [R4_test](../R4_001_TEST.fastq)and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).

4. Pseudocode:

[Pseudcode](pseudo_code_pt2.txt)

5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
