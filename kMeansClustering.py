"""Summary
    File with functions to create and process clustering using the kMeans algorithm.

"""
import random


def calcMax(data):
    """Summary
        Calculates the maximum from a collection of features
    Args:
        data (list): 2d data list

    Returns:
        list: List of maximums
    """
    mxs = []
    for i in range(len(data[0])):
        max = 0
        for feature in data:
            if feature[i] > max:
                max = feature[i]
        mxs.append(max)
    return mxs


def calcNearestCluster(feature, clusterCenters):
    """Summary
        Calculate the distance of the current feature to each cluster

    Args:
        feature (list): Feature list
        clusterCenters (list): List of cluster centers

    Returns:
        int: Index of the cluster the feature is closest to
    """
    distances = []
    for cluster in clusterCenters:
        distance = 0
        for i, center in enumerate(cluster):
            distance += abs(center - feature[i])
        distances.append(distance)

    # find min
    min = distances[0]
    nearest = 0
    for i, distance in enumerate(distances):
        if distance <= min:
            min = distance
            nearest = i
    return nearest  


def normalizeShape(feature): 
    """Summary
        Normalize a feature by shape

    Args:
        feature (list): Feature list

    Returns:
        list: Normalized feature list
    """
    # find average height
    avg = 0
    for val in feature:
        avg += val
    avg = avg / len(feature)
    # divide each position by average
    normalFeature = []
    for val in feature:
        normalFeature.append(val / avg)
    return normalFeature


def calcNCShape(feature, clusterCenters):
    """Summary
        Calculates the nearest cluster based on shape

    Args:
        feature (list): Feature list
        clusterCenters (list): List of cluster centers

    Returns:
        int: Index of the nearest cluster
    """
    normalFeature = normalizeShape(feature)
    normalCenters = []
    for center in clusterCenters:
        normalCenters.append(normalizeShape(center))

    return calcNearestCluster(normalFeature, normalCenters)


def calcCenters(cluster, data): 
    """Summary
        Calulates the centers for a cluster

    Args:
        cluster (list): Cluster to find the center of
        data (list): 2D Data list

    Returns:
        list: List of centers for each feature in a cluster
    """
    centers = []
    for i in range(len(data[0])):
        center = 0
        numFeatures = 0
        for feature in cluster:
            center += data[feature][i]
            numFeatures += 1

        avgCenter = center / numFeatures
        centers.append(avgCenter)
    return centers


def isStable(memory):  # return bool
    """Summary
        Internal function to test stability of memory

    Args:
        memory (list): 

    Returns:
        bool: Returns true if the memory is stable
    """
    # look at general number of movers --> identify convergence of num movers
    numMovers = memory[-1]
    print('movers:', numMovers)

    if numMovers == 0 or (len(memory) > 2 and (abs(memory[-2] - memory[-1]) <= .1 * memory[-2])
                          and memory[-1] < .25 * max(memory) and memory[-1] <= memory[-2]
                          and memory[-1] == min(memory)):
        return True

    return False


def init(numClusters, data):
    """Summary
        Initializer 

    Args:
        numClusters (int): Number of clusters
        data (list): 2d list storing data

    Returns:
        (list, list, list): Tuple storing: List of clusters, list of cluster centers, list of previous feature locatoins
    """
    clusters = []  # an array of feature indexes belong to each cluster
    clusterCenters = []  # a center for each position of each cluster
    prev = []  # tracks the previous location of each feature
    for i in range(len(data)):
        prev.append([])

    mxs = calcMax(data)

    # initialize clusters with random centers
    while len(clusterCenters) < (numClusters):
        clusters.append([])
        centers = []
        for i in range(len(data[0])):
            # pick random value in the range of the data at that index
            center = random.randint(0, int(mxs[i]))
            centers.append(center)
        clusterCenters.append(centers)
    return clusters, clusterCenters, prev


# calculate final distances from each feature to their current cluster to assess the accuracy of the clustering
def finalDistance(clusters, clusterCenters, data):
    """Summary
        Calculates final distances between features and their current clusters

    Args:
        clusters (list): List of clusters
        clusterCenters (list): List of cluster centers
        data (list): 2D data list

    Returns:
        int: Total distance between clusters and cluster centers
    """
    totDist = 0
    for i, cluster in enumerate(clusters):
        clusterDist = 0
        for feature in cluster:
            featureDist = 0
            for j, val in enumerate(data[feature]):
                featureDist += abs(clusterCenters[i][j] - val)
            clusterDist += featureDist
        totDist += clusterDist

    return totDist

# add return cluster centers and /0 error


def kCluster(numClusters, data, distCalc):
    """Summary
        Generates kClusters
    Args:
        numClusters (int): Number of clusters
        data (list): 2D data list
        distCalc (int): Distance calculated using calculation methods

    Returns:
        (list, int): Returns The list of clusters and total distance between 
                    features and their clusters
    """
    if distCalc > 1:
        print('Undefined distance measure. Use 0 for height or 1 for shape.')
        return
    clusters = []  # an array of feature indexes belonging to each cluster
    clusterCenters = []  # a center for each position of each cluster
    prev = []  # tracks the previous location of each feature

    for i in range(len(data)):
        prev.append(0)

    mxs = calcMax(data)

    # #initialize clusters with random centers
    while len(clusterCenters) < (numClusters):
        clusters.append([])
        centers = []
        for i in range(len(data[0])):
            center = random.randint(0, int(mxs[i]))
            centers.append(center)
        clusterCenters.append(centers)
    centers = []
    # for i in range(len(data[0])):
    #     center=data[0][i]
    #     centers.append(center)
    # clusterCenters.append(centers)
    # clusters.append([])

    # check prev
    #prev = clusters
    # clusters, clusterCenters,prev =init(numClusters,data)
    #print('numcluster ',len(clusters) , len(clusterCenters))
    stop = False
    memory = []
    First = True
    # memory.append(len(data))
    while stop == False:
        movers = 0
        # reset clusters
        for i in range(numClusters):  # [[],[],[],...]
            clusters[i] = []

        # assign new cluster for each feature
        for i, feature in enumerate(data):
            if distCalc == 0:
                cluster = calcNearestCluster(
                    feature, clusterCenters)  # cluster index
            elif distCalc == 1:
                cluster = calcNCShape(feature, clusterCenters)

            clusters[cluster].append(i)  # populate clusters
            if First == True:
                prev[i] = cluster
                First = False
            else:
                if prev[i] != cluster:
                    movers += 1
                    prev[i] = cluster

        # calc new centers for each cluster
        for i, cluster in enumerate(clusters):
            clusterCenters[i] = calcCenters(cluster, data)

        memory.append(movers)  # track how many features changed cluster
        stop = isStable(memory)  # stop condition

        # calc final distance
        totDistance = finalDistance(clusters, clusterCenters, data)
    return clusters, totDistance

def oneCluster(graphArrays):
    """Summary
        Finds a baseline to be used when the clustering type is set to auto.

    Args:
        graphArrays (list): 2D Input data list

    Returns:
        (list, int): Returns a list of averages and totalDistance between features
    """
    avgArray = []
    for i in range(len(graphArrays[0])):
        avgArray.append(0)
    numArray = len(graphArrays)
    for array in graphArrays:
        for i in range(len(array)):
            avgArray[i] += array[i]
    for j in range(len(avgArray)):
        avgArray[j] = avgArray[j] / numArray
    totDistance = 0
    for i in range(len(graphArrays)):
        for j in range(len(avgArray)):
            dist = abs(graphArrays[i][j] - avgArray[j])
            totDistance += dist
    return avgArray, totDistance


def autoKCluster(data, distCalc):
    """Summary
        Generates clusters using autoK algorithm.
    Args:
        data (list): 2D list storing data
        distCalc (int): Distance calculated using calculation methods

    Returns:
        list: Returns a list of clusters
    """
    # get total distance from each cluster, stop when change in total distance from last cluser < 25%
    totDistancePerIteration = []
    x, totDistance1 = oneCluster(data)  # baseline
    totDistancePerIteration.append(totDistance1)
    diff = totDistance1
    numClusters = 2
    while diff > (.2 * (totDistancePerIteration[numClusters - 2])):
        clusters, totDistance = kCluster(numClusters, data, distCalc)
        totDistancePerIteration.append(totDistance)
        diff = abs(
            totDistancePerIteration[numClusters - 1] - totDistancePerIteration[numClusters - 2])
        print(diff)
        numClusters += 1

    diff = abs(totDistancePerIteration[1] - totDistancePerIteration[0])
    if diff > (.2 * (totDistancePerIteration[0])):
        numClusters = 1
        clusters, totDistance = kCluster(numClusters, data, distCalc)
        numClusters = 2
    print('Best clusters:', numClusters - 1)
    return clusters
