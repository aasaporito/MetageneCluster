from datapros import metaGenePlot
from kMeansClustering import kCluster
import math 
import random
from plot import genPlot
from datapros import invertArray 





test = metaGenePlot('RPKM_alignments.sam','saccharomyces_cerevisiae.gff','gene', 0 ) #single para, if single = true - provide input for left or right end (if exists)
test.plot( 4,500)
 
# labels = []
# with open('SRR20274751_HUMAN.sam', 'r') as samFile:
#             for line in samFile:
#                 cols = line.split('\t')
#                 print(line)
#                 if len(cols)>=10 and cols[2] not in labels :
#                     labels.append(cols[2])
          
# print(labels)
 