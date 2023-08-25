"""Summary
    File to run to execute the program from the command line.  See README.md for specifications and usage

Attributes:
    feature_type (str): Description
    gff_file (str): Description
    sam_file (str): Description
    ud_stream (int): Description
"""
import sys
from metaGene import *

args = sys.argv  # [0]: script name

sam_file = ""
gff_file = ""
feature_type = "CDS"
ud_stream = 500
clustering = 2

if len(args) == 6:
    try:
        sam_file = args[2]
        gff_file = args[3]
        feature_type = args[4]
        ud_stream = int(args[5])

        if args[1] == "-u":
            clustering = 1
        elif args[1] == "-c":
            clustering = 2
        elif args[1] == "-uc" or args[1] == "-cu":
            clustering = 3
    except:
        print("Invalid input, closing program")
        exit()
elif len(args) == 4:
    if args[1] == "-u":
        clustering = 1
    elif args[1] == "-c":
        clustering = 2
    elif args[1] == "-uc" or args[1] == "-cu":
        clustering = 3
    sam_file = args[2]
    gff_file = args[3]

else:
    print("Incorrect number of arguements, closing program")
    exit()

p = metaGenePlot(sam_file, gff_file, feature_type,
                 ud_stream, clustering=clustering)
p.plot("auto", ud_stream, d=1)
