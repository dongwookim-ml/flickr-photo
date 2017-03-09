import os, sys
import numpy as np
import pandas as pd
import pickle as pkl

if __name__ == '__main__':

    fmodel = 'model-Melb.pkl'  # path of the trained model file
    model = pkl.load(open(fmodel, 'rb'))['MODEL']  # trained model
    
    startPOI = 9  # the start POI-ID for the desired trajectory, can be any POI-ID in poi-Melb-all.csv
    length = 8    # the length of desired trajectory: the number of POIs in trajectory (including start POI)
                  # if length > 8, the inference could be slow

    recommendations = model.predict(startPOI, length) # recommendations is list of 10 trajectories

    for i in range(len(recommendations)):
        print('Top %d recommendation: %s' % (i+1, str(list(recommendations[i]))))
