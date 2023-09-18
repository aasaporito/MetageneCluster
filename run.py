"""Summary
    File to run to execute the program from the command line.  See README.md for specifications and usage

Attributes:
    clustering (int): Determines if we are making a single metagene plot (1), a set of k-means clustered plots (2), or both (3).
    shape_or_magnitude (str): Determines if we are clustering based on shape (1) or magnitude (2).
    sam_file (str): The input file in .sam format that contains the genomic signal to be analyzed.
    gff_file (str): The input file in .gff format that contains the genomic regions to be analyzed.
    feature_type (str): The feature to be extracted from the gff for analysis, such as 'gene,' 'CDS,' or 'exon.'
    ud_stream (int): The amount of upstream and downstream sequence to include in the metagene plot(s).  Provided for reference, does not contribute to clustering calculations.
"""
import sys
from metaGene import *

args = sys.argv  # [0]: script name

clustering = 2
shape_or_magnitude = -1
sam_file = ""
gff_file = ""
feature_type = ""
ud_stream = 500

if len(args) == 7:
    try:
        if args[1] == "-u":
            clustering = 1
        elif args[1] == "-c":
            clustering = 2
        elif args[1] == "-uc" or args[1] == "-cu":
            clustering = 3
        if args[2] == "-s":
            shape_or_magnitude = 1
        elif args[2] == "-m":
            shape_or_magnitude = 0
        sam_file = args[3]
        gff_file = args[4]
        feature_type = args[5]
        ud_stream = int(args[6])

    except:
        print("Invalid input, closing program")
        exit()
elif len(args) == 6:
    if args[1] == "-u":
        clustering = 1
    elif args[1] == "-c":
        clustering = 2
    elif args[1] == "-uc" or args[1] == "-cu":
        clustering = 3
    if args[2] == "-s":
        shape_or_magnitude = 1
        sam_file = args[3]
        gff_file = args[4]
        feature_type = args[5]
    elif args[2] == "-m":
        shape_or_magnitude = 0
        sam_file = args[3]
        gff_file = args[4]
        feature_type = args[5]
    else:
        sam_file = args[2]
        gff_file = args[3]
        feature_type = args[4]
        ud_stream = int(args[5])
elif len(args) == 5:
    if args[1] == "-u":
        clustering = 1
    elif args[1] == "-c":
        clustering = 2
    elif args[1] == "-uc" or args[1] == "-cu":
        clustering = 3
    sam_file = args[2]
    gff_file = args[3]
    feature_type = args[4]

else:
    print("Incorrect number of arguements, closing program")
    exit()

p = metaGenePlot(sam_file, gff_file, feature_type,
                 ud_stream, clustering=clustering)
p.plot("auto", ud_stream, d=shape_or_magnitude)
