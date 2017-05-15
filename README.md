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
3. Non-Maxima Supression on the clusters in step 2. 
4. Generate annotations of the output from 3. 
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

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/OTSU_Notebook.ipynb
)

Here is an example of an input image into otsuVox, and an output from otsuVox: 
![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/input.png)

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/otsu.png)

Here is an example of an output input image's histogram, and an output image's histogram: 

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/inputHist.png)
![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/images/otsuHist.png)

[Here is a link to our otsuVox notebook](https://github.com/NeuroDataDesign/pan-synapse/blob/master/pipeline_3/background/OTSU_Notebook.ipynb)

**K-nearest Neighbors Filter:**

Function: 

KNN gets rid of the values in the image that have no neighbors that are not identified as synapse

Inputs: 
1. image volume
2. n

Outputs: 
1. The filtered image

Notes:

The KNN filter simply goes through each index, appends its neighbors to a temporary array, and checks how many of those neighbors are nonzero. If there are at least n neighbors that are considered synapse, don't change anything. Otherwise, set the value at that index it to 0 (i.e. say it isn't synapse) 

We use n = 1 for our data modality.

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/figures/exampleKNN.png?raw=true)


**ClusterThresh**

Function: 

ClusterThresh identifies clusters from an image and keeps track of statistics.

Inputs: an input image

Outputs: an array of Class cluster

To do so, we first run [Scipy's ndimage.label function](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html). We then convert this matrix to sparse using [Scipy's sparse function](https://docs.scipy.org/doc/scipy/reference/sparse.html). Then, for each label, we search through this sparse matrix for which indices have value of that label and call these "members." If the number of members (a.k.a. the volume of the cluster) is greater than 10 and less than 100, we then call the construtor for a cluster class with "members" as the input. Doing so keeps track of these indices, the volume (number of indices), and the centroid (average of the indices). We then append this object of type cluster to a variable called clusterList. After we've iterated through each label, we return the clusterList.

For assurance that our volume thresholding is working, here is an example of a distribution of volumes before and after volume thresholding: 

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/figures/BeforeThresholding.png?raw=true)

Note that all of those ticks look small because there is a very high amount of clusters with volume around 1, 2, or 3. We don't want those. 

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/figures/AfterThresholding.png?raw=true)

Note that all of those small ticks are now larger ticks. This means that we got rid of all of the volumes (around 1, 2, or 3) that we didn't want. 

Furthermore, our average volume is 27 voxels. This corroborates the anatomical statistics we were given concerning the average volume of a synapse. Furthermore, our average synapse-to-total volume ratio ranges from 2-4% on average, which is also the biological range we are looking for.
	

### 3. Give each synapse in moving image a unique label 

To do so, we simply use connected components. Specifically, we use [Scipy's ndimage.label function](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html).

Example Connected Components Output: 

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/figures/Connected.png?raw=true)

Note that each cluster has its own label. It appears to be a gradient because there are so many clusters and synapses that are close to each other will have similarly valued labels, and thus appear to be similar colors - the rainbow simply ran out of colors.

### 4. ANTs registration

For ANTs registration, we used Translational, Rigid, and Affine linear registration with MeanSquares as our similarity metric. For more information on ANTs, click [here](http://stnava.github.io/ANTs/_). Specifically, we used the following parameters: 
* transform parameters: 0.1
* number of iterations: [10000, 111110, 11110]
* metric: MeanSquares
* convergence threshold: 1 * 10^(-8)
* convergence window size: 20
* smoothing sigmas: [4, 2, 1]
* shrink factors: [6, 4, 2]

### 5. L2 centroid distance match 

To centroid match, we iterate through the clusters in the fixed image, find its centroid, then iterate through the clusters in the moving image, then find its centroid, as well as the distance between the moving clusters' centroid and the fixed clusters' centroid. We store this distance in an array. We then find which distance was the smallest and say that the cluster in the moving image that corresponds to that distance is the L2 centroid distance match of the fixed cluster.

### 6. For each cluster in (1), note the label of its L2 centroid registered pair, then find which cluster in (3) has that color. Set this cluster to the "timeRegistration" datamember of its corresponding cluster in (1).

For each cluster in the filtered moving image, make note of its L2 centroid distance match's centroid. Then find the value of the registered moving image at that centroid. That is the label of that filtered moving image clusters' L2 centroid distance match. Then search through the connected components + filtered fixed image for which indices have that label. Call the cluster class's constructor on this list of indices, and name this "registered cluster". Say that the moving image clusters's "timeRegistration" data member is this new object of type cluster, "registered cluster." 

To search through the connected components + filtered fixed image, we first convert it to sparse using [Scipy's sparse function](https://docs.scipy.org/doc/scipy/reference/sparse.html), and then search. 

![Cloud Figure](https://github.com/NeuroDataDesign/pan-synapse/blob/master/figures/Screen%20Shot%202017-04-10%20at%205.11.16%20PM.png)
