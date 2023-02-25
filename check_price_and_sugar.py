#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 12:53:08 2023
@author: BD

- Check if the sugar content and the price define how often a given candy is
chosen when compared with one other candy from the list (85 in total)
- Plot the results

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

def draw_a_candy(x,y,c,s):
    # This is used to draw a custom symbol
    plt.scatter(x, y, marker='o', \
                c='black', s=s*1.3, cmap='plasma')
    plt.scatter(x+1, y, marker='<', \
                c='black', s=s*1.3, cmap='plasma')
    plt.scatter(x-1, y, marker='>', \
                c='black', s=s*1.3, cmap='plasma')

    plt.scatter(x, y, marker='o', \
                c=c, s=s, cmap='plasma')
    plt.scatter(x+1, y, marker='<', \
                c=c, s=s, cmap='plasma')
    plt.scatter(x-1, y, marker='>', \
                c=c, s=s, cmap='plasma')

def check_price_and_sugar(tbl):
    # Get the correlation between all columns in the table
    corr_coeficients = pd.DataFrame.corr(tbl)

    # Fit a straight line between sugar content and win percent
    fit = np.polyfit(x=tbl['sugarpercent'], y=tbl['winpercent'], deg=1)
    p = np.poly1d(fit)

    # Initiate the figure
    plt.figure(figsize=(10,5))
    ax1 = plt.subplot(1,2,1)
    
    # Plot the correlation line
    sugar_min = tbl['sugarpercent'].min()
    sugar_max = tbl['sugarpercent'].max()
    ax1.plot([sugar_min, sugar_max], p([sugar_min, sugar_max]), \
        color='gray', lw=2, zorder=1)

    # Map the winpercentage to a colormap (needed because of the custom symbols)
    cmap = cm.plasma
    norm = matplotlib.colors.Normalize(vmin=tbl['winpercent'].min(),\
                                       vmax=tbl['winpercent'].max(), clip=True)
    
    # Plot the data points
    for i in range(len(tbl)):
        draw_a_candy(tbl['sugarpercent'][i], tbl['winpercent'][i],\
                     cmap(norm(tbl['winpercent'][i])), s=tbl['winpercent'][i])
    
    # Format the plot
    ax1.set_xlabel('sugar content [% of the highest]')
    ax1.set_ylabel('win [%]')
    # The title shows the correlation coefficient
    ax1.set_title('correlation = {:.2f}'.format(corr_coeficients['winpercent']['sugarpercent']))
    ax1.tick_params(axis='both', direction='in', which='both', right='on', top='on')


###
    # Fit a straight line between price percent and win percent
    fit = np.polyfit(x=tbl['pricepercent'], y=tbl['winpercent'], deg=1)
    p = np.poly1d(fit)

    ax2 = plt.subplot(1,2,2)
    
    # Plot the correlation line
    sugar_min = tbl['pricepercent'].min()
    sugar_max = tbl['pricepercent'].max()
    ax2.plot([sugar_min, sugar_max], p([sugar_min, sugar_max]), \
            color='gray', lw=2, zorder=1)

    # Plot the data points
    for i in range(len(tbl)):
        draw_a_candy(tbl['sugarpercent'][i], tbl['winpercent'][i],\
                     cmap(norm(tbl['winpercent'][i])), s=tbl['winpercent'][i])
    
    # Format the plot
    ax2.set_yticklabels([])
    ax2.set_xlabel('price [% of the highest]')
    ax2.set_ylabel("")
    # The title shows the correlation coefficient
    ax2.set_title('correlation = {:.2f}'.format(corr_coeficients['winpercent']['pricepercent']))
    ax2.tick_params(axis='both', direction='in', which='both', right='on', top='on')

    # Save it
    plt.tight_layout()
    plt.savefig(path+'check_sugar_price.png', dpi=300)


if __name__ == '__main__':
    path = '/home/tazio/works/2023/LDLAssignment/'
    # Read in the table
    tbl = pd.read_csv(path+'candy-data.csv')
    # Turn it into a real percent
    tbl['sugarpercent'] *= 100
    tbl['pricepercent'] *= 100
    
    check_price_and_sugar(tbl)