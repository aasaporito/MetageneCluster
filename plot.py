"""Summary
    Provides the genPlot function to create and save feature plots.
"""
import matplotlib.pyplot as plt
import numpy as np

# Unclustered edition


def genPlotUn(result, fname, dirName, udStream, numFeatures, computeRatio):
    """Summary
        Creates a plot of features using numpy and matplotlib for unclustered
    Args:
        result (list): The result to plot
        fname (str): File name to be used as the plot title
        dirName (str): Directory to output to within Outputs/
        udStream (int): Distance between chromosomes.
        numFeatures (int): The number of features (utilized in the plot title)
        computeRatio (boolean): Whether to compute the ratio of two files (true) or plot a single file's coverage (false)
    """
    print("Generating Unclustered plot")
    y = np.array(result)
    x = np.arange(len(y))
    
    # plot
    fig, ax = plt.subplots()

    ax.set(xlim=(0, len(result)), xticks=np.arange(0, len(result)),
           ylim=(0, max(result)), yticks=np.arange(0, max(result) + 10))  # result[1]

    ax.set_xlabel('Distance')
    if computeRatio:
        ax.set_ylabel('log2-ratio')
    else:
        ax.set_ylabel('Coverage')

    plt.figure(figsize=(15, 10))
    plt.plot(x[(len(x) - udStream - 1):len(x) - 1],
             y[(len(x) - udStream - 1):len(x) - 1], linestyle='-.', color='red')
             
    plt.plot(x[0:udStream - 1], y[0:udStream - 1], linestyle='-.', color='red')
    
    plt.plot(x[udStream - 1:(len(x) - udStream - 1)],
             y[udStream - 1:(len(x) - udStream - 1)], color='black')
    plt.title(fname)
    plt.xlabel('Distance')
    if computeRatio:
        plt.ylabel('log2-ratio')
    else:
        plt.ylabel('Coverage')

    path = fname + ".png"  # in case of single plot
    if dirName != None:
        path = 'Outputs/' + dirName + '/' + path

    plt.savefig(path, dpi=75)

def genPlot(result, fname, dirName, udStream, numFeatures, computeRatio):
    """Summary
        Creates a plot of features using numpy and matplotlib.
    Args:
        result (list): The result to plot
        fname (str): File name to be used as the plot title
        dirName (str): Directory to output to within Outputs/
        udStream (int): Distance between chromosomes.
        numFeatures (int): The number of features (utilized in the plot title)
        computeRatio (boolean): Whether to compute the ratio of two files (true) or plot a single file's coverage (false)
    """
    print("Generating clustered plot")
    y = np.array(result)
    x = np.arange(len(y))
    # plot
    fig, ax = plt.subplots()

    ax.set(xlim=(0, len(result)), xticks=np.arange(0, len(result)),
           ylim=(0, max(result)), yticks=np.arange(0, max(result) + 10))  # result[1]

    ax.set_xlabel('Distance')
    if computeRatio:
        ax.set_ylabel('log2-ratio')
    else:
        ax.set_ylabel('Coverage')

    plt.figure(figsize=(15, 10))
    plt.plot(x[(len(x) - udStream - 1):len(x) - 1],
             y[(len(x) - udStream - 1):len(x) - 1], linestyle='-.', color='red')
    plt.plot(x[0:udStream - 1], y[0:udStream - 1], linestyle='-.', color='red')
    plt.plot(x[udStream - 1:(len(x) - udStream - 1)],
             y[udStream - 1:(len(x) - udStream - 1)], color='black')
    plt.title(fname + ' (' + str(numFeatures) + ')')
    plt.xlabel('Distance')
    if computeRatio:
        plt.ylabel('log2-ratio')
    else:
        plt.ylabel('Coverage')
    plt.xticks([])

    path = fname + ".png"  # in case of single plot
    if dirName != None:
        path = 'Outputs/' + dirName + '/' + path

    plt.savefig(path, dpi=75)

