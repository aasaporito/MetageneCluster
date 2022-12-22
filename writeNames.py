#create txt list of features for a cluster

def writeNames(names, fileName):

    with open(fileName , 'w') as record: 
        #write header

        #write names
        for name in names:
            line = str(name)
            record.write(line)
    record.close()  