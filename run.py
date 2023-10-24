"""Summary
    File to run to execute the program from the command line.  See README.md for specifications and usage

Attributes:
    clustering (int): Determines if we are making a single metagene plot (1), a set of k-means clustered plots (2), or both (3).
    shape_or_magnitude (str): Determines if we are clustering based on shape (1) or magnitude (2).
    ratio_of_files (str): Determines if we are clustering based on a single input file (0) or the ratio of first file:second file (1).
    sam_file (str): The input file in .sam format that contains the genomic signal to be analyzed.

    sam_file2 (str): The input file in .sam format that contains the genomic signal to divide sam_file's signal by when -r is enabled.
    gff_file (str): The input file in .gff format that contains the genomic regions to be analyzed.
    feature_type (str): The feature to be extracted from the gff for analysis, such as 'gene,' 'CDS,' or 'exon.'
    ud_stream (int): The amount of upstream and downstream sequence to include in the metagene plot(s).  Provided for reference, does not contribute to clustering calculations.
    norm_length (int): The length to normalize features to.
    dist_reduct (float): The number of clusters, k, stops increasing when doing so reduces total variability by less than this amount.  Default: 25%.
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
ud_stream = 500
norm_length = 1000
dist_reduct	= 0.25

argsNum = 1
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
norm_length = int(args[argsNum])
argsNum = argsNum + 1
if len(args) > argsNum:
    dist_reduct = float(args[argsNum])
    argsNum = argsNum + 1

p = metaGenePlot(sam_file, sam_file2, gff_file, feature_type,
                 ud_stream, clustering=clustering)
p.plot("auto", norm_length, dist_reduct, d=shape_or_magnitude)
