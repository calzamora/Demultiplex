Define the problem: 
The problem for de-multiplexing is that the 4 intitial read files that are given contain reads from 24 seperate cell lines which were each prepped with different barcodes. The goal is to take these 4 files and output 52 files. 2 unknown (FW and RV reads in which the index aka barcode is either not in the barcde library OR is too low of a qual score) - 2 unmatched (FW and RV reads in which the indexes ARE in the library but do not match indicating that index hopping occured) - and 48 matched files (24 FW reads for each indes and 24 RV reads for each index)


ARG PARSE: 
inputs: 
1) f1, f2, f3, f4
2) quality score threshold 
3) matched index txt


FUNCTIONS: 
def rev_compliment: 
take in STRING 
for each index pos of the string: 
    string.upper()
    string.replace(A, T)
    string.replace(T, A)
    string.replace(C, G)
    string.replace(G, C)
return(string)

def:append_index_head
take in 3 strings (header, index 1, index 2)
return(header + index1 + index2)

def: get average of quality score for read (PS4)


def: write file 


OPEN txt file of indexes 
    create a set containing ALL UNIQUE barcodes

4 lists to hold the RECORD for each file every loop
File1 = []
File2 = []
File3 = []
File4 = []
matched_dict = {} #to count the number in each file 
unmatched_dict = {}

OPEN all 4 read files concurently (While true loop)
    for i in range 4 
        file1.readline.strip.append
        file2.readline.strip.append
        file3.readline.strip.append
        file4.readline.strip.append
    use reverse compliment function to rc R3 file seq line 
    APPEND indexes (R2 + R3 files) to END OF ALL HEADERS in R1 + R4 files
    append_index_head(F2)
    append_index_head(F3)
    IF (indexes are unknown either containing Ns or NOT in the set of indexes)
        write R1 file (w indexes appended) -> UNKNOWN biological reads 1 (FW reads) 
        write R2 file (w indexes appended) -> UNKNOWN biological reads 2 (RV reads)
    ELIF indicies are valid (are in the set of known indexes):
        IF mean qual score of the INDEX is NOT greater than or equal to the cut off:
        write R1 file (w indexes appended) -> UNKNOWN biological reads 1 (FW reads) 
        write R2 file (w indexes appended) -> UNKNOWN biological reads 2 (RV reads)
        ELIF: 
            IF both indexes appended to the headers MATCH:
                if in matched_dict += 1
                if not in matched = 1
                write R1 file (w indexes appended) -> MATCHED biological reads 1 (FW reads) 
                write R2 file (w indexes appended) -> MATCHED biological reads 2 (RV reads)
            ELIF: (indexes are valid but do not MATCH):
                if in unmatched_dict += 1
                if not in unmatched = 1
                write R1 file (w indexes appended) -> UNMATCHED biological reads 1 (FW reads) 
                write R2 file (w indexes appended) -> UNMATCHED biological reads 2 (RV reads)
    File1 = []
    File2 = []
    File3 = []
    File4 = []
