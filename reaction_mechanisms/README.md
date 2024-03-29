`zahnle_earth.yaml` is Kevin Zahnle's network of reactions. He calls the network `earth_125.rx`. The meaning of "125" is unclear. I have documented the small changes to the network [at this Github repo.](https://github.com/Nicholaswogan/ImpactAtmosphere/blob/main/ImpactAtmosphere/data/notes.md). But from now, onward, I will document the changes here.

# 10/27/21

- Several species had valid polynomial Gibbs energy fits down to 100 K. But this was not compatible with Titan, because Titan is really cold. Therefore, I decreased the lower bounds of the fits to 50 K.
- I added many particles. Particles are made in various way from species. 

I added

```yaml
- equation: C2H4 + N2D <=> CH3CN + H
  rate-constant: {A: 2.3e-10, b: 0.0, Ea: 503}
```

I was modeling Titan, and was getting far to little CH3CN. Lavvas et al. (2008) uses this reaction rate.

I will keep the reaction for now, but note that this reaction might not be correct. From Loison et al (2015),

> The CH3CN molecule is not produced in our model by the N(2D) + C2H4 reaction but through the association reaction H+CH2CN (Balucani et al., 2012; Lee et al., 2011). We calculated the rate constant from our semi-empirical model for association reactions (Hébrard et al., 2013), the CH2CN radical being produced by the H + C2H4CN reaction (this work, C2H4CN itself being the product of the H + C2H3CN association) and the N + C2H3 reaction (Payne et al., 1996).

I would like to follow Loison et al.'s advice, but our model is missing two things

1. Radiative association reactions: A + B => AB + hv. These reactions are important for some speices in Titan's atmosphere (Vuitton et al. 2012)
2. We do not have C2H4CN in the network.

# 12/16/21

I added

```yaml
- equation: Cl + O3 <=> ClO + O2
  rate-constant: {A: 2.8e-11, b: 0.0, Ea: 250}
```

From Atkinson et al. (2007). Full citation:

> R. Atkinson, D. L. Baulch, R. A. Cox, J. N. Crowley, R. F. Hampson, et al.. Evaluated kinetic and photochemical data for atmospheric chemistry: Volume III ? reactions of inorganic halogens. Atmospheric Chemistry and Physics Discussions, European Geosciences Union, 2006, 6 (2), pp.2281-2702. ⟨hal-00301101⟩

# 12/23/21

I updated the following reaction. Rate from JPL-15

```yaml
- equation: S + O2 <=> SO + O
  rate-constant: {A: 1.6e-12, b: 0, Ea: -100.0}
```

Also added NH3aer and He.

# 3/9/23

I updated the following reaction following [Lovejoy et al. (1996)](https://doi.org/10.1021/jp962414d)

```yaml
# - equation: SO3 + H2O (+ M) <=> H2SO4 (+ M)
#   type: falloff
#   low-P-rate-constant: {A: 9.0e-29, b: -2.0, Ea: -1000.0}
#   high-P-rate-constant: {A: 3.6e-10, b: -2.0, Ea: -1000.0}
- equation: SO3 + H2O + H2O <=> H2SO4 + H2O
  rate-constant: {A: 2.3e-43, b: 1.0, Ea: -6540.0}
```

# 10/27/23

I updated a variety of thermodynamics for CH3O and H2COH, and rates for related species. All changes were motivated by [Xu et al. (2015)](https://doi.org/10.1021/acs.jpca.5b00553). Details for these changes are justified at this github repository: https://github.com/Nicholaswogan/RateExplorer/tree/main/experiments/10-02-23

I also updated thermodynamics for H2 and Cl2 following NIST, to include thermodynamic data up to 6000 K.

# 1/16/24

I added two new photolysis branches. All the H2O branches are now OH + H, H2 + O1D, and O + H + H. Branching ratios are based on JPL-19. I also added H2 photolysis, taking data from the Leiden database. 

Finally, I also, added gas-phase S8 into the code, along with 3 reactions connecting S8 to the rest of the network. These reactions + thermodynamics come from Kevin's original network he sent me (https://github.com/Nicholaswogan/ImpactAtmosphere/blob/main/ImpactAtmosphere/data). I also added S8 photolysis, but only as an opacity source (S8 absorbs light, but does not photolyze). I also added the particles S2aer and S8aer, with saturation vapor pressures based on Zahnle et al. (2016) (10.3847/0004-637X/824/2/137).
