#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 11:46:50 2023
@author: BD

Evaluate hte effect of package color on the win rate
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def draw_it(i):
    ax.errorbar(x[i], MC_mean[i], yerr=uncertainty[i], fmt='o', elinewidth=2,\
                ms=5, color='black', zorder=0)
    ax.plot(x[i]-0.1, MC_mean[i], marker='>', ms=5, color='black', zorder=0)
    ax.plot(x[i]+0.1, MC_mean[i], marker='<', ms=5, color='black', zorder=0)
    
    ax.errorbar(x[i], MC_mean[i], yerr=uncertainty[i]*0.99, fmt='o', elinewidth=1.5,\
                ms=1, color=color_codes[i], zorder=1)
    ax.plot(x[i], MC_mean[i], marker='o', ms=5, color='black', zorder=2)
    ax.plot(x[i], MC_mean[i], marker='o', ms=4, color=color_codes[i], zorder=3)
    ax.plot(x[i]-0.1, MC_mean[i], marker='>', ms=4, color=color_codes[i], zorder=2)
    ax.plot(x[i]+0.1, MC_mean[i], marker='<', ms=4, color=color_codes[i], zorder=2)



if __name__ == '__main__':
    path = '/home/tazio/works/2023/LDLAssignment/'
    # Read in the table
    tbl = pd.read_csv(path+'candy_data_extended.csv')
    
    colors = np.unique(tbl['main color'])
    
    color_codes = ['#00FFFF', 'k', 'b', '#8B4513', 'y', 'gray', 'g', '#00FFFF',\
                  '#FFA500', '#FFC0CB', 'purple', 'r', 'w', '#FFD700']
    
    MC_mean = []
    MC_std = []
    N = []
    
    for color in colors:
        MC_mean.append(np.mean(tbl['winpercent'][tbl['main color']==color]))
        MC_std.append(np.std(tbl['winpercent'][tbl['main color']==color]))
        N.append(len(tbl[tbl['main color']==color]))
    
    uncertainty = MC_std/np.sqrt(N)
    x = range(len(colors))
    
    plt.figure()
    ax = plt.subplot(111)
    for i in range(len(N)):
        draw_it(i)
        ax.text(x[i]-0.1, 32, N[i])
    
    ax.text(-0.75, 32, 'N=')
    ax.set_xticks(range(len(colors)), colors, rotation=90)
    ax.set_ylabel('win [%]')
    
    plt.tight_layout()
    plt.savefig(path+'package_colors.pdf')