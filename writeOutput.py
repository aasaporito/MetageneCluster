from plot import genPlot
import os




#create txt list of features for a cluster
def writeNames(names, fileName, dirName):

    with open('Outputs/'+dirName+'/'+fileName , 'w') as record: 
        #write header

        #write names
        for name in names:
            line = str(name)
            record.write(line)
    record.close()  

def makeDir(name):
    newName = name
    path = 'Outputs/'+newName
    while os.path.exists(path):#path exists, create new sub file name
       num = int(newName[-1]) + 1 
       newName = name[:-1]+str(num)
       path = 'Outputs/'+newName
    
    os.makedirs(path) 
    return newName
             

    