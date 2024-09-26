
# Aerosol optical properties

I use the `miepython` python package to compute aerosol optical properties: https://github.com/scottprahl/miepython

**Folder and File formats**

Each folder corresponds to optical properties of different types of aerosols. For example `khare1984` contains the measured index of refraction of laboratory synthetic hydrocarbon aerosols analogous to the ones that are made in Titan's atmosphere.

Each folder should contain a few files: `mie_<folder-name>.h5` (required), `frac_<folder-name>.h5` (optional), and an ascii file containing measured index of refractions.

`mie_<folder-name>.h5` - Contains calculated optical properties using mie theory. The file has the following structure

```yaml
wavelengths: Wavelength [nm]
radii: Particle radii [um]
w0: Single scattering albedo [unitless], dimensions (len(radii),len(wavelengths))
qext: Extinction [1/particle], dimensions (len(radii),len(wavelengths))
g0: Asymmetry factor [unitless], dimensions (len(radii),len(wavelengths))
```

`frac_<folder-name>.h5` (optional) - A file containing calculated optical properties using fractal theory following [Wolf and Toon (2010)](https://science.sciencemag.org/content/328/5983/1266.abstract).

## Folders

`khare1984` is data for optical properties of fractal hydrocarbon aerosols from [Khare et al. (1984)](https://www.sciencedirect.com/science/article/pii/0019103584901428) downloaded from hitran.org at this link: https://hitran.org/data/Aerosols-2016/ascii/exoplanets/khare_tholins.dat.

