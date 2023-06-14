"""Summary

"""
from Extras.tree import cluster

#cal distance between two data points 
def calcDistance(data1,data2):
    """Summary
    
    Args:
        data1 (TYPE): Description
        data2 (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    if len(data1)!= len(data2):
        print('Data lengths not compatible.')
        return
    distance = 0 
    for i in range(len(data1)):
        distance+= abs(data1[i]-data2[i])
    
    return distance
        
# build distance matrix from data
def calcMatrix(data): 
    """Summary
    
    Args:
        data (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    distMatrix =[[] for i in range(len(data))]
    for i,feature1 in enumerate(data):
        for j,feature2 in enumerate(data):
            if i!=j: 
                distance = calcDistance(feature1,feature2)
                distMatrix[i].append(distance)
            else:
                distMatrix[i].append(0)
    return distMatrix

#find nearest clusters 
def findNextPair(distMatrix): 
    """Summary
    
    Args:
        distMatrix (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    minDist=distMatrix[0][1]
    nearestPair = [0,1]
    for i in range(len(distMatrix)):
        for j in range(len(distMatrix)): 
            if distMatrix[i][j]< minDist and i!=j:
                nearestPair=[i,j]
                minDist = distMatrix[i][j]
    return nearestPair, minDist

#shrink matrix based on last cluster
def reduceMatrix(pair,distMatrix): #pair => int for each cluster index
    """Summary
    
    Args:
        pair (TYPE): Description
        distMatrix (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    newMatrix =[[] for i in range(len(distMatrix)-1)]
    for i in range(len(distMatrix)):
        if i>= pair[1]: 
            col = i -1 
        else: 
            col = i

        for j in range(len(distMatrix)):
            if i == pair[1] or j == pair[1]:
                continue
            elif i == j:
                newMatrix[col].append(-1)
            elif i not in pair and j not in pair: #not in cluster, copy val 
                newMatrix[col].append(distMatrix[i][j])
            elif j == pair[0] :   #if first in pair, replace row/col with combined (avg)or j == pair[0]:
                #col
                avgVal = (distMatrix[i][pair[0]] + distMatrix[i][pair[1]])/2
                newMatrix[col].append(avgVal)
            # elif j == pair[0]: #row
            elif i ==pair[0]:
                avgVal = (distMatrix[j][pair[0]] + distMatrix[j][pair[1]])/2
                newMatrix[col].append(avgVal)
           
    return newMatrix 

 #shift element at idx to end of array    
def shiftArray(array,idx): 
    """Summary
    
    Args:
        array (TYPE): Description
        idx (TYPE): Description
    """
    i = idx
    while i <len(array)-1:
        temp = array[i] 
        array[i] = array[i+1] 
        array[i+1] = temp 
        i+=1 

#combine clusters and shrink cluster array
def combineClusters(pair,dist,clusters): 
    """Summary
    
    Args:
        pair (TYPE): Description
        dist (TYPE): Description
        clusters (TYPE): Description
    """
    leftBranch = clusters[pair[0]]
    rightBranch = clusters[pair[1]]

    newCluster =  cluster(dist,leftBranch,rightBranch)
    idxs = leftBranch.getIdxs() + rightBranch.getIdxs()

    for idx in idxs:
        newCluster.addIdx(idx)

    clusters[pair[0]] = newCluster
    
    shiftArray(clusters,pair[1])

def divideClusters(numClusters,root): #add depth
    """Summary
    
    Args:
        numClusters (TYPE): Description
        root (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    clusters = []
    #very likely only works for up to three clusters
    if numClusters == 2:
        clusters.append(root.getLeft())
        clusters.append(root.getRight())
    elif numClusters== 1:
        clusters.append(root)
    else: 
        if root.getLeft().isLeaf():
            clusters.append(root.getLeft())
            subClusters = divideClusters(numClusters-len(clusters),root.getRight())
            clusters+=subClusters
        elif root.getRight().isLeaf():
            clusters.append(root.getRight())
            subClusters = divideClusters(numClusters-len(clusters),root.getLeft())
            clusters+=subClusters
        elif root.getLeft().getDistance()>root.getRight().getDistance():
            clusters.append(root.getRight())
            subClusters = divideClusters(numClusters-len(clusters),root.getLeft())
            clusters+=subClusters
        else:
            clusters.append(root.getLeft())
            subClusters = divideClusters(numClusters-len(clusters),root.getRight())
            clusters+=subClusters
            
    return clusters




#cluster all data into one tree, then split to form clusters 
def hCluster(numClusters,data):
    """Summary
    
    Args:
        numClusters (TYPE): Description
        data (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    #create node for each feature
    clusters= []
    for i in range(len(data)):
        leaf = cluster()
        leaf.addIdx(i) 
        clusters.append(leaf) 
        
    
    distMatrix = calcMatrix(data)
    n = len(distMatrix)
    while n>1:
       
        nextPair,dist = findNextPair(distMatrix) #find next cluster 

        #combine clusters
        combineClusters(nextPair,dist,clusters)

        #shrink matrix to accomadate clustered pair
        distMatrix = reduceMatrix(nextPair,distMatrix)
        
        n-=1 
    
    #split tree into clusters 
    clusters= divideClusters(numClusters,clusters[0])
    return clusters
   