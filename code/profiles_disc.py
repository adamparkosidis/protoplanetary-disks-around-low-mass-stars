#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 20:11:51 2021

@author: adam
"""
import plonk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
#from lmfit.models import PowerLawModel
from plonk.analysis.filters import annulus


##############################
### Disc Profiles ##
##############################

# Plot surface Density vs Radius in log scale

filename = '../Runs/Runs/r_1s_0.01d_0.3q/disc_00100.h5'
snap = plonk.load_snap(filename)
snap.add_quantities('disc')
prof = plonk.load_profile(snap, cmin='1 au', cmax='100 au', n_bins=100)
prof.set_units(position='au', scale_height='au', surface_density='g/cm^2', density='kg/m^3')

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(14, 8), dpi = 200)
ax0_0_kwargs={'xlabel': 'Radius [AU]', 'ylabel': 'Σ(R) g/cm^2', 'yscale': 'log'} 
ax0_1_kwargs={'xlabel': 'Radius [AU]', 'ylabel': 'T(R) K'} 
ax1_0_kwargs={'xlabel': 'Radius [AU]', 'ylabel': 'H [AU]'}
ax1_1_kwargs={'xlabel': 'Radius [AU]', 'ylabel': 'density [kg/m^3]'}

prof.plot('radius', 'surface_density', ax=axs[0,0], ax_kwargs=ax0_0_kwargs)
axs[0,0].grid()
prof.plot('radius', 'temperature', ax=axs[0,1], ax_kwargs=ax0_1_kwargs)
axs[0,1].grid()
prof.plot('radius', 'scale_height', ax=axs[1,0], ax_kwargs=ax1_0_kwargs)
axs[1,0].grid()
prof.plot('radius', 'density', ax=axs[1,1], ax_kwargs=ax1_1_kwargs)
axs[1,1].grid()


##############################
### Z Coordinate Profile ##
##############################

au = plonk.units('au')
subsnap = annulus(snap=snap, radius_min=47.5*au, radius_max=52.5*au, height=100*au)
prof = plonk.load_profile(subsnap,ndim=1,coordinate='z',cmin='-15 au', cmax='15 au')
prof.set_units(position='au', density='g/cm^3')
ax = prof.plot('z', 'density')
ax.grid()



#############################
###### Whole Simulation ######
#############################

#prefix = '../Runs/Runs/r_1s_0.01d_0.3q'
#sim = plonk.load_simulation(prefix=prefix)

filename = '../Runs/Runs/r_1s_0.01d_0.3q/disc_00100.h5'
snap = plonk.load_snap(filename)

subsnaps = snap.subsnaps_as_dict(squeeze=True)

profs = {family: plonk.load_profile(subsnap) for family, subsnap in subsnaps.items()}

fig, ax = plt.subplots()

for label, prof in profs.items():
    prof.set_units(position='au', scale_height='au')
    prof.plot('radius', 'scale_height', label=label, ax=ax)

ax.set_ylabel('Scale height [au]')

