"""Summary
"""
import os


# create txt list of features for a cluster
def writeNames(names, fileName, dirName):
    """Summary

    Args:
        names (TYPE): Description
        fileName (TYPE): Description
        dirName (TYPE): Description
    """
    with open('Outputs/' + dirName + '/' + fileName, 'w') as record:
        # write header

        # write names
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
