import matplotlib.pyplot as plt
import numpy as np



##add up/down stream markers
def genPlot(result,name,udStream):
    if udStream == 0: 
        markers = [] 
    else:
        start = udStream
        end = udStream+ len(result)
        markers = [start,end]
    x = [0] * len(result)
    #y = [0] * len(result)
    
    for i in range(0, len(result)):
        x[i] = i
        #y[i] = result[i]
    y= result

    # ?? 
    np.random.seed(5)

    # plot
    fig, ax = plt.subplots()

    ax.set(xlim=(0, len(result)), xticks=np.arange(0, len(result)),
        ylim=(0, max(result) ), yticks=np.arange(0, max(result)+10))#result[1]

    xyScale= 25

    ax.set_xlabel('Distance')
    ax.set_ylabel('Reads')

    plt.figure(figsize=(15, 10))
    plt.plot(x,y,markevery = markers)
    plt.title(name)
    plt.xlabel('Distance')
    plt.ylabel('Reads')
    plt.locator_params(axis='y', nbins=xyScale)
    plt.locator_params(axis='x',nbins=xyScale)
    plt.savefig(name+".png" , dpi = 75)