#from datapros import metaGenePlot
import gzip 

import os
import io
# test = metaGenePlot('RPKM_alignments.sam.gz','saccharomyces_cerevisiae.gff')
# test.setArray()
maxLength = 0 
numArrays = 0 
currChrom = ''
# with open('saccharomyces_cerevisiae.gff', "r") as gffFile:
#             for line in gffFile:
#                 cols = line.split('\t')

#                 #print(cols)
#                 if len(cols)>1 and cols[6]=='+':
#                     # if cols[0]=='chrmt':
#                     #     print(line)
#                     #print(cols[3], cols[4])
#                     if int(cols[4]) > maxLength:
#                            maxLength=int(cols[4])
#                     if cols[0]!= currChrom:
#                         currChrom=cols[0] 
#                         numArrays+= 1

with gzip.open('RPKM_alignments.sam.gz', 'r') as samFile:
    for line in samFile:
        cols = line.split('\t')
        print(cols)