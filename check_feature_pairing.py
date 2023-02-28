#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:32:51 2023
@author: BD

Check and plot the correlation between all separate features
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = '/home/tazio/works/2023/LDLAssignment/'
# Read in the table
tbl = pd.read_csv(path+'candy_data_extended.csv')
# We check those separately so they are not needed here
tbl.drop(['Unnamed: 0', 'winpercent'], axis=1, inplace=True)

# Get the correlation between all columns in the table
corr_coeficients_all = pd.DataFrame.corr(tbl)

size = corr_coeficients_all.shape[0]

# The result is symmetric around the main diagonal.
# Zero the unnecessary part to avoid cluttering the plot
for i in range(size):
    corr_coeficients_all.iloc[i][i:] = 0

# Get the highest coeficient (Needed to make the plot symmetric around 0)
vlim = np.max(abs(corr_coeficients_all.values))

# Plot it
plt.figure(figsize=(5,5))
ax = plt.subplot(111)

# Use diverging color map that works even for colorblind people
plt.imshow(corr_coeficients_all.values[1:,:-1], cmap='PRGn', vmin=-vlim, vmax=vlim)
plt.colorbar(label='correlation coefficient', aspect=50)

# Remove the frame
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Set the tick labels
ax.set_xticks(range(size-1), corr_coeficients_all.columns[:-1], rotation=90)
ax.set_yticks(range(size-1), corr_coeficients_all.columns[1:])

plt.tight_layout()
plt.savefig(path+'feature_pairing2.pdf')