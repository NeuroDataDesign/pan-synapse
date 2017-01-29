import math
import pickle

from cluster import Cluster
from munkres import Munkres

import numpy as np

def clusterLoss(cluster1, cluster2):
    c1Centroid = np.array(cluster1.centroid)
    c2Centroid = np.array(cluster2.centroid)
    error = math.sqrt(np.sum((c1Centroid - c2Centroid)**2) + (cluster1.volume-cluster2.volume)**2)
    print error
    return error

#simple em k-means to prototype hungarian
def divide(clusterList, numSubsets, iterations, verbose=False):
    subsets = [[] for i in range(numSubsets)]

    #initialize subsets foldwise
    for i in range(len(clusterList)):
        subsets[i%numSubsets].append(clusterList[i])

    #k means for given iterations
    for iteration in range(iterations):
        if verbose:
            print '\tDivide Progress: ', float(iteration)/iterations
        centroids = [np.average([elem.centroid for elem in subset]) for subset in subsets]
        #TODO deal with empty case
        newSubsets = [[] for i in range(numSubsets)]
        for cluster in clusterList:
            arg = np.argmin([math.sqrt(np.sum((cluster.centroid-centroid)**2)) for centroid in centroids])
            newSubsets[arg].append(cluster)
        subsets = newSubsets
    return subsets

#run hungarian on final subset means, then on the clusters in each subset
def conquer(transSuperClusters, baseSuperClusters, verbose=False):

        if verbose:
            print '\tGenerating Centroid Lists'

        #precompute centroids for speed
        tscCents = [np.average([elem.centroid for elem in subset]) for subset in transSuperClusters]
        bscCents = [np.average([elem.centroid for elem in subset]) for subset in baseSuperClusters]

        if verbose:
            print '\tGenerating Loss Matrix'

        #initialize supercluster loss matrix
        superClusterLoss = np.zeros((len(transSuperClusters), len(baseSuperClusters)))
        for tscIdx in range(len(transSuperClusters)):
            for bscIdx in range(len(baseSuperClusters)):
                superClusterLoss[tscIdx][bscIdx] = math.sqrt(np.sum((tscCents[tscIdx] - bscCents[bscIdx])**2))

        #generate a Munkres object
        m = Munkres()

        if verbose:
            print superClusterLoss.shape
            pickle.dump(superClusterLoss, open('scl.this', 'w'))
            print '\tCalulating Supercluster Pairing'

        #get the supercluster pairing
        superClusterAssignments = zip(*m.compute(superClusterLoss))

        #initialize the assignment list
        assignments = []

        #keep track of iterations for verbose mode
        iterations = 0.
        maxIterations = len(superClusterAssignments)

        #calculate the sub pairings
        for superPairing in superClusterAssignments:
            #print progress if verbose
            if verbose:
                print '\tConquer Progress: ', float(iteration)/maxIterations
                iterations+=1.

            #retrieve paired super clusters
            curTransSubset = transSuperClusters[superPairing[0]]
            curBaseSubset = baseSuperClusters[superPairing[1]]

            #generate sub cost matrix
            subLossMat = np.zeros((len(curTransSubset), len(curBaseSubset)))
            for tsIdx in range(len(curTransSubset)):
                for bsIdx in range(len(curBaseSubset)):
                    subLossMat[tsIdx][bsIdx] = clusterLoss(curTransSubset[tsIdx], curBaseSubset[bsIdx])

            #run sub hungarian on those clusters, get the index pairs
            curPairs = zip(*m.compute(subLossMat))

            #add the cluster pairs at correct indices to the final list
            for pairing in curPairs:
                assignments.append([curTransSubset[pairing[0]], curTransSubset[pairing[1]]])

        return assignments

def register(rawTransList, rawBaseList, supersets, iterations, verbose=False, debug=False):
    if verbose:
        print 'Began Transform Superset Clustering'
    rawTransSuperSet = divide(rawTransList, supersets, iterations, verbose=verbose)
    if verbose:
        print 'Began Base Superset Clustering'
    rawBaseSuperSet = divide(rawBaseList, supersets, iterations, verbose=verbose)

    if debug:
        pickle.dump(rawBaseSuperSet, open('baseSuperSet.this', 'w'))
        pickle.dump(rawTransSuperSet, open('transSuperSet.this', 'w'))

    if verbose:
        print 'Began Conquer Clustering'
    return conquer(rawTransSuperSet, rawBaseSuperSet, verbose=verbose)
