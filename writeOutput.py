from plot import genPlot
from pathlib import Path




#create txt list of features for a cluster
def writeNames(names, fileName,location):

    with open(fileName , 'w') as record: 
        #write header

        #write names
        for name in names:
            line = str(name)
            record.write(line)
    record.close()  

def makeDir(name): 
    #Path("./Outputs").mkdir(parents=True, exist_ok=True) 
    Path("./Outputs/"+name).mkdir(parents=True, exist_ok=True)