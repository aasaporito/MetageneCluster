"""Summary
    Tester file to run the program
"""
from metaGene import metaGenePlot
from Extras.hCluster import reduceMatrix,shiftArray
# add single para, if single = true - provide input for left or right end (if exists)


##example use 
# test = metaGenePlot('SRR20274751_HUMAN.sam','hg38.knownGene.gtf','CDS', 50)  # sam file, gff file, up/down stream length
# test.plot( 1,500,d=1)
# # num clusters, normalizat
# +ion length

# test = metaGenePlot('RPKM_alignments.sam','saccharomyces_cerevisiae.gff','gene', 50)  # sam file, gff file, up/down stream length
# test.plot( 1,500,d=1)
test2 = metaGenePlot('Control_ground.sam','hg38.knownGene.gtf','CDS',50)
# #move feature and ud stream (the gathering steps) from constructor  to new method (maybe the cluster one....)
test2.plot("auto",500,d=1)

