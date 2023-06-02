"""Summary
"""
#class tree:
   


class cluster:

    """Summary
    
    Attributes:
        dataIdxs (list): Description
        distance (TYPE): Description
        left (TYPE): Description
        right (TYPE): Description
    """
    
    def __init__(self,distance=None,left=None,right=None) -> None:
        """Summary
        
        Args:
            distance (None, optional): Description
            left (None, optional): Description
            right (None, optional): Description
        """
        self.distance=distance
        self.left = left 
        self.right=right
        self.dataIdxs = []


    def addIdx(self,idx):
        """Summary
        
        Args:
            idx (TYPE): Description
        """
        self.dataIdxs.append(idx)
    


    def getIdxs(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.dataIdxs
    def isLeaf(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        if self.left == None:
            return True 
    def getRight(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.right
    def getLeft(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.left
    def getDistance(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.distance