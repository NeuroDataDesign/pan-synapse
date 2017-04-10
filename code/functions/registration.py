import nibabel

import nibabel as nib

import os
import urllib.request
import urllib.error
import urllib.parse
from nipype.interfaces.ants import Registration

import numpy as np
from nibabel.testing import data_path
import pandas as pd
from libtiff import TIFF
from medpy.io import save
from PIL import Image
import nibabel as nb
import operator
import connectLib as cLib
import scipy.sparse as sparse
from cluster import Cluster

def ANTs(fixedImg, movingImg, lowerFence, upperFence):
    img2 = nib.Nifti1Image(fixedImg, np.eye(4))
    nb.save(img2, 'fixed.nii')
    img3 = nib.Nifti1Image(fixedImg, np.eye(4))
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
    real_registered = os.path.join('registered.nii.gz')
    img = nib.load(real_registered)
    real_registered_img = img.get_data()

    registeredClusters = cLib.clusterThresh(real_registered_img, lowerFence, upperFence)
    fixedClusters = cLib.clusterThresh(fixedImg, lowerFence, upperFence)
    movingClusters = cLib.clusterThresh(movingImg, lowerFence, upperFence)

    for i in range(len(fixedClusters)):
        fixedCluster = fixedClusters[i]
        distances = []
        for j in range(len(registeredClusters)):
            registeredCluster = registeredClusters[j]
            distances.append(np.linalg.norm([x1 - x2 for (x1, x2) in zip(registeredCluster.getCentroid(), fixedCluster.getCentroid())]))
        min_index, _ = min(enumerate(distances), key=operator.itemgetter(1))
        centroid = registeredClusters[min_index].getCentroid()
        members = [np.ceil(i) for i in centroid]
        value = np.floor(real_registered_img[members[0], members[1], members[2]])
        i = 0
        while value == 0:
            if i < len(registeredClusters[min_index].members):
                newMembers = registeredClusters[min_index].members[i]
                value = np.floor(real_registered_img[newMembers[0], newMembers[1], newMembers[2]])
                i = i + 1
            if i >= len(registeredClusters[min_index].members):
                value = 2000

        #convert labeled to Sparse
        sparseLabeledMoving = np.empty(len(movingImg), dtype=object)
        for i in range(len(movingImg)):
            sparseLabeledMoving[i] = sparse.csr_matrix(movingImg[i])

        memberList = []
        memberListWithZ = []
        while(len(memberListWithZ) == 0):
            for z in range(len(sparseLabeledMoving)):
                memberListWithoutZ = np.argwhere(sparseLabeledMoving[z] == value)
                memberListWithZ = [[z] + list(tup) for tup in memberListWithoutZ]
                memberList.extend(memberListWithZ)
            value = value - 1

        fixedCluster.timeRegistration = Cluster(memberList)

    return fixedClusters
