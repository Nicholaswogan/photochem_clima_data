# Aerosol optical properties

These files contain Mie optical properties for homogeneous spherical particles. They were generated with [`miepython`](https://github.com/scottprahl/miepython) by the [RateExplorer aerosol script](https://github.com/Nicholaswogan/RateExplorer/blob/304878abfc28a773493f8109c4e3618235b76bc1/aerosol_xsections/main.py). Reproducing the Mars dust table also requires the refractive-index file provided by Melinda Kahre through personal communication; that file is not in the RateExplorer repository.

All three tables have 1,000 logarithmically spaced wavelengths from 10 nm to 1,000 µm and 80 logarithmically spaced radii from 0.01 to 500 µm. Array datasets use gzip level 4 compression with shuffle.

The source refractive indices are linearly interpolated in wavelength. Below and above the source range, the real and imaginary indices are held at their nearest source values; Mie properties are then calculated over the full table range. The optical properties themselves are not held constant outside the source range. Each file records its source range and extrapolation method in root HDF5 attributes.

| Folder | Refractive-index source | Source wavelength range |
| --- | --- | --- |
| `khare1984` | [Khare et al. (1984)](https://www.sciencedirect.com/science/article/pii/0019103584901428), Titan tholins; data from HITRAN | 20.7 nm–920 µm |
| `marsdust` | [Wolff et al. (2009)](https://doi.org/10.1029/2009JE003350), Mars dust; data provided by Melinda Kahre | 263 nm–98.5423 µm |
| `palmer1975` | [Palmer and Williams (1975)](https://doi.org/10.1364/AO.14.000208), 95.6% H$_2$SO$_4$ and 4.4% H$_2$O; data from HITRAN | 360 nm–25 µm |

## HDF5 datasets

| Dataset       | Meaning                  | Units | Shape as read by h5py |
| ------------- | ------------------------ | ----- | --------------------- |
| `wavelengths` | Wavelength               | nm    | `(1000,)`             |
| `radii`       | Particle radius          | µm    | `(80,)`               |
| `w0`          | Single-scattering albedo | 1     | `(1000, 80)`          |
| `qext`        | Extinction efficiency    | 1     | `(1000, 80)`          |
| `g0`          | Asymmetry factor         | 1     | `(1000, 80)`          |

The two-dimensional datasets are stored with wavelength as the first axis and radius as the second. Dataset attributes record the units and axis names.
