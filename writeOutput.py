"""Summary
"""
import os


def writeNames(names, fileName, dirName):
    """Summary
        Creates a text list of features for a given cluster

    Args:
        names (list): A list of features
        fileName (str): Name for the file
        dirName (str): Name for the output folder within Outputs/
    """
    with open('Outputs/' + dirName + '/' + fileName, 'w') as record:
        for name in names:
            line = str(name)
            record.write(line)
    record.close()


def makeDir(name):
    """Summary

    Args:
        name (TYPE): Description

    Returns:
        TYPE: Description
    """
    newName = name
    path = 'Outputs/' + newName
    while os.path.exists(path):  # path exists, create new sub file name
        num = int(newName[-1]) + 1
        newName = name[:-1] + str(num)
        path = 'Outputs/' + newName

    os.makedirs(path)
    return newName
