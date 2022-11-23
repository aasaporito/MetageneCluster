from metaGene import metaGenePlot
# add single para, if single = true - provide input for left or right end (if exists)


#example use 
test = metaGenePlot('SRR20274751_HUMAN.sam','hg38.knownGene.gtf','transcript', 0)  # sam file, gff file, up/down stream length
test.plot( 1,'avg')# num clusters, normalization length

