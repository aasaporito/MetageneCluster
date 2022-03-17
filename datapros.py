#import gffutils




class metaGenePlot:
    def __init__(self,sam_file, gff_file):
        self.sam = sam_file 
        self.gff = gff_file

    #build chromosome arrays from gff 
    def setArray(self):
        # gffFileName = self.gff 
        # fn =gffutils.example_filename(gffFileName)
        # db = gffutils.create_db(fn, dbfn = 'test.db') #create data base
        
        # for i in db.features_of_type("mRNA"):
        #     print(i)
        numArrays= 0 
        maxLength = 0 
        currChrom=''
        with open(''+self.gff+'', "r") as gffFile:
            for line in gffFile:
                cols = line.split('\t')

                #print(cols)
                if len(cols)>1 and cols[6]=='+':
                    # if cols[0]=='chrmt':
                    #     print(line)
                    #print(cols[3], cols[4])
                    if int(cols[4]) > maxLength:
                           maxLength=int(cols[4])
                    if cols[0]!= currChrom:
                        currChrom=cols[0] 
                        numArrays+= 1


    def populateArray(self): 
        
    def normalize(self):
    



    
    #populate Arrays with sam data
    # def populateArray(self):

    
    # #pull gff arrays
    # def gffArray(self):
    
    # #normalize gff arrays to same length 
    # def normalizeArray(self): 

    # #average normalized gff arrays 
    # def averageArray(self):
    
    # #filter out overlapping trends
    # def separateTrends(self):

    # #generate plots
    # def genPlots(self):
