

class cluster: 
    def __init__(self,data):
        #initialize random centers 

        self._centers =[]
        self._idxs=[]
        self._data=[]
        self._plus=[]
        self._minus=[]

    #gettrs 
    def getCenters(self):
        return self._centers
    def getIdxs(self):
        return self._idxs
    def getData(self):
        return self._data
    def strandRatio(self):
        return self._plus/(self._plus/self._minus) 
    
    def _randCenters(self):
    
    def 