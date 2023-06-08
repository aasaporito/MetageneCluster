# Helper functions for __ParseData in metaGene.py
def parseSam(sam):
    samLines = None
    print('Reading SAM file...')
    with open(sam, 'r') as samFile:
        samLines = samFile.readlines()
    samFile.close()

    return samLines
    
# Helper functions for __ParseData in metaGene.py
def parseGff(gff):
    gffLines = None
    print('Reading GFF file...')
    with open(gff) as gffFile:
        gffLines = gffFile.readlines()
    gffFile.close()

    return gffLines