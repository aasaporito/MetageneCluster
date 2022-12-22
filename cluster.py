

class cluster: 
    def __init__(self,data):
        #initialize random centers 

        self._centers =[]
        self._idxs=[]
        self._data=[]
        self._plus=0
        self._minus=0

    #gettrs 
    def getCenters(self):
        return self._centers
    def getIdxs(self):
        return self._idxs
    def getData(self):
        return self._data
    def strandRatio(self):
        return self._plus/(self._plus/self._minus) 
    
    def incStrand(self,strand):
        if strand =='+':
            self._plus+=1
        elif strand =='-':
            self._minus+=1 

   # def _randCenters(self): 
    
    