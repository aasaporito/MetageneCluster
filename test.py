from datapros import metaGenePlot
from kMeansClustering import kCluster
import math 
import random
from plot import genPlot
from datapros import invertArray 


#sort / require sorted files by chromosome, collect data for one chromosome at a time 


test = metaGenePlot('RPKM_alignments.sam','saccharomyces_cerevisiae.gff','gene', 0) #single para, if single = true - provide input for left or right end (if exists)
# test.plot( 1,1000)

# labels = []
# with open('hg38.knownGene.gtf', 'r') as samFile:
#     lines = samFile.readlines()
#     print(lines)
# samFile.close()
# for line in lines:
#     print(line)
#             for line in samFile:
#                 cols = line.split('\t')
#                 print(line)
#                 if len(cols)>=10 and cols[2] not in labels :
#                     labels.append(cols[2])
          
# print(labels)
 