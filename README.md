# Synapsys Documentation

### Function:
Synapsys detects synapses from two-fluorescent microscope images.

### Inputs:
1. A PSD95_448 image.

### Output:
1. An annotation image.

_____________________________________________________________________________
### Overall Steps

1. Otsu's Binarization on the input image to binarize the image.
2. Cluster the image from Step 1 into Objects of type Cluster. 
3. Noise Supression of clusters from Step 2. 
4. Generate annotations of the output from Step 3. 
_____________________________________________________________________________

### 1. Otsu's Binarization:

To binarize the input image, we run a custom algorithm called otsuVox. 

**otsuVox:**

Function: 

otsuVox maximizes inter-class variance and minimizes intra-class variance. In other words, if we have two normal curves, otsuVox will find the cutoff point between the two and grab everything in the rightmost normal curve.

Inputs: 
1. image volume

Outputs: 
1. binarized volume.

Here is an example of an input image into otsuVox, and an output from otsuVox: 

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/input.png)
![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/otsu.png)

Here is an example of an output input image's histogram, and an output image's histogram: 

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/inputHist.png)
![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/otsuHist.png)

[Here is a link to our otsuVox notebook](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/OTSU_Notebook.ipynb)
	

### 2. Clustering

For Clustering, we use a custom algorithm called ClusterThresh. 

**ClusterThresh**

Function: 

ClusterThresh identifies clusters from an image and keeps track of statistics (centroids, member indices, volume).

Inputs: an input image, a lower bound, an upper bound

Outputs: an array of Class cluster

To do so, we first run [Scipy's ndimage.label function](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html). We then convert this matrix to sparse using [Scipy's sparse function](https://docs.scipy.org/doc/scipy/reference/sparse.html). Then, for each label, we search through this sparse matrix for which indices have value of that label and call these "members." If the number of members (a.k.a. the volume of the cluster) is greater than the lower bound and less than the upper bound, we then call the construtor for a cluster class with "members" as the input. Doing so keeps track of these indices, the volume (number of indices), and the centroid (average of the indices). We then append this object of type cluster to a variable called clusterList. After we've iterated through each label, we return the clusterList.

[Here is a link to our clusterThresh notebook](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/Cluster_Thresh_Algorithms.md.ipynb)

### 3. Noise Supression

For Noise Supression, we use a custom algorithm called nonMaximaSupression

**nonMaximaSupression** 

Function: 

nonMaximaSupression simply takes the brightest clusters using z-score. 

Inputs: a clusterList, a raw image, and a z-score

Outputs: a supressed list of clusters

To supress the non-bright clusters, we graph the distribution of the raw image, keeping track of the mean and the standard deviation. For each of the cluster in clusterList, we find the average brightness of that cluster in the raw image, and if that average brightness is at least the input z-score standard deviation from the mean of the raw image, we keep it. Otherwise, we say it is not synapse. 

[Here is a link to our nonMaximaSupression notebook](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/non_maxima_supression.ipynb)

### 4. Generate Annotations 

To generate annotations, we return an image where the indices of the remaining synapses from Step 3 are 1, and everything else is 0. We also return a list of centroids, by simply taking the average of the indices of each synapse individually and adding that centroid to the list. 


