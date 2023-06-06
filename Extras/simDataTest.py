"""Summary
    Script for running a simulated data test. Data may be clustered
    using different clustering algorithms as well as plotted pre clustering.
"""
from Extras.hCluster import hCluster
from kMeansClustering import kCluster
from plot import genPlot
from metaGene import averageArray

###test clustering algos on simulated data

#read sim data
simData = []
firstHalf =[]
secondHalf =[]
with open('simData2.txt','r') as df:
    for i,line in enumerate(df):
        newLine = line.replace('[','').replace(']\n','')
        vals = newLine.split(', ')
        simData.append([float(vals[i]) for i in range(len(vals))])
        # if i < 50:
        #     firstHalf.append([float(vals[i]) for i in range(len(vals))])
        # else:
        #     secondHalf.append([float(vals[i]) for i in range(len(vals))])


### pre-cluster visulaization ###
# fullData = averageArray(simData)
# genPlot(fullData,'simNoCluster2',0)

# first = averageArray(firstHalf)
# genPlot(first,'firstNoCluster2',0)

# second = averageArray(secondHalf)
# genPlot(second,'secondNoCluster2',0)

# fullData =[first,second]
# full = averageArray(fullData)
# genPlot(full,'simNoCluster2',0)
#-------------------------------------#

### HClustering ####
nodes = hCluster(3,simData)

clusters =[]
for node  in nodes:
    data = node.getIdxs()
    clusters.append(data)
#----------------------#

###kmeans clustering###
#clusters,x = kCluster(2,simData)
#-------------------------------------#


#extract cluster data 
for i,cluster in enumerate(clusters):
            clusterData = []
            for feature in cluster: 
                clusterData.append(simData[feature])

    
            #plot cluster
            avgArray=averageArray(clusterData)
            name= 'simData2.2 hCluster '+str(i) + ' ('+str(len(cluster))+')'
            print("Plotting data...",len(cluster))
            genPlot(avgArray,name,0)
            


