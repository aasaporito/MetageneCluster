"""Summary
	File to run to execute the program from the command line.  See README.md for specifications and usage.

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
feature_type = ""
ud_stream = ""

if len(args) == 5:
    try:
        sam_file = args[1]
        gff_file = args[2]
        feature_type = args[3]
        ud_stream = int(args[4])
    except:
        print("Invalid input, closing program")
        exit()
else:
    print("Incorrect number of arguements, closing program")
    exit()

try:
    p = metaGenePlot(sam_file, gff_file, feature_type, ud_stream)
    p.plot("auto", 500, d=1)
except:
    print("Ensure all inputs are meet the requirements, closing program")
    exit()
