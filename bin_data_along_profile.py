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


# data = np.genfromtxt("tree_height.txt", delimiter=" ")
data = np.genfromtxt("/nfs/a1/homes/eeehu/Santiago/satellite_data/SPOT7/POINT_CLOUD/extract_points/road3.txt", delimiter=" ")

bin_width = 0.00036      # 40 metres in degrees

# determine the number of bins needed
nbins = int(math.ceil((data[:, 0].max() - data[:, 0].min())/bin_width))

# pre-assign output array
output = np.empty([nbins, 6], dtype=float)

# bin the data
for i in range(0, nbins):
    xl = i*bin_width + data[:, 0].min()
    xu = (i+1)*bin_width + data[:, 0].min()

    # points inside the bin
    (ix,) = np.where((data[:, 0] > xl) & (data[:, 0] <= xu))
    binnedDat = data[ix, :]

    # remove points outside the 5 and 90 percentile
    pct = stats.scoreatpercentile(data[ix, 2], (5, 90))
    (ix2,) = np.where((binnedDat[:, 2] > pct[0]) & (binnedDat[:, 2] <= pct[1]))

    # remove points outside +/- 5m of mean in each bin
    medianH = np.median(binnedDat[:, 2])
    meanH = binnedDat[ix2, 2].mean()
    (ix3,) = np.where((binnedDat[:, 2] >= (meanH - 2)) &
             (binnedDat[:, 2] < (meanH + 4)))

    avgLon = binnedDat[ix3, 0].mean()
    avgLat = binnedDat[ix3, 1].mean()
    avgH = binnedDat[ix3, 2].mean()
    pct2 = stats.scoreatpercentile(binnedDat[ix3, 2], (5, 95))

    output[i, 0] = avgLon
    output[i, 1] = avgLat
    output[i, 2] = avgH
    output[i, 3] = pct2[0]
    output[i, 4] = pct2[1]
    output[i, 5] = medianH    

# remove any rows with nans from the output file
output = output[~np.isnan(output).any(axis=1)]

plt.figure()
plt.plot(data[:, 0], data[:, 2], 'k.')
plt.plot(output[:, 0], output[:, 2], 'r')
plt.plot(output[:, 0], output[:, 5], 'g')
# plt.plot(output[:, 0], output[:, 3], 'b')
# plt.plot(output[:, 0], output[:, 4], 'g')
plt.show()

# save output to ascii file
# np.savetxt("binned_profile3.txt", output, delimiter="\t", fmt="%0.5f")
