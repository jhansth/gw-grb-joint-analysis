# Glossary and Units

Terms used across the repository, with units where relevant.

- `GW`: gravitational wave trigger
- `GRB`: gamma-ray burst trigger
- `BNS`: binary neutron star system
- `SNR`: signal-to-noise ratio (dimensionless; simulated proxy)
- `fluence`: GRB fluence (arbitrary units in this simulation)
- `ra`: right ascension (radians)
- `dec`: declination (radians)
- `theta`: angular separation between two sky positions (radians)
- `delta_t`: absolute time separation |t_gw - t_grb| (seconds)
- `DELTA_T`: coincidence time threshold (seconds)
- `DELTA_OMEGA`: coincidence sky threshold (radians)
- `SIGMA_T`: Gaussian time kernel width (seconds)
- `SIGMA_OMEGA`: Gaussian sky kernel width (radians)
- `I_t`: time overlap kernel, exp(-0.5 * (delta_t / SIGMA_T)^2)
- `I_omega`: sky overlap kernel, exp(-0.5 * (theta / SIGMA_OMEGA)^2)
- `I_theta`: combined overlap kernel, I_t * I_omega
- `R_gw`: GW trigger rate (1/second)
- `R_grb`: GRB trigger rate (1/second)
- `correlated GRB`: a simulated GRB tied to a GW event with a small time/sky offset
- `time_offset_s`: delay between GW and GRB times for correlated events (seconds)
- `sky_offset_rad`: angular separation between GW and GRB positions (radians)
- `GW_SKY_SMOOTH_FWHM_DEG`: smoothing width for GW sky maps (degrees)
- `GRB_SKY_SMOOTH_FWHM_DEG`: smoothing width for GRB sky maps (degrees)
- `H_nn`: both triggers are noise
- `H_sn`: GW is signal, GRB is noise
- `H_ns`: GW is noise, GRB is signal
- `H_ss`: both are signals but from distinct sources
- `H_C`: both are signals from the same source
- `Lambda`: ranking statistic, p(D|H1) / p(D|H0)
- `p_H0_D`: posterior p(H0 | D)
- `p_H1_D`: posterior p(H1 | D)
- `GPS time`: continuous seconds used in GW analysis (not UTC)
