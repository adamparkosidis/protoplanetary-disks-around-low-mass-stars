# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy as np
import phantomsetup
import os
import datetime

begin_time = datetime.datetime.now()

cwd = os.getcwd()

System_constants={

    'utime' : 5.022E6, # PHANTOM code unit for time in seconds
    'yr' : 3.15E7, # Seconds in year
    'msun' : 1.989E33,
    'AU' : 1.496E13,

    }

##############
# Disc setup #
##############

Disc_setup = {

    'number_of_particles' : 200_000, # will be ~200.000
    'norbits' : 5,
    'radius_min' : 1.0,
    'radius_max' : 100.0,
    'disc_mass' : 0.01,
    'alpha_art' : 0.01, # Artifical viscosity alpha
    'beta_art' : 2.0,  # Artifical viscosity beta (keep this as 2 to prevent interparticle penetration)
    'p_index' : 2.05, # Doesn't realy matter now, cause this will be the output of the simulation. This specific (large) value let the disc relax faster
    'R0' : 10,
    'reference_radius' : 10.0

    }

###########################
# Equation of state setup #
###########################

q_index = 0.15 # sound speed profile exponent <----ITS DOESN'T CHANGE IN THE CODE!CHANGE IT IN SRC/PHANTOMSETUP/PHANTOMSETUP/DEFAULTS.PY
Equation_of_state_setup = {

    'ieos' : 3, # Locally Isothermal Disc --> q_index = qfacdisc
    'isink' : 1,
    'q_index' : q_index, # sound speed profile exponent

    'my_temp_exp' : 2*q_index, # Temperature profile exponent. This is always double q_index
    'T0' : 280,        # Isn't calculated in the Code
    'Tinf' : 10,
    'R0_temp' : 0.25

    }


##############
# Sink setup #
##############

Sink_setup={

    'qfacdisc' : q_index,          # Equal with q_index for a locally isothermal simulation
    'stellar_mass' : 1.0,
    'stellar_accretion_radius' : 1

    }

stellar_position = (0.0, 0.0, 0.0)
stellar_velocity = (0.0, 0.0, 0.0)


################################################################################
# Calculate the simualtion run time based on number of orbits and size of disc #
################################################################################
period = (Disc_setup['radius_max'] **(3/2)) # Outer orbital period in years.
tmax = ((period * System_constants['yr'] * Disc_setup['norbits'])/System_constants['utime']) # Simulation runtime in code units to follow disc for norbits
time_between_dumps = tmax/100 # Time in code units between dumps, by default set to produce 100 dump files

igas = phantomsetup.defaults.PARTICLE_TYPE['igas']
prefix = 'disc'
particle_type = igas


length_unit = phantomsetup.units.unit_string_to_cgs('au')
mass_unit = phantomsetup.units.unit_string_to_cgs('solarm')
gravitational_constant = 1.0



def density_distribution(radius, p_index, disc_mass,R0,radius_min,radius_max):
    """Disc surface density distribution.
    """
    return phantomsetup.disc.my_surface_density(radius, p_index, disc_mass,R0,radius_min,radius_max)



setup = phantomsetup.Setup()
setup.prefix = prefix
setup.set_units(
    length=length_unit, mass=mass_unit, gravitational_constant_is_unity=True
)
tree_accuracy=0.3
setup.set_run_option('tmax', tmax)
setup.set_run_option('dtmax', time_between_dumps)
setup.set_run_option('beta', Disc_setup['beta_art'])
setup.set_compile_option('GRAVITY', True)
setup.set_run_option('tree_accuracy', 0.3)
setup.set_run_option('tree_accuracy', tree_accuracy)

aspect_ratio = phantomsetup.eos.get_aspect_ratio_new(Equation_of_state_setup['T0'],
Equation_of_state_setup['R0_temp'], Equation_of_state_setup['Tinf'], Equation_of_state_setup['my_temp_exp'],
Disc_setup['reference_radius'], Sink_setup['stellar_mass'],gravitational_constant)


polyk = phantomsetup.eos.polyk_for_locally_isothermal_disc_mine(
    Equation_of_state_setup['T0'],Equation_of_state_setup['q_index'], Disc_setup['reference_radius'],
    Sink_setup['stellar_mass'], gravitational_constant,aspect_ratio)


setup.set_equation_of_state(ieos=Equation_of_state_setup['ieos'], polyk=polyk)
setup.set_run_option('isink', Equation_of_state_setup['isink'])


setup.set_dissipation(disc_viscosity=True, alpha=Disc_setup['alpha_art'])



setup.add_sink(
    mass=Sink_setup['stellar_mass'],
    accretion_radius=Sink_setup['stellar_accretion_radius'],
    position=stellar_position,
    velocity=stellar_velocity,

)



disc = phantomsetup.Disc(
    particle_type=particle_type,
    T0 = Equation_of_state_setup['T0'],
    Tinf = Equation_of_state_setup['Tinf'],
    R0 = Disc_setup['R0'],
    R0_temp = Equation_of_state_setup['R0_temp'],
    number_of_particles=Disc_setup['number_of_particles'],
    disc_mass=Disc_setup['disc_mass'],
    density_distribution=density_distribution,
    radius_max=Disc_setup['radius_max'],
    radius_range=(Disc_setup['radius_min'], Disc_setup['radius_max']),
    q_index=Equation_of_state_setup['q_index'],
    qfacdisc = Sink_setup['qfacdisc'],
    my_temp_exp = Equation_of_state_setup['my_temp_exp'],
    p_index=Disc_setup['p_index'],
    aspect_ratio=aspect_ratio,
    reference_radius=Disc_setup['reference_radius'],
    stellar_mass=Sink_setup['stellar_mass'],
    gravitational_constant=gravitational_constant,
    # extra_args=(radius_critical,gamma),
    extra_args=(Disc_setup['p_index'],Disc_setup['disc_mass'],Disc_setup['R0'],Disc_setup['radius_min'],
                Disc_setup['radius_max']),
    # extra_args=(p_index,reference_radius)
)

setup.add_container(disc)


working_dir = cwd


setup.write_dump_file(directory=working_dir)
setup.write_in_file(directory=working_dir)


read_me_file = open(cwd+'/disc_setup_README.txt','w')

print("#" * 50,file=read_me_file)
print("               Accretion disc setup               ",file=read_me_file)
print("-" * 50,file=read_me_file)
print('Stellar mass             = ', Sink_setup['stellar_mass'], 'solar masses',file=read_me_file)
print('Stellar accretion radius = ', Sink_setup['stellar_accretion_radius'], 'AU',file=read_me_file)
print('Disc mass                = ', Disc_setup['disc_mass'], 'solar masses',file=read_me_file)
print('Disc radius              = ', Disc_setup['radius_max'], 'AU',file=read_me_file)
print('Initial temperature T0   = ', Equation_of_state_setup['T0'], 'Kelvin',file=read_me_file)
print('Number of particles      = ', Disc_setup['number_of_particles'],file=read_me_file)
print('Number of orbits         = ', Disc_setup['norbits'],file=read_me_file)
print('Artificial viscosity α   = ', Disc_setup['alpha_art'],file=read_me_file)
print('Sound speed profile exp  = ', q_index,file=read_me_file)
print('qfacdisc exponent        = ', Sink_setup[ 'qfacdisc'],file=read_me_file)
print('Temperature profile exp  = ', Equation_of_state_setup['my_temp_exp'],file=read_me_file)
print("-" * 50,file=read_me_file)
print(" Edit the disc.in file to change runtime options, ",file=read_me_file)
print("    any values not defined are set to default     ",file=read_me_file)
# print("-" * 50,file=read_me_file)
# print("           Set the following in disc.in           ",file=read_me_file)
# print("-" * 50,file=read_me_file)
print("#" * 50,file=read_me_file)

read_me_file.close()

###################################################################################
# Calculate parameter for Fragmatation M_disc/M_star >= H/R * M_star (Gammie 2001)#
###################################################################################

w = Disc_setup['disc_mass']/Sink_setup['stellar_mass'] 

if w >= aspect_ratio:
    print(True, 'The disc will fragment, {:f} >= {:f}'.format(w,aspect_ratio))
else:
    print(False, 'The disc will NOT fragment, {:f} < {:f}'.format(w,aspect_ratio))

print('Initial conditions generated successfully. See disc_setup_README for full log')
print('Script duration {}:'.format(datetime.datetime.now() - begin_time))
