"""Summary
    Contains helper functions for saving data.
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

    print('Outputs/' + fileName + '/' + dirName)
    with open('Outputs/' + fileName + '/' + dirName, 'w') as record:
        for name in names:
            line = str(name)
            record.write(line)
    record.close()


def makeDir(name):
    """Summary
        Creates a directory within Outputs/
    Args:
        name (str): The name for the new directory. Must end in an integer.

    Returns:
        str: Returns the new path name 
    """
    newName = name
    path = 'Outputs/' + newName
    while os.path.exists(path):  # path exists, create new sub file name
        try:
            num = int(newName[-1]) + 1
            newName = newName[:-1] + " " + str(num)
        except:
            num = 1
            newName = name + " " + str(num)
        path = 'Outputs/' + newName
        print(path)

    os.makedirs(path)
    return newName
