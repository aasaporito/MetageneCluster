"""Summary
    Cluster node class for storage in a tree structure
"""


class cluster:

    """Summary
        Cluster node class.

    Attributes:
        dataIdxs (list): List of data IDs (Used as node names)
        distance (int): Distance
        left (cluster): Left node
        right (cluster): Right node
    """

    def __init__(self, distance=None, left=None, right=None) -> None:
        """Summary
            Standard constructor for cluster
    
        Args:
            distance (int, optional): Distance
            left (cluster, optional): Left cluster in the tree from current
            right (cluster, optional): Right cluster in the tree from current
        """
        self.distance = distance
        self.left = left
        self.right = right
        self.dataIdxs = []

    def addIdx(self, idx):
        """Summary
            Adds an id to the dataIdxs list

        Args:
            idx (int): Integer to identify an entry
        """
        self.dataIdxs.append(idx)

    def getIdxs(self):
        """Summary
            Gets idxs
        Returns:
            list: 
        """
        return self.dataIdxs

    def isLeaf(self):
        """Summary
            Checks if the cluster is a leaf

        Returns:
            bool: Returns true or None
        """
        if self.left == None:
            return True

    def getRight(self):
        """Summary
            Gets the cluster to the right

        Returns:
            cluster: Cluster to the right
        """
        return self.right

    def getLeft(self):
        """Summary
            Gets the cluster to the left

        Returns:
            cluster: Cluster to the left
        """
        return self.left

    def getDistance(self):
        """Summary
            Gets the distance
        Returns:
            int: Distance
        """
        return self.distance
