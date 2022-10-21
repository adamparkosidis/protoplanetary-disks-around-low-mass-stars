#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 16:51:52 2021

@author: adam
"""
import plonk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from lmfit.models import PowerLawModel
from matplotlib.offsetbox import AnchoredText
import datetime

begin_time = datetime.datetime.now()

#############################
###### Simulation Info ######
#############################

#list(snap.properties())
#prof.loaded_profiles()
#prof.available_profiles()


##############################
### Surface Density Profile ##
##############################

def Function(Surf_Dens_profile, disc_id):
    model = PowerLawModel()
    params = model.guess(Surf_Dens_profile['surface_density_1D'], x=Surf_Dens_profile['radius_1D'])
    result = model.fit(Surf_Dens_profile['surface_density_1D'], params, x=Surf_Dens_profile['radius_1D'])
    
    #result.plot_fit(xlabel=('Radius [AU]'), ylabel=('Σ(R) g/cm${}^2$'))
    
    star_mass=float(disc_id.split('_')[1][:-1])
    disc_mass=float(disc_id.split('_')[2][:-1])
    symbol_star = '\star'
    symbol_solar_m='\odot'
    string=result.fit_report(result.params)
    string = string.split('+/-')
    amp_uncert = string[1].split()[1]
    exp_uncert = string[2].split()[1]
    equation_str = r'$\Sigma (R)=${:4.0f}$\times(\frac{{R}}{{AU}})$^({:1.3f})$, 20AU<R<50AU$'.format(result.values['amplitude'], result.values['exponent'])
    title = r'$M_{}={} M_{} \; \; M_d= {} M_{}$'.format(symbol_star, star_mass, symbol_solar_m, disc_mass, symbol_solar_m)
    
    
    print(result.fit_report(result.params))
    print(result.ci_report())
    print(result.params.pretty_print())
    return(equation_str,title,amp_uncert,exp_uncert,float(result.values['amplitude']),float(result.values['exponent']),result)

def Plot_Surf_Dens(eq_str,title,fit,Surf_Dens_profile):
    units = {'position': 'au', 'density': 'g/cm^3', 'projection': 'cm', 'temperature' : 'K'}
    #snap.image( quantity='density', extent=(-100, 100, -100, 100), ax_kwargs={'title': title, 'aspect': 'equal'},
    #          units= units, cmap='hot', norm='log10', vmin=Surf_Dens_profile['surface_density_2D'].min(), vmax=Surf_Dens_profile['surface_density_2D'].max())
    #plt.savefig(os.getcwd()+'/../Runs/Graphs_2D/'+disc_id+'_2D.png', kwargs= {'bbox_inches':'tight', 'pad_inches':0})
    # 'xscale':'log'
    
    ax2=prof_1D.plot('radius', 'surface_density', ax_kwargs={'title' : title}, linestyle = 'None')
    fit.plot_fit(ax=ax2,xlabel=('Radius [AU]'), ylabel=('Surface Density  [g/cm^2]'), show_init=True) #comment out if you want only plonks' line
    ax2.set_title(title)
    ax2.legend([eq_str], bbox_to_anchor=(0.5, 0, 0.5, 1.0))
    #box = AnchoredText('Uncertainty in amp, exp : {},{}'.format(amp_uncert,exp_uncert), prop=dict(size=11), frameon=True, loc='upper right')
    #box.patch.set_boxstyle('round, pad=0.,rounding_size=0.2')
    #ax2.add_artist(box)
    ax2.grid()
    plt.tight_layout()   
    #plt.savefig(os.getcwd()+'/../Runs/Graphs_1D/'+disc_id+'_1D.png')
    

####################### 
#### Main Program #####
#######################
#len(os.listdir('../Runs/Runs'))
# Plot surface Density vs Radius in log scale

data = []
for i in range(2): #len(os.listdir('../Runs/Runs'))
    filename = '../Runs/Runs/'+sorted(os.listdir('../Runs/Runs'))[i]+'/disc_00100.h5'
    snap = plonk.load_snap(filename)
    disc_id = filename.split('/')[-2]
    
    snap.add_quantities('disc')
    prof_1D = plonk.load_profile(snap, cmin='20au', cmax='50 au', n_bins=100)
    prof_2D = plonk.load_profile(snap, cmin='2au', cmax='100 au', n_bins=100)
    prof_1D.set_units(position='au', scale_height='au', surface_density='g/cm^2', density='g/cm^3')
    prof_2D.set_units(position='au', scale_height='au', surface_density='g/cm^2', density='g/cm^3')
    #, 'aspect':50, 'yscale': 'log'
    df_input = {
        'radius_1D' : prof_1D['radius'],'surface_density_1D' : prof_1D['surface_density'].to('g/cm^2'),
        'radius_2D' : prof_2D['radius'],'surface_density_2D' : prof_2D['surface_density'].to('g/cm^2')
                   }
    
    Surf_Dens_profile = pd.DataFrame(data=df_input)
    eq_str,title,amp_uncert,exp_uncert,ampl,exp,fit = Function(Surf_Dens_profile, disc_id)
    data.append([disc_id, exp,ampl,exp_uncert,amp_uncert])
    Plot_Surf_Dens(eq_str,title,fit,Surf_Dens_profile)
    

df = pd.DataFrame(data,columns=['disc_id', 'exp', 'ampl [g/cm^2]', 'exp_uncert', 'ampl_uncert'])
print('Script duration {}:'.format(datetime.datetime.now() - begin_time))
'''
###############################
###Check Temperature Profile###
###############################

#len(os.listdir('../Runs/Runs'))

for i in range(len(os.listdir('../Runs/Runs'))):
    filename = '../Runs/Runs/'+sorted(os.listdir('../Runs/Runs'))[i]+'/disc_00100.h5'
    snap = plonk.load_snap(filename)


    snap.add_quantities('disc')
    prof = plonk.load_profile(snap, cmin='1 au', cmax='100 au', n_bins=100) 
    prof.set_units(position='au', scale_height='au', surface_density='g/cm^2', density='g/cm^3')
    ax_kwargs={'xlabel': 'Radius [AU]', 'ylabel': 'T(R) K$', 'title': sorted(os.listdir('../Runs/Runs'))[i]} 
    ax = prof.plot(x='radius', y='temperature', ax_kwargs=ax_kwargs, std='errorbar')
    ax.grid()
    
    df_input = {'radius' : prof['radius'], 'temperature' : prof['temperature']}
    Temperature_profile = pd.DataFrame(data=df_input)

    #model = PowerLawModel()
    #params = model.guess(Temperature_profile['temperature'], x=Temperature_profile['radius'])

    result = model.fit(Temperature_profile['temperature'], params, x=Temperature_profile['radius'])
    result.plot_fit(xlabel=('Radius AU'), ylabel=('T(R) K'))
    plt.title('R_ref=10AU y={:f}x^{:1.4f}'.format(result.values['amplitude'], result.values['exponent']))
    plt.show()

    print(result.fit_report(result.params))
    print(result.ci_report())



###############################
###Check Viscosity###
###############################

#len(os.listdir('../Runs/Runs'))

for i in range(0,19,9):
    filename = '../Runs/Runs/'+sorted(os.listdir('../Runs/Runs'))[i]+'/disc_00100.h5'
    snap = plonk.load_snap(filename)

   
    snap.add_quantities('disc')
    profiles = ['radius','sound_speed','scale_height','disc_viscosity']
    prof = plonk.load_profile(snap, cmin='1 au', cmax='100 au', n_bins=100)
    prof.set_units(position='au', scale_height='au', surface_density='g/cm^2', density='g/cm^3')
    df = prof.to_dataframe(columns=profiles)
    ax_kwargs={'xlabel': 'Radius [AU]', 'ylabel': 'surface_density', 'title': sorted(os.listdir('../Runs/Runs'))[i]} 
    ax = prof.plot(x='radius', y='alpha_shakura_sunyaev', ax_kwargs=ax_kwargs, std='errorbar')
    ax.grid()
    plt.show()
    #df_input = {'radius' : prof['radius'], 'toomre_q' : prof['toomre_q']}
    #Temperature_profile = pd.DataFrame(data=df_input)
 ''' 