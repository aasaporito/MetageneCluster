#class tree:
   


class cluster:
    def __init__(self,distance=None,left=None,right=None) -> None:
        self.distance=distance
        self.left = left 
        self.right=right
        self.dataIdxs = []


    def addIdx(self,idx):
        self.dataIdxs.append(idx)
    


    def getIdxs(self):
        return self.dataIdxs
    def isLeaf(self):
        if self.left == None:
            return True 
    def getRight(self):
        return self.right
    def getLeft(self):
        return self.left
    def getDistance(self):
        return self.distance