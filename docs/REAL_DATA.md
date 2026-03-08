# Using Real GW and GRB Data

This project is simulation-first, but you can run the same pipeline with real catalogs by creating compatible CSV files.

## Required columns
Your CSVs should match the simulated format.

For GW:
- `event_id`
- `time_gps`
- `snr`
- `ra`
- `dec`

For GRB:
- `event_id`
- `time_gps`
- `fluence`
- `ra`
- `dec`

## GW data workflow (catalog + sky map)
1. Choose a GW event catalog source (for example, GWOSC).
2. For each event, record a trigger time and a representative sky position.
3. If you have a sky map, take the maximum-probability pixel and convert it to RA/Dec.
4. Convert event times to GPS seconds.
5. Write `data/simulated/gw_triggers.csv` in the required format.

Example: UTC to GPS conversion using astropy
```python
from astropy.time import Time
t = Time("2017-08-17T12:41:04", format="isot", scale="utc")
gps_time = t.gps
```

## GRB data workflow (catalog + localization)
1. Choose a GRB catalog source (for example, Fermi GBM or Swift).
2. Collect trigger time and sky position for each GRB.
3. Convert times to GPS seconds (often GRB times are UTC or mission elapsed time).
4. Write `data/simulated/grb_triggers.csv` in the required format.

## Run the pipeline on real data
Once the two CSVs are prepared:
```bash
python src/coincidence.py
python src/statistics.py
python src/plotting.py
python src/analysis_plots.py
```

## Overlap sky maps from FITS
If you have HEALPix FITS maps for GW and GRB localization:
```bash
python src/overlap_skymap.py --gw-map path/to/gw_skymap.fits --grb-map path/to/grb_skymap.fits
```

## Notes
- Ensure RA/Dec are in radians. Convert degrees if needed.
- If sky maps have different NSIDE, reproject to a common NSIDE before overlap.
- This pipeline treats each trigger as a point estimate, not a full posterior.
