
from audioop import avg
import math
from operator import inv


from numpy import full
from kMeansClustering import autoKCluster, kCluster 
from plot import genPlot
from writeExcel import wtExcell

def invertArray(feature): 
    temp = 0 
    inverted = feature 
    for i in range(math.ceil(len(inverted)/2)):
        temp = inverted[i]
        inverted[i] = inverted[-(i+1)] 
        inverted[-(i+1)] = temp
    return inverted


def averageArray(graphArrays):
    avgArray = []
    for i in range(len(graphArrays[0])):
        avgArray.append(0)
    numArray =  len(graphArrays)
    for array in graphArrays:
        for i in range(len(array)): 
            avgArray[i]+= array[i]
    for j in range(len(avgArray)):
        avgArray[j]=avgArray[j]/numArray
    return avgArray


def averageUpDown(upDownStream):
    
    upArray = []
    downArray =[]
    for i in range(len(upDownStream[0][0])):
        upArray.append(0)
        downArray.append(0)
    numArray =  len(upDownStream)
    for pair in upDownStream:
        for i in range(len(upDownStream[0][0])): 
            upArray[i]+= pair[1][i]
            downArray[i]+= pair[0][i]

    for j in range(len(upArray)):
        upArray[j]=upArray[j]/numArray
        downArray[j] = downArray[j]/numArray

    return downArray , upArray



class metaGenePlot:
    def __init__(self,sam_file, gff_file, featureType, udStream = 0):
        self.sam = sam_file 
        self.gff = gff_file
        self.feature= featureType
        self.names=[]
        self.chromDict={} 
        self.upDown = udStream
        #self.chromDict, self.romanNums = setArray(self.gff, self.feature)


    #build chromosome arrays from gff 
   
    def setArray(self):
        numArrays= 0 
        maxLength = 0 #add maxLength for each unique chrom 
        currChrom=''
        chromDict={}
        romanNums = False
        with open(self.gff, "r") as gffFile:
            for line in gffFile:
                cols = line.split('\t')
                #print(cols)
                if len(cols)>1 and  (cols[6]=='+' ):#or cols[6] == '-') : # and cols[6]=='+' #skip the rows at the bottom and check if the sequence is read forwards
                    #print(cols[3], cols[4])
                    # if cols[0][3] == 'I':
                    #     romanNums = True
                    if int(cols[4]) > maxLength: #farthest poi in chromosome
                            maxLength=int(cols[4])
                    if cols[0]!= currChrom: # crhomosome number
                        currChrom=cols[0] 
                        numArrays+= 1
                        chromDict[cols[0]]=[] #create new dict entry for each chrom
        gffFile.close()
        for key in chromDict:
            arrLen= []
            for i in range(maxLength):
                arrLen.append(0)
            chromDict[key]= arrLen #innitialize each chrom array with 0s to len(maxLength)
        self.chromDict = chromDict   

    #populate Arrays with sam data
    def populateArray(self):
        romanNums = False
        with open(self.sam, 'r') as samFile:
            for line in samFile:
                cols = line.split('\t')
                if len(cols)>=10:
                    chrom,start,seqLength= cols[2],int(cols[3]),len(cols[9]) #get chrom number, postion and sequence length
                    if chrom[3] =='Y' or chrom[3] =='X': 
                        chrom = chrom[0:4]
                    else:
                        chrom = chrom[0:5]
                    # try:
                    #     int(chrom[3:])
                    # except:
                    #     romanNums =True
                    end = start + seqLength -1 
                    # if self.romanNums != romanNums and romanNums == False: 
                    #     #convert SAM chrom labels from int to roman
                    #     chrom = intToRoman(chrom[3:])
                    # elif self.romanNums != romanNums  and romanNums == True: 
                    #     #convert SAM chrom labels from roman to int
                    #     chrom = romanToInt(chrom[3:])

                        
                    for i in range(start-1, end):
                        self.chromDict[chrom][i]+= 1
                  
        samFile.close()

    def testArrays(self):
        self.setArray()
        self.populateArray()
        print(self.chromDict['chrI'])

    
    # #pull gff arrays
    def getGffArray(self):
        gffArrays = []
        names=[]
        upDownStream= [] # 2d array, first is down (left) second is up (right) corresponding to the gffArray of the same index
        with open(self.gff, "r") as gffFile:
            for line in gffFile:
                cols = line.split('\t')

                if len(cols)>1  and cols[2]== self.feature and (cols[6]=='+' ):#or cols[6] == '-'): # #if feature of interest 
                    currArray=[]
                    dwnStream = []
                    upStream =[]
                    chrom, start, end = cols[0], int(cols[3])-1 , int(cols[4])-1 # get chromosome, start/end locations
                    down = start- self.upDown
                    up = end + self.upDown

                    for i in range(start, end):
                        currArray.append(self.chromDict[chrom][i])#pull the values from the chromDIct to build new array
                    
                    for i in range(down, start):
                        dwnStream.append(self.chromDict[chrom][i])

                    for i in range(end, up):
                        try:
                            upStream.append(self.chromDict[chrom][i])
                        except: 
                            upStream.append(0)

                    # if  cols[6]=='-':
                    #     currArray = invertArray(currArray)

                    upDownStream.append((dwnStream,upStream))
                    gffArrays.append(currArray)#add to array of arrays 
                    names.append(cols[8])
                    

        gffFile.close()
        self.upDownStream = upDownStream
        self.gffArrays= gffArrays
        self.names=names
        # for i in range(10): 
        #     print(len(self.upDownStream[i][0]) , len(self.upDownStream[i][1]))
    
    def testgffArrays(self):
        self.setArray()
        self.populateArray()
        self.getGffArray()
        print('gffLength:', len(self.gffArrays))
        lengths= []
        for el in self.gffArrays:
            length = len(el)
            lengths.append(length) 
        print(lengths)    
    
    # #normalize gff arrays to same length 
    def normalizeArray(self, targetLength):
        if targetLength== 'avg': 
            avg = 0 
            for array in self.gffArrays:
                avg+= len(array)
            avg= avg/(len(self.gffArrays))
            targetLength=avg
        
        graphArrays =[]
        for array in self.gffArrays:
            
            currArray=[]
            stepSize = len(array)/targetLength
            step = 0
            prev = 0 

            if (stepSize < 1):  #stretch
                while len(currArray) < targetLength: 
                    prev = step 
                    step+= stepSize
                    
                    if math.floor(step)== math.ceil(step):  #reached a whole number step
                        currArray.append(array[int(step)-1])
                    
                    elif (math.ceil(prev) == math.floor(step))  and prev!= 0: #step cross an integer -> perform weighted average
                        
                        weight1 = ((math.ceil(prev)-prev)/stepSize)*array[int(math.floor(prev))]
                        if math.floor(step)<len(array):
                            weight2 = ((step-math.ceil(prev))/stepSize)*array[int(math.floor(step))]
                        else:
                            weight2 = ((step-math.ceil(prev))/stepSize)*array[int(math.floor(step)-1)]
                        #print(weight1, weight2 )

                        avg = weight1 + weight2
                        currArray.append(avg)
                    

                    else: #not a whole number step but hasnt crossed an integer 
                        currArray.append(array[int(math.floor(step))])
            
            elif (stepSize>1): #shrink 
                while len(currArray) < targetLength: 
                    prev = step
                    step+= stepSize 
                    
                    i = prev
                    x = 0 
                    frac= math.ceil(prev)-prev
                    if frac == 0:
                        frac = 1
                    
                    x+= array[math.floor(i)]*frac 
                   
                    i+=frac
                    
                    while i < step-1:#include all the whole values spanned by the step 
                        if i < len(array):
                            x+= array[math.floor(i)]
                        
                        i+=1 
                    frac= step - math.floor(step)
                    if frac ==0:
                        frac=1
                    
                    if i < len(array):
                        x+= array[math.floor(i)]*frac

                    # if (step+stepSize)>targetLength:#accout for extra portion of last value
                    #     frac= targetLength-step
                    #     x+= array[math.floor(i)]*frac
                    
                    avg = x/stepSize 
                    currArray.append(avg)
                
            else: #same length
                currArray = array 

            graphArrays.append(currArray)
        return graphArrays             

    # #average normalized gff arrays (see top) 

    def plot(self, numClusters,length, clusterUpDown =False): #call to generate plot(s) after creating metaGenePlot object

        print("Setting chromosome arrays...")
        self.setArray()
        print(list((self.chromDict.keys())))
        print("Populating chromosomes...")
        self.populateArray()

        print("Identifying signals of interest...")
        self.getGffArray()

        print("Normalizing feature length...")
        trendData=self.normalizeArray(length)

        if numClusters==1: 
            avgArray=averageArray(trendData)
            avgDown,avgUp = averageUpDown(self.upDownStream)
           
            print("Plotting data...")
            name=self.gff[0:-4]+' '+self.feature
            if self.upDown> 0:
                print(len(avgDown), len(avgArray),len(avgUp))
                fullArray = avgDown+avgArray+avgUp 
            else:
                fullArray = avgArray
            genPlot(fullArray,name,self.upDown)
            return
        elif(numClusters =='auto'): 
            print("Fitting data...") 
            print('features:', len(trendData))
            clusters = autoKCluster(trendData)
        else: #divide data into clusters
            print("Fitting data...")
            clusters, distance = kCluster(numClusters, trendData)
           
        clusterNames=[]
        for i,cluster in enumerate(clusters):
            clusterData = []
            featureNames=[]
            name=self.gff[0:-4]+' '+self.feature+' cluster '+str(i)
            for feature in cluster:
                clusterData.append(trendData[feature])
                featureNames.append(self.names[feature])
            clusterNames.append(featureNames)
                
            avgArray=averageArray(clusterData)
            avgDown,avgUp = averageUpDown(self.upDownStream)
            if self.upDown> 0:
                print(len(avgDown), len(avgArray),len(avgUp))
                fullArray = avgDown+avgArray+avgUp 
            else:
                fullArray = avgArray
            print("Plotting data...",len(cluster))
            genPlot(avgArray,name,self.upDown)
            #enPlot(clusterCenters[i],name)
        wtExcell(clusterNames,self.gff)

# def getFeatures(self): # call to check existing features and their proper syntax
#             features = []
#             with open(gff_File, "r") as gffFile:
#                 for line in gffFile:
#                     cols = line.split('\t')
#                     if len(cols)>1 and cols[2] not in features:
#                         features.append(cols[2])
#             gffFile.close()
#             print("\nThis feature is not found in "+gff_File+". Please refer to the list below for possible features.\n")
#             print(features)                        

            



