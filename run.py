"""Summary
    File to run to execute the program from the command line.  See README.md for specifications and usage

Attributes:
    clustering (int): Determines if we are making a single metagene plot (1), a set of k-means clustered plots (2), or both (3).
    shape_or_magnitude (str): Determines if we are clustering based on shape (1) or magnitude (2).
    sam_file (str): The input file in .sam format that contains the genomic signal to be analyzed.
    sam_file2 (str): An optional second .sam file that will be the source of the signal denominator when the -r/-R option is enabled.
    gff_file (str): The input file in .gff format that contains the genomic regions to be analyzed.
    feature_type (str): The feature to be extracted from the gff for analysis, such as 'gene,' 'CDS,' or 'exon.'
    ud_stream (int): The amount of upstream and downstream sequence to include in the metagene plot(s).  Provided for reference, does not contribute to clustering calculations.
    dist_reduct (float): The cutoff for clustering.  Stop when change in total distance from last cluser is lower than this value.  Between 0 and 1.
"""
import sys
from metaGene import *

args = sys.argv  # [0]: script name

clustering = 2
shape_or_magnitude = 1
ratio_of_files = 0
sam_file = ""
sam_file2 = ""
gff_file = ""
feature_type = ""
ud_stream = -1
dist_reduct = 0.25


argsNum = 1
try:
    if args[argsNum] == "-u":
        clustering = 1
        argsNum = argsNum + 1
    elif args[argsNum] == "-c":
        clustering = 2
        argsNum = argsNum + 1
    elif args[argsNum] == "-uc" or args[argsNum] == "-cu":
        clustering = 3
        argsNum = argsNum + 1
    if args[argsNum] == "-s":
        shape_or_magnitude = 1
        argsNum = argsNum + 1
    elif args[argsNum] == "-m":
        shape_or_magnitude = 0
        argsNum = argsNum + 1
    if args[argsNum] == "-r" or args[argsNum] == "-R":
        ratio_of_files = 1
        argsNum = argsNum + 1
        sam_file = args[argsNum]
        argsNum = argsNum + 1
        sam_file2 = args[argsNum]
        argsNum = argsNum + 1
        gff_file = args[argsNum]
    else:
        sam_file = args[argsNum]
        argsNum = argsNum + 1
        gff_file = args[argsNum]
        argsNum = argsNum + 1
    feature_type = args[argsNum]
    argsNum = argsNum + 1
    ud_stream = int(args[argsNum])
    argsNum = argsNum + 1
    if len(args) >= argsNum:
        dist_reduct = int(args[argsNum])
        argsNum = argsNum + 1
except:
    print("Invalid input, closing program")
    exit()

p = metaGenePlot(sam_file, gff_file, feature_type,
                 ud_stream, clustering=clustering)
p.plot("auto", ud_stream, d=shape_or_magnitude)
