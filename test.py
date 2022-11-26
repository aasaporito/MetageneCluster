from metaGene import metaGenePlot
from hCluster import reduceMatrix,shiftArray
# add single para, if single = true - provide input for left or right end (if exists)


#example use 
#test = metaGenePlot('SRR20274751_HUMAN.sam','hg38.knownGene.gtf','transcript', 0)  # sam file, gff file, up/down stream length
# test.plot( 1,'avg')# num clusters, normalization length

# testMatrix = [  
#     [-1,15.8,26.5,32],
#     [15.8,-1,30.3,31.8],
#     [26.5,30.3,-1,41],
#     [32,31.8,41,-1]
# ]

# print(reduceMatrix([0,1],testMatrix))

# testArray =[1,2,3,4,5,6]
# shiftArray(testArray,3)
# print(testArray)
test2 = metaGenePlot('RPKM_alignments.sam','saccharomyces_cerevisiae.gff','gene',0)
test2.plot(2,500,clusterAlgo='h')
