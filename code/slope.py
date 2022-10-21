#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 10:15:47 2021

@author: adam
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import datetime

begin_time = datetime.datetime.now()

#########################################
### Slopes in Surface Density Profiles ##
#########################################

df = pd.read_csv('original_surf_dens_parameters.csv')
#df = df.set_index('Exponent q')
sns.set_style("darkgrid")
plot_1 = sns.lineplot(data=df, x='Exponent q', y= 'Exponent p', style = r'$M_{\star} [M_{\odot}]$')
plt.tight_layout() 
plt.savefig(os.getcwd()+'/../Runs/Figures/figure1.png', dpi =200)
plot_2 = sns.relplot(data=df, x='Exponent q', y= 'Exponent p', col= 'Disc-to-Star Mass Ratio', 
                     style = r'$M_{\star} [M_{\odot}]$', kind='line', legend='full')

leg = plot_2._legend
leg.set_frame_on(True)
leg.set_bbox_to_anchor([0.115, 0.82])
plt.tight_layout() 
plt.savefig(os.getcwd()+'/../Runs/Figures/figure2.png', dpi =200)
print('Script duration {}:'.format(datetime.datetime.now() - begin_time))