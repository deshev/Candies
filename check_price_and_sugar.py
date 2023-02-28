#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 12:53:08 2023
@author: BD

- Check if the sugar content and the price define how often a given candy is
    chosen
- Plot the results

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

def draw_a_candy(x,y,c,s, box=None):
    # This is used to draw a custom symbol
    plt.scatter(x, y, marker='o', \
                color='black', s=s*1.3, cmap='plasma')
    plt.scatter(x+1, y, marker='<', \
                color='black', s=s*1.3, cmap='plasma')
    plt.scatter(x-1, y, marker='>', \
                color='black', s=s*1.3, cmap='plasma')

    plt.scatter(x, y, marker='o', \
                color=c, s=s, cmap='plasma')
    plt.scatter(x+1, y, marker='<', \
                color=c, s=s, cmap='plasma')
    plt.scatter(x-1, y, marker='>', \
                color=c, s=s, cmap='plasma')
    if box:
        plt.plot(x, y, 's', ms=np.sqrt(s*6), mfc="None", mec='black')

def check_price_and_sugar(tbl):
    # Get the correlation between all columns in the table
    corr_coeficients_all = pd.DataFrame.corr(tbl)
    corr_coeficients_single = pd.DataFrame.corr(tbl[tbl['pluribus']==0])
    corr_coeficients_package = pd.DataFrame.corr(tbl[tbl['pluribus']==1])
    
    # Define the colors for individal candies
    colors = np.unique(tbl['main color'])
    color_codes = ['#00FFFF', 'k', 'b', '#8B4513', 'y', 'gray', 'g', '#00FFFF',\
                  '#FFA500', '#FFC0CB', 'purple', 'r', 'w', '#FFD700']
    ccs=dict()
    for i in range(len(colors)):
        ccs[colors[i]] = color_codes[i]

    # Fit a straight line between sugar content and win percent
    fit = np.polyfit(x=tbl['sugarpercent'], y=tbl['winpercent'], deg=1)
    p_line = np.poly1d(fit)

    # Initiate the figure
    plt.figure(figsize=(10,4))
    
    # First deal with sugar content
    ax1 = plt.subplot(1,2,1)
    
    # Plot the correlation line
    sugar_min = tbl['sugarpercent'].min()
    sugar_max = tbl['sugarpercent'].max()
    ax1.plot([sugar_min, sugar_max], p_line([sugar_min, sugar_max]), \
        color='gray', lw=2,\
        label='{:.2f}'.format(corr_coeficients_all['winpercent']['sugarpercent']),\
        zorder=1)
    
    # Plot the data points
    for i in range(len(tbl)):
        draw_a_candy(tbl['sugarpercent'][i], tbl['winpercent'][i],\
                     ccs[tbl['main color'][i]], s=tbl['winpercent'][i])
    
    # Format the plot
    ax1.set_xlabel('sugar content [% of the highest]')
    ax1.set_ylabel('win [%]')
    ax1.legend(loc=2)
    ax1.tick_params(axis='both', direction='in', which='both', right='on', top='on')

### Deal with the price

    # Fit a straight line between price percent and win percent (all points)
    fit = np.polyfit(x=tbl['pricepercent'], y=tbl['winpercent'], deg=1)
    p_line_all = np.poly1d(fit)
    # Repeat the fit only to single candies, not a package
    fit = np.polyfit(x=tbl['pricepercent'][tbl['pluribus']==0], y=tbl['winpercent'][tbl['pluribus']==0], deg=1)
    p_line_single = np.poly1d(fit)
    # Repeat the fit only to candies in packages of many
    fit = np.polyfit(x=tbl['pricepercent'][tbl['pluribus']==1], y=tbl['winpercent'][tbl['pluribus']==1], deg=1)
    p_line_package = np.poly1d(fit)

    ax2 = plt.subplot(1,2,2)
    
    # Plot the correlation line
    sugar_min = tbl['pricepercent'].min()
    sugar_max = tbl['pricepercent'].max()
    ax2.plot([sugar_min, sugar_max], p_line_all([sugar_min, sugar_max]),\
            color='gray', lw=2,\
            label='{:.2f}'.format(corr_coeficients_all['winpercent']['pricepercent']),\
            zorder=1)

    ax2.plot([sugar_min, sugar_max], p_line_single([sugar_min, sugar_max]),\
            color='black', lw=2, ls='--',\
            label='{:.2f}'.format(corr_coeficients_single['winpercent']['pricepercent']),\
            zorder=1)

    ax2.plot([sugar_min, sugar_max], p_line_package([sugar_min, sugar_max]),\
            color='black', lw=2, ls=':',\
            label='{:.2f}'.format(corr_coeficients_package['winpercent']['pricepercent']),\
            zorder=1)

    # Plot the data points
    for i in range(len(tbl)):
        draw_a_candy(tbl['pricepercent'][i], tbl['winpercent'][i],\
                     ccs[tbl['main color'][i]], s=tbl['winpercent'][i],\
                         box=tbl['pluribus'][i])
    
    # Format the plot
    ax2.set_yticklabels([])
    ax2.set_xlabel('price [% of the highest]')
    ax2.set_ylabel("")
    ax2.legend(loc=2)
    ax2.tick_params(axis='both', direction='in', which='both', right='on', top='on')

    # Save it
    plt.tight_layout()
    plt.savefig(path+'check_sugar_price.pdf', dpi=300)


if __name__ == '__main__':
    path = ''
    # Read in the table
    tbl = pd.read_csv(path+'candy_data_extended.csv')
    
    check_price_and_sugar(tbl)