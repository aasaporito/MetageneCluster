from metaGene import metaGenePlot
from hCluster import reduceMatrix,shiftArray
# add single para, if single = true - provide input for left or right end (if exists)


#example use 
#test = metaGenePlot('SRR20274751_HUMAN.sam','+hg38.knownGene.gtf','transcript', 0)  # sam file, gff file, up/down stream length
# test.plot( 1,'avg')# num clusters, normalizat
# +ion length


test2 = metaGenePlot('RPKM_alignments.sam','saccharomyces_cerevisiae.gff','intron',100)
test2.plot(3,400,d=1)

# with open('RPKM_alignments.sam', 'r') as samFile:
#     for i,line in enumerate(samFile): 
#         print(line)
#         if i>20:
#             break 

# samFile.close()