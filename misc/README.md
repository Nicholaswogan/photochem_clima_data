# misc

This folder contains miscellaneous data.

**`H2SO4.dat`**

A Fortran binary file that contains the saturation data for H2SO4 mixed with water. Its file format is
  - Number of temperatures (integer(4))
  - Number of H2O values (integer(4))
  - Temperature array in Kelvin (real(8))
  - H2O pressure array in log10 bars (real(8))
  - H2SO4 saturation pressure shape (size of temperatures,size of H2O). In log10 bars. (real(8))