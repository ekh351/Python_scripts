#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Median filter and flatten SRF profiles
@author: Ekbal Hussain
Created: May 16 2017
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

# number of profiles and width in degrees
nprofs = 15
bin_width = 0.00027

folder = "/nfs/a1/homes/eeehu/Santiago/satellite_data/SPOT7/POINT_CLOUD/SRF_profiles/"


def load_data(ID):
    """ load in the data for the profile """
    datafile = folder + "profile"+str(ID)+".txt"
    return np.genfromtxt(datafile, delimiter=" ")


def median_filter(data, ID, bin_width):
    """ Input: Profile ID and bin width in degrees! """

    # determine the number of bins needed
    nbins = int(math.ceil((data[:, 0].max() - data[:, 0].min())/bin_width))

    # pre-assign a nan output array
    output = np.empty([nbins, 6], dtype=float) * np.nan

    # bin elevations
    for i in range(0, nbins):
        xl = i*bin_width + data[:, 0].min()
        xu = (i+1)*bin_width + data[:, 0].min()

        # points inside the bin
        (ix,) = np.where((data[:, 0] > xl) & (data[:, 0] <= xu))
        binnedDat = data[ix, :]

        # remove points outside the 5 and 90 percentile (noise)
        pct = stats.scoreatpercentile(data[ix, 2], (5, 90))
        (ix2,) = np.where(
                (binnedDat[:, 2] > pct[0]) & (binnedDat[:, 2] <= pct[1])
                )

        if len(binnedDat[ix2, 1]) > 3:
            medLon = np.median(binnedDat[ix2, 0])
            medLat = np.median(binnedDat[ix2, 1])
            medLoc = np.median(binnedDat[ix2, 2])
            medH = np.median(binnedDat[ix2, 3])
            pct2 = stats.scoreatpercentile(binnedDat[ix2, 3], (5, 95))

        # add results to the output array
        output[i, :] = np.array(
                [medLon, medLat, medLoc, medH, pct2[0], pct2[1]])

    # remove any rows with nans from the output file
    return output[~np.isnan(output).any(axis=1)]


# run filter for all profiles
for ID in range(1, nprofs+1):
    print "median filter on profile: %d" % (ID)

    data = load_data(ID)
    output = median_filter(data, ID, bin_width)

    # plot and check results make sense
#    plt.figure()
#    plt.plot(data[:, 0], data[:, 3], 'k.')
#    plt.plot(output[:, 0], output[:, 3], 'r')
#    plt.show()

    # save file
    outfile = folder+"binned_prof"+str(ID)+".txt"
    np.savetxt(outfile, output, delimiter="\t", fmt="%0.5f")
