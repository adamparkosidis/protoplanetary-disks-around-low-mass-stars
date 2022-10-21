# Protoplanetary Discs around Low Mass Stars: The effect of the Temperature on the Disc Structure

## Abstract

Planets form in young protoplanetary discs that are made of gas and dust. We simulate locally isothermal gaseous protoplanetary discs evolving around low mass stars using the SPH code ``PHANTOM'' while varying the disc-to-star mass ratio and the initial exponent of the temperature profile. We investigate different temperature profiles and different disc-to-star mass ratios to estimate the surface density profile of the disc when it reaches the equilibrium state.  We refer to the period before this point as the time taken for the discs to relax (approximately few $kyrs$). Each simulation evolves for $5000yr$, which corresponds to 5 orbits of the outer radius of the disc. The disc-to-star mass ratio,$w$, is set to $0.01, 0.05$ and $0.1$, while the temperature profile follows a power law $T_{disc} \propto r^{-q}$. We find that the transport of angular momentum towards the disc outer region is more efficient in colder discs, thus discs with steeper initial temperature profile result to steeper surface density profile when they reach the equilibrium state. Furthermore we find that more massive systems-more massive discs around more massive stars- also result to steeper surface density profile after they have relaxed. Surprisingly, we find that the aforementioned behavior does not apply in the case of the least massive star ($M_{\star}=0.2M_{\odot}$). Furthermore, we see that this discrepancy becomes greater for bigger values of $w$ corresponding to more massive discs around the star. 


## PHANTOM

[PHANTOM](https://phantomsph.bitbucket.io) was used to simulate locally isothermal gaseous protoplanetary discs evolving around low mass stars.

Phantom is a fast, parallel, modular and low-memory smoothed particle hydrodynamics (SPH) and magnetohydrodynamics code developed over the last decade for astrophysical applications in three dimensions. The code has been developed with a focus on stellar, galactic, planetary and high energy astrophysics and has already been used widely for studies of accretion discs and turbulence, from the birth of planets to how black holes accrete.

## Samples

![2D-image-disk_initially](/figures/Graphs_2D/r_1s_0.1d_0.3q_2D.png)
![1D-image-disk_initially](/figures/Graphs_1D/r_1s_0.1d_0.3q_1D.png)
![effect-of-initial-temperature](/figures/figure2.png)