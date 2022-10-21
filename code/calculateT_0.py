#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 16:42:01 2021

@author: adam
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u

######################################################################
#################### Initial Conditions  ###########################
######################################################################

Star_known_param = {
    
    'M_star' : 1., # in Solar Masses
    

    }

######################################################################
#################### Functions to be used  ###########################
######################################################################

def Mass_to_Luminosity(star_mass):
    while True:
        if star_mass < 0.2:
            print("The luminosity is wrong, give mass values bigger than 0.2 solar masses")
            constant = 1
            n = 1
            break
        elif star_mass >= 55:
            n = 1
            constant = 3025
            break
        elif star_mass < 0.43:
            n = 2.5
            constant = 0.1849
            break
        elif star_mass < 2:
            n = 4.5
            constant = 1
            break
        else:
            n = 3.0
            constant = 2.8284
            break
    return constant * const.L_sun * (star_mass*const.M_sun/const.M_sun)**n # Luminosity in Watt


def Luminosity_to_T_eff(star_lum):
    return  (star_lum/(4* np.pi * (const.R_sun**2) * const.sigma_sb))**(1/4)

def Temp_at_1AU(star_luminosity):
    r = 149597870700.0 * u.meter
    a = 16* np.pi*np.pi * (r**2)*const.sigma_sb
    return (star_luminosity/a)**(1/4)
    


######################################################################
#################### Main Program  ###########################
######################################################################        

L_star = Mass_to_Luminosity(Star_known_param['M_star']) # Luminosity in Watt
L_star_odot = L_star/const.L_sun


T_AU = Temp_at_1AU(L_star) 

T_eff = Luminosity_to_T_eff(L_star)

