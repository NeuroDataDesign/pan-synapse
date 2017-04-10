# Synapsys Documentation

### Function:
Synapsys detects synapses from two-fluorescent microscope images and tracks their volumes and centroids over time.

### Inputs:
1. A tiff image at first timepoint
2. A tiff image at second timepoint

### Output:
1. A csv file annotating volume changes and centroids changes over time in the form of a table. Example: 

					Volume Change		Centroid Change
		Synapse 1	v1 --> v1`			(c1_x, c1_y) --> (c1`_x, c1`_y)
        Synapse 2	v2 --> v2`			(c2_x, c2_y) --> (c2`_x, c2`_y)

### Notes:
* For the purpose of this documentation, we will call the first image the "fixed image" and the second image the "moving image." This terminology comes directly from the ANTs registration documentation that we used to deteremine which synapses correspond to which across timepoints.
* We use ANTs heavily in our pipeline. If you would like more information concerning exactly what ANTs does, click [here](http://stnava.github.io/ANTs/_)
_____________________________________________________________________________
### Overall Steps

1. Identify clusters in fixed image (i.e. Volume Threshold + Adaptive Threshold + knn filter)
2. Identify clusters in moving image - (i.e. Volume threshold + Adaptive threshold + knn filter)
3. Give each synapse in moving image a unique label - (i.e. Connected Components)
3. ANTs registration on (3) with (1) as the fixed image.
4. L2 centroid distance match of clusters in (3) w/ those in (1) 
5. For each cluster in (1), note the label of its L2 centroid registered pair, then find which cluster in (3) has that color. Set this cluster to the "timeRegistration" datamember of its corresponding cluster in (1).
_____________________________________________________________________________

### 1/2. Identifying Clusters:

To identify clusters in the fixed image, we run adaptive thresholding, a k nearest neighbors filter, and volume thresholding. We then run a custom algorithm called clusterThresh.

**Adaptive Thresholding:**

Function: 

Adaptive Thresholding segments an image by identifying the pixels of highest intensity in neighborhoods. 

Inputs: 
1. image volume
2. sx
3. sy

Outputs: 
1. The segmented image

Notes:

Our adaptive thresholding method is unique. We split the image into a certain amount of neighbors (the number will be explained), and then run a binary threshold within that neighborhood on each slice. The cutoff value for that binary threshold is defined as the 90th percentile in the distribution of intensities within that slice. The number of neighbors is deteremined by sx and sy. This is how many times we to "split" the x and y axis, respectively, into neighborhoods for binary thresholding. For example, saw you have sX = 2, sY = 1. Then you will have 2 neighbors. One consists of every value in the image containing x values less than half x-axis length. The other consists of every value in the image containing x values larger than half the x-axis length. If sX were 3, this would occur from x = 0 to x_ax_len/3, x_ax_len/3 to 2 * x_ax_len/3, and 2 * x_ax_len/3 to 1. The same applies for sY, but with the Y axis. 

We use sX =64 and sY = 64 for our data modality.

![](https://github.com/NeuroDataDesign/pan-synapse/blob/master/exampleImg.png?raw=true)

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

**Volume Thresholding** 

For volume thresholding, we used [Scipy's ndimage.label function](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html) (which runs connected components). Then, for each unique label in the image, we find how many indices in the connected components image contain that value. If the number of indices is fewer than 10 or greater than 100, we set the values at those indices of the original image equal to 0 (i.e. say it isn't synapse).

**ClusterThresh**

Function: 

ClusterThresh identifies clusters from an image and keeps track of statistics.

Inputs: an input image

Outputs: an array of Class cluster

To do so, we first run [Scipy's ndimage.label function](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html). We then convert this matrix to sparse using [Scipy's sparse function](https://docs.scipy.org/doc/scipy/reference/sparse.html). Then, for each label, we search through this sparse matrix for which indices have value of that label and call these "members." We then call the construtor for a cluster class with "members" as the input. Doing so keeps track of these indices, the volume (number of indices), and the centroid (average of the indices). We then append this object of type cluster to a variable called clusterList. After we've iterated through each label, we return the clusterList.
	

### 3. Give each synapse in moving image a unique label 

To do so, we simply use connected components. Specifically, we use [Scipy's ndimage.label function](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html).

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
