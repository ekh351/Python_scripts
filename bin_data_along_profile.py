# -*- coding: utf-8 -*-
"""
Spyder Editor
bin profile data removing trees
Ekbal Hussain @ Uni Leeds
09-05-2017
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

roadID = 6

folder = "/nfs/a1/homes/eeehu/Santiago/satellite_data/SPOT7/POINT_CLOUD/extract_points/"
data = np.genfromtxt(folder+"road"+str(roadID)+".txt", delimiter=" ")

bin_width = 0.00036      # 40 metres in degrees

# determine the number of bins needed
nbins = int(math.ceil((data[:, 0].max() - data[:, 0].min())/bin_width))

# pre-assign a nan output array
output = np.empty([nbins, 6], dtype=float) * np.nan

# bin the data
for i in range(0, nbins):
    xl = i*bin_width + data[:, 0].min()
    xu = (i+1)*bin_width + data[:, 0].min()

    # points inside the bin
    (ix,) = np.where((data[:, 0] > xl) & (data[:, 0] <= xu))
    binnedDat = data[ix, :]

    # remove points outside the 5 and 90 percentile (noise)
    pct = stats.scoreatpercentile(data[ix, 2], (5, 90))
    (ix2,) = np.where((binnedDat[:, 2] > pct[0]) & (binnedDat[:, 2] <= pct[1]))

    if len(binnedDat[ix2, 1]) > 3:
        medH = np.median(binnedDat[ix2, 2])
        std = np.std(binnedDat[ix2, 2])
        medLon = np.median(binnedDat[ix2, 0])
        medLat = np.median(binnedDat[ix2, 1])
        pct2 = stats.scoreatpercentile(binnedDat[ix2, 2], (5, 95))

        # add results to the output array
        output[i, :] = np.array([medLon, medLat, medH, std, pct2[0], pct2[1]])

# remove any rows with nans from the output file
output = output[~np.isnan(output).any(axis=1)]

# plot and check results make sense
plt.figure()
plt.plot(data[:, 0], data[:, 2], 'k.')
plt.plot(output[:, 0], output[:, 2], 'r')
plt.show()

# save output to ascii file
np.savetxt(folder+"bin_profile/binned_profile"+str(roadID)+".txt", output, delimiter="\t", fmt="%0.5f")
