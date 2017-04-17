import nibabel

import nibabel as nib

import os
from nipype.interfaces.ants import Registration

import numpy as np
from scipy.spatial import KDTree
from nibabel.testing import data_path
import pandas as pd
from medpy.io import save
from PIL import Image
import nibabel as nb
import operator
import connectLib as cLib
import scipy.sparse as sparse
from cluster import Cluster

def ANTs(fixedImg, movingImg, fixedImgLandmarks, movingImgLandmarks, lowerFence, upperFence, r = 5000):
    img2 = nib.Nifti1Image(fixedImgLandmarks, np.eye(4))
    nb.save(img2, 'fixed.nii')
    img3 = nib.Nifti1Image(movingImgLandmarks, np.eye(4))
    nb.save(img3, 'moving.nii')
    reg = Registration()
    reg.inputs.fixed_image = 'fixed.nii'
    reg.inputs.moving_image = 'moving.nii'
    reg.inputs.output_transform_prefix = 'thisTransform'
    reg.inputs.output_warped_image = 'registered.nii.gz'
    reg.inputs.output_transform_prefix = "output_"
    reg.inputs.transforms = ['Translation', 'Rigid', 'Affine']
    reg.inputs.transform_parameters = [(0.1,), (0.1,), (0.1,)]
    reg.inputs.number_of_iterations = ([[10000, 111110, 11110]] * 3)
    reg.inputs.dimension = 3
    reg.inputs.write_composite_transform = True
    reg.inputs.collapse_output_transforms = False
    reg.inputs.metric = ['MeanSquares'] * 3
    reg.inputs.metric_weight = [1] * 3
    reg.inputs.radius_or_number_of_bins = [32] * 3
    reg.inputs.sampling_strategy = ['Regular'] * 3
    reg.inputs.sampling_percentage = [0.3] * 3
    reg.inputs.convergence_threshold = [1.e-8] * 3
    reg.inputs.convergence_window_size = [20] * 3
    reg.inputs.smoothing_sigmas = [[4, 2, 1]] * 3
    reg.inputs.sigma_units = ['vox'] * 3
    reg.inputs.shrink_factors = [[6, 4, 2]] + [[3, 2, 1]] * 2
    reg.inputs.use_estimate_learning_rate_once = [True] * 3
    reg.inputs.use_histogram_matching = [False] * 3
    reg.inputs.initial_moving_transform_com = True
    reg.run()

    img2 = nib.Nifti1Image(fixedImg, np.eye(4))
    nb.save(img2, 'fixed.nii')
    img3 = nib.Nifti1Image(movingImg, np.eye(4))
    nb.save(img3, 'moving.nii')
    reg.inputs.fixed_image = 'fixed.nii'
    reg.inputs.moving_image = 'moving.nii'
    reg.initial_moving_transform = 'transform0DerivedInitialMovingTranslation.mat'
    reg.run()

    real_registered = os.path.join('registered.nii.gz')
    img = nib.load(real_registered)
    real_registered_img = img.get_data()

    registeredClusters = cLib.clusterThresh(real_registered_img, lowerFence, upperFence)
    fixedClusters = cLib.clusterThresh(fixedImg, lowerFence, upperFence)
    movingClusters = cLib.clusterThresh(movingImg, lowerFence, upperFence)

    print 'registering clusters'
    #l2 centroid match, capped at r
    A = [elem.getCentroid() for elem in fixedClusters]
    B = [elem.getCentroid() for elem in movingClusters]

    tree = KDTree(B)
    for baseIdx, a in enumerate(A):
        dist, idx = tree.query(a, k=1, distance_upper_bound = r)
        if dist == float('Inf'):
            fixedClusters[baseIdx].timeRegistration=Cluster([[-1, -1, -1]])
        else:
            fixedClusters[baseIdx].timeRegistration=movingClusters[idx]

    return fixedClusters
