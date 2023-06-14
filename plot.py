"""Summary
    Provides the genPlot function to create and save feature plots.
"""
import matplotlib.pyplot as plt
import numpy as np


def genPlot(result, fname, dirName, udStream, numFeatures):
    """Summary
        Creates a plot of features using numpy and matplotlib.
    Args:
        result (list): The result to plot
        fname (str): File name to be used as the plot title
        dirName (str): Directory to output to within Outputs/
        udStream (int): Distance between chromosomes.
        numFeatures (int): The number of features (utilized in the plot title)
    """
    y = np.array(result)
    x = np.arange(len(y))

    # plot
    fig, ax = plt.subplots()

    ax.set(xlim=(0, len(result)), xticks=np.arange(0, len(result)),
           ylim=(0, max(result)), yticks=np.arange(0, max(result) + 10))  # result[1]

    ax.set_xlabel('Distance')
    ax.set_ylabel('Reads')

    plt.figure(figsize=(15, 10))
    plt.plot(x[(len(x) - udStream - 1):len(x) - 1],
             y[(len(x) - udStream - 1):len(x) - 1], linestyle='-.', color='red')
    plt.plot(x[0:udStream - 1], y[0:udStream - 1], linestyle='-.', color='red')
    plt.plot(x[udStream - 1:(len(x) - udStream - 1)],
             y[udStream - 1:(len(x) - udStream - 1)], color='black')
    plt.title(fname + ' (' + str(numFeatures) + ')')
    plt.xlabel('Distance')
    plt.ylabel('Reads')

    path = fname + ".png"  # in case of single plot
    if dirName != None:
        path = 'Outputs/' + dirName + '/' + path

    plt.savefig(path, dpi=75)
