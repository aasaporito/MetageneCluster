"""Summary
    Contains the core MetaGenePlot class. This class processes, stores, and plots metagene data from .sam and .gff files.
    Contains list helper functions.
"""
import math
from kMeansClustering import autoKCluster, kCluster
from plot import genPlot
from writeOutput import writeNames, makeDir
from Extras.hCluster import hCluster

import concurrent.futures
from file_tools import *

def invertArray(feature):
    """Summary
        Inverts an array of features.

    Args:
        feature (list): A list of features to invert

    Returns:
        list: Returns the inveted list
    """
    temp = 0
    inverted = feature
    for i in range(math.ceil(len(inverted) / 2)):
        temp = inverted[i]
        inverted[i] = inverted[-(i + 1)]
        inverted[-(i + 1)] = temp
    return inverted


def averageArray(graphArrays):
    """Summary
        Averages feature arrays at each index.

    Args:
        graphArrays (list): List to average.

    Returns:
        list: Averaged list
    """
    avgArray = []
    numArray = len(graphArrays)

    for i in range(len(graphArrays[0])):
        indxTot = 0
        for array in graphArrays:
            indxTot += array[i]
        avgArray.append(indxTot / numArray)
    return avgArray


def averageUpDown(upDownStream):
    """Summary
        Averages up and down stream lists.

    Args:
        upDownStream (list[list]): A 2d list represnting the up and downstream.

    Returns:
        (list, list): A tuple storing the averaged downStream list and the averaged upStream list.
    """
    upArray = []
    downArray = []
    for i in range(len(upDownStream[0][0])):
        upArray.append(0)
        downArray.append(0)
    numArray = len(upDownStream)
    for pair in upDownStream:
        for i in range(len(upDownStream[0][0])):
            upArray[i] += pair[1][i]
            downArray[i] += pair[0][i]

    for j in range(len(upArray)):
        upArray[j] = upArray[j] / numArray
        downArray[j] = downArray[j] / numArray

    return downArray, upArray


class metaGenePlot:

    """Summary
        A class to create and store metagene plots given a SAM and GFF/GFT file. Chomosome labels must be compatible.

    Attributes:
        data (list): Stores raw GFF data
        feature (str): Stores the given feature type. i.e. 'gene' or 'CDS'
        gff (str): The .GFF file name
        names (list): Frames indicating the base of the codon from .GFF column 8.
        plotData (list): Normalized data
        sam (str): .SAM file name
        trash (list): Stores removed features (features that are all 0's.)
    """

    def __init__(self, sam_file: str, gff_file: str, featureType: str, udStream: int = 0, sorted=True):
        """Summary
            Constructor for metaGenePlot class.

        Args:
            sam_file (str): Name of the .sam file to use
            gff_file (str): Name of the .gff file to use
            featureType (str): Feature type i.e. gene, CDS
            udStream (int, optional): The distance between up and down stream for chromosomes in .gff. Default = 0.
            sorted (bool, optional): Deprecated, does nothing.
        """
        self.__samLines, self.__gffLines = self.__parseData(
            sam_file, gff_file)  # set file variables
        self.__samLength = len(self.__samLines)
        self.__gffLength = len(self.__gffLines)
        self.gff = gff_file
        self.sam = sam_file
        self.feature = featureType
        self.names = []
        self.__upDown = udStream
        self.data = []
        self.plotData = []
        self.__progress = 0
        self.__chrom = None
        self.__upDownStream = []  # up down stream data tuples
        self.trash = []
        self.__strand = []

    def sort(self):
        """Summary
            Divides sam file by chromosome. Results are stored in self.__samLines

        Deleted Parameters:
            files (str, optional): Removed: Used to specify the file to split.
        """

        # create dict ent for each chrom     ie chr1:[]
        chroms = {}
        for line in self.__samLines:  # go through file and add each line to respective chrom array
            cols = line.split('\t')
            if len(cols) >= 10 and len(cols[2]) < 8:
                chrom = cols[2]
                if chrom in chroms:
                    chroms[chrom].append(line)
                else:
                    chroms[chrom] = []
                    chroms[chrom].append(line)

        self.__samLines = chroms

    def __parseData(self, sam, gff):
        """Summary
            Reads and stores .sam and .gff files.

        Args:
            sam (string): .sam file name
            gff (string): .gff file name

        Returns:
            (str, str): A tuple storing the raw data from .sam and .gff files
        """
        concurrent.futures.ThreadPoolExecutor()

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            f1 = executor.submit(parseSam, sam)
            f2 = executor.submit(parseGff, gff)
            
        return f1.result(), f2.result()


    def __getChromLength(self):
        """Summary
            Finds the max length and sorts .gff entries by chromosome.
        """

        maxLength = 0
        firstChrom = None
        chroms = {}

        for i, line in enumerate(self.__gffLines):
            cols = line.split('\t')
            if len(cols) > 1 and len(cols[0]) < 8:
                chrom = cols[0]
                if chrom in chroms:
                    chroms[chrom].append(line)
                else:
                    chroms[chrom] = []
                    chroms[chrom].append(line)

            if (len(cols) > 1) and int(cols[4]) > maxLength:

                # farthest point in chromosome
                maxLength = int(cols[4])
                if firstChrom == None:
                    firstChrom = cols[0]

        self.__gffLines = chroms

        # initialize nt positions
        self.__chrom = []
        for i in range(maxLength + self.__upDown):
            self.__chrom.append(0)

    def testSort(self):
        """Summary
            A test function to check on the output of sort()
        """

        self.sort()
        firstChrom, loc = self.__getChromLength()
        gffKeys = []
        samKeys = []
        for key in self.__gffLines:
            gffKeys.append(key)
        for key in self.__samLines:
            samKeys.append(key)

        print('gff chroms ', gffKeys)
        print('sam chroms ', samKeys)

    def __populateChromosome(self, chrom):
        """Summary
            Populates a given chromosome with .sam data

        Args:
            chrom (int): The index of the chomosome within the .sam file
        """
        for line in self.__samLines[chrom]:
            cols = line.split('\t')
            if len(cols) >= 10:
                start, seqLength = int(cols[3]), len(
                    cols[9])  # postion and sequence length
                end = start + seqLength - 1
                for j in range(start - 1, end):
                    try:
                        self.__chrom[j] += 1
                    except:
                        continue

        print('populated ', chrom)

    def __getGffArrays(self, chrom):
        """Summary
            Processes data from gff input. Sets the following class properties: __strand, __upDownStream, data, names, trash.

        Args:
            chrom (int): The index of the chromosome within the .gff file
        """

        for line in self.__gffLines[chrom]:
            cols = line.split('\t')
            if len(cols) > 1 and cols[2] == self.feature:  # if feature of interest
                currArray = []
                dwnStream = []
                upStream = []
                start, end = int(cols[3]) - 1, int(cols[4]) - 1
                down = start - self.__upDown
                up = end + self.__upDown
                if end - start >= 10:  # some CDS in hg38 had length 0
                    # get feature values
                    zeros = 0
                    for i in range(start, end - 1):
                        # pull the values from the chromDIct to build new array
                        currArray.append(self.__chrom[i])
                        zeros += self.__chrom[i]

                    # throw out features that are all zeros
                    if zeros > 0:
                        # get down stream values
                        for i in range(down, start):
                            dwnStream.append(self.__chrom[i])
                        # get up stream values
                        for i in range(end, up):
                            try:
                                upStream.append(self.__chrom[i])
                            except:
                                upStream.append(0)

                        if cols[6] == '-':
                            # invert feature array
                            currArray = invertArray(currArray)
                            # invert and flip up/down stream
                            temp = invertArray(dwnStream)
                            dwnStream = invertArray(upStream)
                            upStream = temp

                        self.__strand.append(cols[6])

                        self.__upDownStream.append((dwnStream, upStream))
                        self.data.append(currArray)
                        self.names.append(cols[8])

                    else:  # zero, skip
                        self.trash.append(cols[8])

        print('Gathered ', chrom, ' data')

    def __resetChrom(self):
        """Summary
            Erases all stored chromosome memory.
        """
        for i in range(len(self.__chrom)):
            self.__chrom[i] = 0

    def __buildData(self):
        """Summary
            Gathers and sets metagene data for each chromosome.
        """
        self.__getChromLength()
        self.sort()

        for chrom in self.__gffLines:
            if chrom in self.__samLines:
                concurrent.futures.ThreadPoolExecutor()

                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(self.__populateChromosome, chrom)
                    executor.submit(self.__getGffArrays, chrom)
                self.__resetChrom()

    def __normalizeArray(self, targetLength):
        """Summary
            Normalizes list stored in self.data. (gff data)
        Args:
            targetLength (int): The length to normalize to. Can be set to 'avg' to use the average array length.

        Returns:
            list: Normalized gff data list
        """
        if targetLength == 'avg':  # find average array length
            avg = 0
            for array in self.data:
                avg += len(array)
            avg = avg / (len(self.data))
            targetLength = round(avg)

        graphArrays = []
        for array in self.data:
            currArray = []
            stepSize = len(array) / targetLength
            step = 0
            prev = 0

            if (stepSize < 1):  # stretch
                while len(currArray) < targetLength:
                    prev = step
                    step += stepSize

                    if math.floor(step) == math.ceil(step):  # reached a whole number step
                        currArray.append(array[int(step) - 1])

                    # step cross an integer -> perform weighted average
                    elif (math.ceil(prev) == math.floor(step)) and prev != 0:

                        weight1 = ((math.ceil(prev) - prev) /
                                   stepSize) * array[int(math.floor(prev))]
                        if math.floor(step) < len(array):
                            weight2 = ((step - math.ceil(prev)) /
                                       stepSize) * array[int(math.floor(step))]
                        else:
                            weight2 = ((step - math.ceil(prev)) /
                                       stepSize) * array[int(math.floor(step) - 1)]

                        avg = weight1 + weight2
                        currArray.append(avg)

                    else:  # not a whole number step but hasnt crossed an integer
                        currArray.append(array[int(math.floor(step))])

            elif (stepSize > 1):  # shrink
                while len(currArray) < targetLength:
                    prev = step
                    step += stepSize

                    i = prev
                    x = 0
                    frac = math.ceil(prev) - prev
                    if frac == 0:
                        frac = 1

                    x += array[math.floor(i)] * frac

                    i += frac

                    while i < step - 1:  # include all the whole values spanned by the step
                        if i < len(array):
                            x += array[math.floor(i)]

                        i += 1

                    frac = step - math.floor(step)
                    if frac == 0:
                        frac = 1

                    if i < len(array):
                        x += array[math.floor(i)] * frac

                    avg = x / stepSize
                    currArray.append(avg)

            else:  # same length
                currArray = array

            graphArrays.append(currArray)
        return graphArrays

    def plot(self, numClusters: int, length: int, clusterUpDown: bool =False, d=0, clusterAlgo='k'):
        """Summary
            Create and saves the plot of a metaGenePlot and saves the data to disk.
            The output is written to Output/(GFF seqname, source, feature)/

        Args:
            numClusters (int): Size of clusters. 'auto' allows for optimal clustering.
            length (int): The feature length to normalize to
            clusterUpDown (bool, optional): When false, upDownStream features are written. Default: False
            d (int, optional): Distance measure between 0 and 1 for clustering. Deault: 0
            clusterAlgo (str, optional): Cluster algorithim to utilize. Values may be 'k' or 'h'. Default: k

        Returns:
            None: 
        """
        self.__buildData()

        print("Normalizing feature length...")
        trendData = self.__normalizeArray(length)

        if clusterAlgo == 'k':
            if numClusters == 1:  # for one cluster just average all data
                avgArray = averageArray(trendData)

                print("Plotting data...")
                name = self.gff[0:-4] + ' ' + self.feature
                if self.__upDown > 0:  # include existing up/down stream data
                    avgDown, avgUp = averageUpDown(self.__upDownStream)
                    print(len(avgDown), len(avgArray), len(avgUp))
                    fullArray = avgDown + avgArray + avgUp
                else:
                    fullArray = avgArray

                genPlot(fullArray, name, None, self.__upDown, len(trendData))
                return
            elif(numClusters == 'auto'):  # find the optimal number of cluster for the given data
                print("Fitting data...")
                print('features:', len(trendData))
                clusters = autoKCluster(trendData, d)
            else:  # divide data into fixed number clusters
                print("Fitting data...")
                clusters, distance = kCluster(numClusters, trendData, d)
                print('Clustering complete')

        elif clusterAlgo == 'h':  # use hCluster on metagene data
            print('hCluster')
            nodes = hCluster(numClusters, trendData)
            clusters = []
            for node in nodes:
                data = node.getIdxs()
                clusters.append(data)

        pathName = makeDir(self.gff[0:-4] + '1')

        for i, cluster in enumerate(clusters):
            clusterData = []
            featureNames = []
            clusterStrands = []
            name = self.gff[0:-4] + ' ' + self.feature + ' cluster ' + str(i)
            for feature in cluster:
                featureNames.append(self.names[feature])
                clusterStrands.append(self.__strand[feature])
                if self.__upDown > 0 and clusterUpDown == False:
                    featureData = self.__upDownStream[feature][0] + \
                        trendData[feature] + self.__upDownStream[feature][1]
                    clusterData.append(featureData)
                else:
                    clusterData.append(trendData[feature])

            avgArray = averageArray(clusterData)

            print("Plotting data...", len(cluster))
            genPlot(avgArray, name, pathName, self.__upDown, len(cluster))
            writeNames(
                featureNames, self.gff[0:-4] + '_' + self.feature + '_' + str(i), pathName)
