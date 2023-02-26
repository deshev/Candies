#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 20:15:27 2023
@author: tazio

Add the columns with the color to the main table
Those columns were created manually
"""

import pandas as pd

path = '/home/tazio/works/2023/LDLAssignment/'

# Open the main data table 
tbl = pd.read_csv(path+'candy-data.csv')

# Some columns are meant to represent percentage but are actually fractions
tbl['sugarpercent'] *= 100
tbl['pricepercent'] *= 100

# Open the table with the tabulated packaging color information
cols = pd.read_csv(path+'colors.csv')

# Remove the artefacts from the manual work (some white spaces)                
cols['main color'] = cols['main color'].str.replace(" ", "")

# Add columns to the main table to contain the color info
tbl['main color'] = cols['main color'].values
tbl['has blue'] = cols['has blue'].values
tbl['has red'] = cols['has red'].values

# Make sure the color values go to the right place
for i in range(len(tbl)):
    tbl['main color'][i] = cols['main color'][cols['competitorname']==tbl['competitorname'][i]].values[0]
    tbl['has blue'][i] = cols['has blue'][cols['competitorname']==tbl['competitorname'][i]].values
    tbl['has red'][i] = cols['has red'][cols['competitorname']==tbl['competitorname'][i]].values

# Save the extended table
tbl.to_csv(path+'candy_data_extended.csv')
