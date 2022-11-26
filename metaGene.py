
import math
from kMeansClustering import autoKCluster, kCluster 
from plot import genPlot
from writeExcel import wtExcell
import roman
from hCluster import hCluster
from tree import cluster


#invert feature array
def invertArray(feature): 
    temp = 0 
    inverted = feature 
    for i in range(math.ceil(len(inverted)/2)):
        temp = inverted[i]
        inverted[i] = inverted[-(i+1)] 
        inverted[-(i+1)] =  temp
    return inverted

#average feature arrays at each index
def averageArray(graphArrays):
    avgArray = []
    numArray =  len(graphArrays)
    # for array in graphArrays:       ###!!!
    #     for i in range(len(array)): 
    #         avgArray[i]+= array[i]
    # for j in range(len(avgArray)):
    #     avgArray[j]=avgArray[j]/numArray

    for i in range(len(graphArrays[0])):
        indxTot=0
        for array in graphArrays: 
            indxTot+= array[i]
        avgArray.append(indxTot/numArray)
    return avgArray

#average up/down arrays
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

#a class to create metagene plots based on SAM and GFF/GFT
#requires compatible chromosome labels 
class metaGenePlot:
    def __init__(self,sam_file:str, gff_file:str, featureType:str, udStream:int = 0,sorted=True):
        self.__samLines, self.__gffLines=self.__parseData(sam_file,gff_file) #set file variables
        self.__samLength = len(self.__samLines)#for tracking progress 
        self.__gffLength = len(self.__gffLines)
        self.gff = gff_file #file names
        self.sam = sam_file
        self.feature= featureType 
        self.names=[] #names of instances of given feature 
        self.__upDown = udStream #up down stream distance 
        self.data = [] #raw data 
        self.plotData = [] #normalized data 
        self.__progress = 0 #track progress of data collecting
        self.__chrom=None 
        self.__upDownStream=[] #up down stream data tuples

    #sort input file variables by chromosome --- right now this is used to divide sam by chromosome
    def sort(self,files='a'): 
    #  create dict ent for each chrom     ie chr1:[]
        chroms ={}
        for line in self.__samLines: # go through file and add each line to respective chrom array 
            cols = line.split('\t')
            if len(cols)>=10 and len(cols[2])<8:
                chrom = cols[2]
                if chrom in chroms:
                    chroms[chrom].append(line)
                else:
                    chroms[chrom]= []
                    chroms[chrom].append(line)

        self.__samLines = chroms 

        ###################################################
    # append the arrays for each chrom to eachother in proper order 
        # sortedLines =[]
        # if 'chr1' not in chroms: #convert from roman 
        #     gffChroms ={}
    
        #     for key in chroms:
        #         num = key[3:]
        #         try:
        #             val = roman.fromRoman(num)
        #             intChroms[val] = chroms[key]
                    
        #         except:
        #             strChroms[key] = chroms[key]
        #     for key in sorted(intChroms):
        #         sortedLines+= intChroms[key]
        #     for key in sorted(strChroms):
        #         sortedLines+=strChroms[key]
        # self.__samLines=sortedLines #sorted

        # for line in self.__samLines:
        #     print(line)
       ####################################################

    def __parseData(self,sam,gff): #read files into arrays

        with open(sam, 'r') as samFile:
            samLines = samFile.readlines()
        samFile.close()

        with open(gff) as gffFile: 
            gffLines = gffFile.readlines()
        gffFile.close()

        return samLines, gffLines
    

    def __getChromLength(self): #find max length and sort gff lines by chrom 
        maxLength = 0
        firstChrom =None 
        chroms = {}

        for i,line in enumerate(self.__gffLines):
            cols = line.split('\t')
            if len(cols)>1 and len(cols[0])<8:
                chrom = cols[0]
                if chrom in chroms:
                    chroms[chrom].append(line)
                else:
                    chroms[chrom]= []
                    chroms[chrom].append(line)

            if (len(cols)>1) and int(cols[4]) > maxLength: #and  (cols[6]=='+' ):#or cols[6] == '-') : # and cols[6]=='+' #skip the rows at the bottom 
               
                #farthest poi in chromosome
                maxLength=int(cols[4])
                if firstChrom==None: 
                    firstChrom = cols[0] 
                    loc = i
                
        self.__gffLines = chroms 

        #initialize nt positions
        self.__chrom = []
        for i in range(maxLength+self.__upDown): 
            self.__chrom.append(0)
       # print(len(self.__chrom))
    
    
    def testSort(self): 
        self.sort()
        firstChrom, loc = self.__getChromLength()
        gffKeys= []
        samKeys = []
        for key in self.__gffLines: 
            gffKeys.append(key)
        for key in self.__samLines: 
            samKeys.append(key)

        print('gff chroms ',gffKeys)
        print('sam chroms ', samKeys)



        
    def __populateChromosome(self,chrom): #populate current chrom with sam data 
        for line in self.__samLines[chrom]:
            cols = line.split('\t') 
            if len(cols)>=10:
                start,seqLength= int(cols[3]),len(cols[9]) # postion and sequence length
                end = start + seqLength -1
                for j in range(start-1, end):
                    try: 
                        self.__chrom[j]+= 1
                    except:
                        continue #print(j)
        print('populated ',chrom)


    def __getGffArrays(self,chrom): 
        for line in self.__gffLines[chrom]:
            cols = line.split('\t') 
            if len(cols)>1  and cols[2]== self.feature: # #if feature of interest 
                currArray=[]
                dwnStream = []
                upStream =[]
                start, end =  int(cols[3])-1 , int(cols[4])-1
                down = start- self.__upDown
                up = end + self.__upDown
                if end-start >= 10: #some CDS in hg38 had length 0
                #get feature values 
                    for i in range(start, end-1):
                        currArray.append(self.__chrom[i])#pull the values from the chromDIct to build new array

                    #get down stream values 
                    for i in range(down, start):
                        dwnStream.append(self.__chrom[i])
                    #get up stream values 
                    for i in range(end, up):
                        try:
                            upStream.append(self.__chrom[i])
                        except: 
                            upStream.append(0)

                    if  cols[6]=='-':
                        currArray = invertArray(currArray) #invert feature array
                        temp= invertArray(dwnStream) #invert and flip up/down stream 
                        dwnStream = invertArray(upStream)
                        upStream = temp


                    self.__upDownStream.append((dwnStream,upStream))
                    self.data.append(currArray)
                    self.names.append(cols[8])
        print('gatherd ',chrom,' data')
        

    def __resetChrom(self): 
        for i in range(len(self.__chrom)):
            self.__chrom[i]=0


    def __buildData(self): #gather metagene data for each chrom
        self.__getChromLength()
        self.sort()
        
        for chrom in self.__gffLines:
            if chrom in self.__samLines: 
                self.__populateChromosome(chrom)
                self.__getGffArrays(chrom) 
                self.__resetChrom()
     
        
     ##################################################################################           
    # def __populateChromosome(self,loc,currChrom): #get sam data for current chrom 
    #     i = loc
    #     firstLine =self.__samLines[loc]
    #     nextCols = firstLine.split('\t') 
    #     nextChrom = currChrom

    #     while nextChrom == currChrom: 
    #         # if i//1000 == 0: #track progress
    #         #     completion = (i/self.__samSize)*100
    #         #     print('\r            \r', end='',flush=True)
    #         #     print("Populating chromosomes... "+ str(round(completion,2)) + '% ', end='',flush=True)
                
    #         cols = nextCols
    #         if len(cols)>=10:
    #             start,seqLength= int(cols[3]),len(cols[9]) # postion and sequence length
    #             end = start + seqLength -1
    #             for j in range(start-1, end):
    #                 self.__chrom[j]+= 1
    #         #go to next line
    #         i+=1 
    #         if i < len(self.__samLines): 
    #             nextLine = self.__samLines[i]
    #             nextCols = nextLine.split('\t')
    #             nextChrom = cols[2]
    #         else: #reached end of doc
    #             nextChrom = None

    #     print('populated ',currChrom)
    #     return nextChrom, i 


    # def __getGffArrays(self,loc,currChrom): # find feature arrays in curr chrom and add to data
    #     upDownStream= [] # 2d array, first is down (left) second is up (right) corresponding to the gffArray of the same index
    #     i = loc
    #     firstLine =self.__gffLines[loc]
    #     nextCols = firstLine.split('\t') 
    #     nextChrom = currChrom
    #     while nextChrom ==currChrom: 

    #         cols = nextCols
    #         if len(cols)>1  and cols[2]== self.feature: #and (cols[6]=='+' ):#or cols[6] == '-'): # #if feature of interest 
    #             currArray=[]
    #             dwnStream = []
    #             upStream =[]
    #             start, end =  int(cols[3])-1 , int(cols[4])-1 # get chromosome, start/end locations
    #             down = start- self.__upDown
    #             up = end + self.__upDown

    #             #get feature values 
    #             for i in range(start, end):
    #                 currArray.append(self.__chrom[i])#pull the values from the chromDIct to build new array

    #             #get down stream values 
    #             for i in range(down, start):
    #                 dwnStream.append(self.__chrom[i])
    #             #get up stream values 
    #             for i in range(end, up):
    #                 try:
    #                     upStream.append(self.__chrom[i])
    #                 except: 
    #                     upStream.append(0)

    #             if  cols[6]=='-':
    #                 currArray = invertArray(currArray) #invert feature array
    #                 temp= invertArray(dwnStream) #invert and flip up/down stream 
    #                 dwnStream = invertArray(upStream)
    #                 upStream = temp


    #             self.__upDownStream.append((dwnStream,upStream))
    #             self.data.append(currArray)
    #             self.names.append(cols[8])
                
    #             #go to next line
    #         i+=1 
    #         if i < len(self.__gffLines): 
    #             nextLine = self.__gffLines[i]
    #             nextCols = nextLine.split('\t')
    #             nextChrom =  cols[0]
    #         else: #reached end of file
    #             nextChrom =None  
    #     print('fetched ', currChrom)
    #     return nextChrom, i 
        
    # def buildData(self):  #private?    gather plot data one chromosome at a time
        
    #     currChrom,gffLoc = self.__getChromLength() #initialize chrom 

    #     for i in range(len(self.__samLines)): #skip headers
    #         cols = self.__samLines[i].split('\t')
    #         if len(cols)>=10:
    #             samLoc = i 
    #             break
       
       
    #     end = False
    #     while end == False: #for each chromosome/until end of files is reached
    #         #populate self.__chrom  with sam data  
    #         nextSamChrom , nextSamLoc = self.__populateChromosome(samLoc, currChrom)
    #         #print(nextSamChrom)
    #         #pull gffArrays and add to self.data 
    #         nextGffChrom, nextGffLoc = self.__getGffArrays(gffLoc, currChrom)
    #         #print(nextGffChrom)
    #         #check for compatibility 
    #         if nextGffChrom!= nextSamChrom:
    #             print("Please ensure input files are sorted and compatible.")
    #             break 
    #         else: #reset chrom -> move to next
    #             print(currChrom, ' completed')
    #             currChrom = nextSamChrom
    #             samLoc = nextSamLoc
    #             gffLoc = nextGffLoc 
                
    #             for i in range(len(self.__chrom)): 
    #                 self.__chrom[i] = 0 

    #         #check for end of file
    #         # if gffLoc >= len(self.__gffLines) and samLoc>= len(self.__samLines): 
    #         #     end = True
    #         if nextGffChrom == None and nextSamChrom== None: 
    #             print('end')
    #             end = True

        #normalize as usual



###----------------------- old way of building data that I don't wanna get rid of just in case --------------------------###

    # def setArray(self):
    #     numArrays= 0 
    #     maxLength = 0 #add maxLength for each unique chrom 
    #     currChrom=''
    #     chromDict={}
    #     romanNums = False
    #     with open(self.gff, "r") as gffFile:
    #         for line in gffFile:
    #             cols = line.split('\t')
               
    #             if len(cols)>1: #and  (cols[6]=='+' ):#or cols[6] == '-') :#skip the rows at the bottom 
    #                 #print(cols[3], cols[4]
    #                 if int(cols[4]) > maxLength: #farthest poi in chromosome
    #                         maxLength=int(cols[4])
    #                 if cols[0]!= currChrom: # crhomosome number
    #                     currChrom=cols[0] 
    #                     numArrays+= 1
    #                     chromDict[cols[0]]=[] #create new dict entry for each chrom
    #     gffFile.close()
    #     for key in chromDict:
    #         arrLen= []
    #         for i in range(maxLength):
    #             arrLen.append(0)
    #         chromDict[key]= arrLen #initialize each chrom array with 0s to len(maxLength)
    #     self.chromDict = chromDict   

    # #populate Arrays with SAM data
    # def populateArray(self): 
    #     with open(self.sam, 'r') as samFile:
    #         #init progress tracking vars
    #         progress = 0 
    #         size = os.path.getsize(self.sam)
    
    #         for i,line in enumerate(samFile): 
    #             cols = line.split('\t')
    #             if len(cols)>=10:
    #                 chrom,start,seqLength= cols[2],int(cols[3]),len(cols[9]) #get chrom number, postion and sequence length
    #                 if chrom[3] =='Y' or chrom[3] =='X': 
    #                     chrom = chrom[0:4]
    #                 else:
    #                     chrom = chrom[0:5]

    #                 end = start + seqLength -1 
    #                 try:    #try to find the chromosomes defined in the GFF, else throw incompatible error and end run
    #                     for i in range(start-1, end):
    #                             self.chromDict[chrom][i]+= 1
    #                 except: 
    #                     print("Please ensure input files are compatible.")
    #                     break 
                    
    #                 ####track percent complete####
    #                 progress += len(bytes(line, encoding='utf-8'))
    #                 if i%10000 == 0: 
    #                     completion = (progress/size)*100
    #                     print('\r            \r', end='',flush=True)
    #                     print("Populating chromosomes... "+ str(round(completion,2)) + '% ', end='',flush=True)
                        
    #     samFile.close()
        
    #     print('\r  Populating chromosomes... Done    \r', end='',flush=True)
    #     ##("Populating chromosomes... "+ "Done")
                        
    # # #pull gff arrays
    # def getGffArray(self):
    #     gffArrays = []
    #     names=[]
    #     upDownStream= [] # 2d array, first is down (left) second is up (right) corresponding to the gffArray of the same index
    #     with open(self.gff, "r") as gffFile:
    #         for line in gffFile:
    #             cols = line.split('\t')

    #             if len(cols)>1  and cols[2]== self.feature and (cols[6]=='+' ):#or cols[6] == '-'): # #if feature of interest 
    #                 currArray=[]
    #                 dwnStream = []
    #                 upStream =[]
    #                 chrom, start, end = cols[0], int(cols[3])-1 , int(cols[4])-1 # get chromosome, start/end locations
    #                 down = start- self.upDown
    #                 up = end + self.upDown

    #                 #get feature values 
    #                 for i in range(start, end):
    #                     currArray.append(self.chromDict[chrom][i])#pull the values from the chromDIct to build new array
    #                     if self.chromDict[chrom][i]!=0:
    #                         zeros = False
    #                 #get down stream values 
    #                 for i in range(down, start):
    #                     dwnStream.append(self.chromDict[chrom][i])
    #                 #get up stream values 
    #                 for i in range(end, up):
    #                     try:
    #                         upStream.append(self.chromDict[chrom][i])
    #                     except: 
    #                        upStream.append(0)

    #                 if  cols[6]=='-':
    #                     currArray = invertArray(currArray) #invert feature array
    #                     temp= invertArray(dwnStream) #invert and flip up/down stream 
    #                     dwnStream = invertArray(upStream)
    #                     upStream = temp
    #                 upDownStream.append((dwnStream,upStream))
    #                 gffArrays.append(currArray)
    #                 names.append(cols[8])
                    

    #     gffFile.close()
    #     self.upDownStream = upDownStream
    #     self.gffArrays= gffArrays
    #     self.names=names

###---------------------------------------------------------------------------------------------------------------###
    



    # #normalize gff arrays to same length 
    def __normalizeArray(self, targetLength):
        if targetLength== 'avg':  #find average array length
            avg = 0 
            for array in self.data:
                avg+= len(array)
            avg= avg/(len(self.data))
            targetLength=round(avg) 
        
        graphArrays =[]
        for array in self.data:
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


    #divide into cluster and plot methods
    def plot(self, numClusters:int,length:int, clusterUpDown:bool =False , clusterAlgo='k'): #call to generate plot(s) after creating metaGenePlot object


        self.__buildData()

        print("Normalizing feature length...")
        trendData=self.__normalizeArray(length)

        if clusterAlgo =='k':
            if numClusters==1: #for one cluster just average all data
                avgArray=averageArray(trendData)  
            
                print("Plotting data...")
                name=self.gff[0:-4]+' '+self.feature
                if self.__upDown> 0: #include existing up/down stream data
                    avgDown,avgUp = averageUpDown(self.__upDownStream)
                    print(len(avgDown), len(avgArray),len(avgUp))
                    fullArray = avgDown+avgArray+avgUp 
                else:
                    fullArray = avgArray
                genPlot(fullArray,name,self.__upDown)
                return
            elif(numClusters =='auto'):  #find the optimal number of cluster for the given data
                print("Fitting data...") 
                print('features:', len(trendData))
                clusters = autoKCluster(trendData)
            else: #divide data into fixed number clusters
                print("Fitting data...")
                clusters, distance = kCluster(numClusters, trendData)
            
            # clusterNames=[]
            # for i,cluster in enumerate(clusters):
            #     clusterData = []
            #     featureNames=[]
            #     name=self.gff[0:-4]+' '+self.feature+' cluster '+str(i)
            #     for feature in cluster: 
            #         featureNames.append(self.names[feature])
            #         if self.__upDown> 0 and clusterUpDown==False:
            #             featureData = self.__upDownStream[feature][0]+trendData[feature]+self.__upDownStream[feature][1]
            #             clusterData.append(featureData)      
            #         else:
            #             clusterData.append(trendData[feature])

            #     clusterNames.append(featureNames)
                
            #     avgArray=averageArray(clusterData)
            # # avgDown,avgUp = averageUpDown(self.upDownStream)
            #     # if self.upDown> 0 and clusterUpDown==False:
            #     #     print(len(avgDown), len(avgArray),len(avgUp))
            #     #     fullArray = avgDown+avgArray+avgUp 
            #     # else:
            #     #     fullArray = avgArray
            #     print("Plotting data...",len(cluster))
            #     genPlot(avgArray,name,self.__upDown)
            #     #enPlot(clusterCenters[i],name)
            # wtExcell(clusterNames,self.gff)
        elif clusterAlgo=='h':
            print('hCluster')
            nodes = hCluster(numClusters,trendData)
            clusters =[]
            for node  in nodes:
                data = node.getIdxs()
                clusters.append(data)
                

            
        clusterNames=[]
        for i,cluster in enumerate(clusters):
            clusterData = []
            featureNames=[]
            name=self.gff[0:-4]+' '+self.feature+' cluster '+str(i)
            for feature in cluster: 
                featureNames.append(self.names[feature])
                if self.__upDown> 0 and clusterUpDown==False:
                    featureData = self.__upDownStream[feature][0]+trendData[feature]+self.__upDownStream[feature][1]
                    clusterData.append(featureData)      
                else:
                    clusterData.append(trendData[feature])

            clusterNames.append(featureNames)
            
            avgArray=averageArray(clusterData)
        # avgDown,avgUp = averageUpDown(self.upDownStream)
            # if self.upDown> 0 and clusterUpDown==False:
            #     print(len(avgDown), len(avgArray),len(avgUp))
            #     fullArray = avgDown+avgArray+avgUp 
            # else:
            #     fullArray = avgArray
            print("Plotting data...",len(cluster))
            genPlot(avgArray,name,self.__upDown)
            #enPlot(clusterCenters[i],name)
        wtExcell(clusterNames,self.gff)


