import matplotlib.pyplot as plt
import numpy as np
import os 


##add up/down stream markers and num features label 
def genPlot(result,fname,dirName,udStream,numFeatures):    
    # for i in range(0, len(result)):
    #     x[i] = i
    #     #y[i] = result[i]
    # y= result
    y=np.array(result)
    x=np.arange(len(y))


    # plot
    fig, ax = plt.subplots()

    ax.set(xlim=(0, len(result)), xticks=np.arange(0, len(result)),
        ylim=(0, max(result) ), yticks=np.arange(0, max(result)+10))#result[1]

    xyScale= 25

    ax.set_xlabel('Distance')
    ax.set_ylabel('Reads')

    plt.figure(figsize=(15, 10))
    plt.plot(x[(len(x)-udStream-1):len(x)-1],y[(len(x)-udStream-1):len(x)-1],linestyle='-.',color='red')
    plt.plot(x[0:udStream-1],y[0:udStream-1],linestyle='-.',color='red')
    plt.plot(x[udStream-1:(len(x)-udStream-1)],y[udStream-1:(len(x)-udStream-1)],color ='black')
    plt.title(fname+' ('+str(numFeatures)+')')
    plt.xlabel('Distance')
    plt.ylabel('Reads')
    # plt.locator_params(axis='y', nbins=xyScale)
    # plt.locator_params(axis='x',nbins=xyScale) 
    
    path=fname+".png" #in case of single plot
    if dirName != None:
        path = 'Outputs/'+dirName+'/'+path

    plt.savefig(path , dpi = 75)