# Outputs Reference

This document explains the files created by the pipeline and what each field means.

## Simulated trigger files

### `data/simulated/gw_triggers.csv`
Columns:
- `event_id`: string ID like `GW001`
- `time_gps`: GPS timestamp (seconds)
- `snr`: simulated signal-to-noise ratio (dimensionless)
- `ra`: right ascension (radians)
- `dec`: declination (radians)

### `data/simulated/grb_triggers.csv`
Columns:
- `event_id`: string ID like `GRB001`
- `time_gps`: GPS timestamp (seconds)
- `fluence`: simulated fluence (arbitrary units in this toy model)
- `ra`: right ascension (radians)
- `dec`: declination (radians)

## Coincidence results

### `data/results/coincident_events.csv`
Each row is a GW–GRB pair that passes the coincidence thresholds.

Columns:
- `gw_event_id`: GW trigger ID
- `grb_event_id`: GRB trigger ID
- `gw_time`: GW trigger time (GPS seconds)
- `grb_time`: GRB trigger time (GPS seconds)
- `delta_t`: absolute time separation |t_gw - t_grb| (seconds)
- `angle_rad`: sky separation (radians)
- `gw_snr`: GW SNR used in signal proxy
- `grb_fluence`: GRB fluence used in signal proxy
- `I_t`: Gaussian time overlap kernel
- `I_omega`: Gaussian sky overlap kernel
- `I_theta`: combined overlap kernel (I_t * I_omega)
- `p_gw_signal`: Normal PDF(snr; mu, sigma)
- `p_grb_signal`: LogNormal PDF(fluence; mu, sigma)
- `p_D_HC`: likelihood proxy for common-source hypothesis
- `p_D_Hnn`: likelihood proxy for noise-noise hypothesis
- `p_D_Hsn`: likelihood proxy for signal-noise hypothesis
- `p_D_Hns`: likelihood proxy for noise-signal hypothesis
- `p_D_Hss`: likelihood proxy for signal-signal (distinct sources)
- `p_D_H0`: total null likelihood (weighted sum of Hnn, Hsn, Hns, Hss)
- `p_D_H1`: signal likelihood (HC weighted by prior)
- `rank_lambda`: Lambda = p(D|H1) / p(D|H0)
- `p_H0_D`: posterior p(H0|D) = 1 / (1 + Lambda)
- `p_H1_D`: posterior p(H1|D) = Lambda / (1 + Lambda)

## Summary statistics

### `data/results/summary_stats.txt`
This file is a small report with:
- total trigger counts
- coincidence count
- min/mean/max angular separation
- mean/max Lambda
- mean/max p(H1|D)
- thresholds and priors used in the run

## Figures

### Sky plots from `src/plotting.py`
- `gw_grb_density.png`: combined sky density map
- `gw_density.png`: GW-only density map
- `grb_density.png`: GRB-only density map
- `gw_grb_overlap.png`: overlap map from normalized density product
- `gw_points_snr.png`: GW triggers colored by SNR
- `grb_points_fluence.png`: GRB triggers colored by fluence
- `gw_grb_publication.png`: combined GW+GRB points

### Analysis plots from `src/analysis_plots.py`
- `analysis_delta_t_hist.png`: time offset histogram
- `analysis_angle_hist.png`: sky separation histogram
- `analysis_rank_lambda_hist.png`: log10 Lambda histogram
- `analysis_pH1_hist.png`: p(H1|D) histogram
- `analysis_dt_vs_angle.png`: delta_t vs angle scatter
- `analysis_no_coincidences.png`: placeholder if no coincidences
