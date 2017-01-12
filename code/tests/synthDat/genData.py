import numpy as np
import matplotlib.pyplot as plt
import pickle

array = np.zeros((100, 100))
for i in range(20):
    for j in range(20):
        array[5*(2*j): 5*(2*j + 1), 5*(2*i): 5*(2*i + 1)] = 100
pickle.dump(array, open( "clusterGrid.synth", "w" ) )
