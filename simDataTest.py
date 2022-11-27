from hCluster import hCluster
from kMeansClustering import kCluster
from plot import genPlot
from metaGene import averageArray

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

df.close()

# fullData = averageArray(simData)
# genPlot(fullData,'simNoCluster2',0)

# first = averageArray(firstHalf)
# genPlot(first,'firstNoCluster2',0)

# second = averageArray(secondHalf)
# genPlot(second,'secondNoCluster2',0)

# fullData =[first,second]
# full = averageArray(fullData)
# genPlot(full,'simNoCluster2',0)

# nodes = hCluster(2,simData)

# clusters =[]
# for node  in nodes:
#     data = node.getIdxs()
#     clusters.append(data)

clusters,x = kCluster(2,simData)
for i,cluster in enumerate(clusters):
            clusterData = []
            for feature in cluster: 
                clusterData.append(simData[feature])

    
            
            avgArray=averageArray(clusterData)
            name= 'simData2 kCluster '+str(i)
            print("Plotting data...",len(cluster))
            genPlot(avgArray,name,0)
            


