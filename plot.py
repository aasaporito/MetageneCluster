import matplotlib.pyplot as plt
import numpy as np



##add up/down stream markers and num features label 
def genPlot(result,name,udStream,numFeatures):
    # if udStream == 0: 
    #     markers = [] 
    # else:
    #     start = udStream
    #     end = udStream+ len(result)
    #     markers = [start,end]
    # x = [0] * len(result)
    #y = [0] * len(result)
    
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
    plt.plot(x[udStream-1:(len(x)-udStream-1)],y[udStream-1:(len(x)-udStream-1)])
    plt.plot(x[(len(x)-udStream-1):udStream-1],y[(len(x)-udStream-1):udStream-1],linestyle='-.')
    plt.title(name+' ('+str(numFeatures)+')')
    plt.xlabel('Distance')
    plt.ylabel('Reads')
    plt.locator_params(axis='y', nbins=xyScale)
    plt.locator_params(axis='x',nbins=xyScale)
    plt.savefig(name+".png" , dpi = 75)