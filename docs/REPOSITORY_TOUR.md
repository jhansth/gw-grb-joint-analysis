# Repository Tour (Beginner-Friendly)

This document explains what this repository contains, what each file does, and how the workflow fits together.

## 1) What this project is

This project simulates gravitational-wave (GW) and gamma-ray burst (GRB) trigger events and then checks for coincidences between the two populations.

A coincidence means:
- events happen close in time
- events are close in sky position

The project is simulation-oriented and focused on conceptual multimessenger analysis.

## 2) Top-level files and folders

- `README.md`: Main introduction and setup/running instructions.
- `QUICKSTART.md`: Short command-first startup guide.
- `WSL2_SETUP.md`: Extra setup guidance for Windows+WSL2 users.
- `PROJECT_STATUS.md`: Cleanup/status snapshot of the repository.
- `CLEANUP_REPORT.md`: Earlier cleanup audit and recommendations.
- `requirements.txt`: Python dependencies.
- `setup_wsl.sh`: Script to initialize a WSL environment.
- `run_pipeline.sh`: Shell script to run the full pipeline.
- `src/`: Python source modules.
- `data/`: Data outputs (simulated triggers and results).
- `docs/`: Documentation (`DATA_FLOW.md`, `OUTPUTS.md`, `GLOSSARY.md`, `REAL_DATA.md`, `methodology.md`).
- `figures/`: Generated visual assets.
- `notebooks/`: Jupyter notebook(s) for exploratory analysis.

## 3) Source code walkthrough (`src/`)

### `src/config.py`
Core thresholds and parameters:
- `DELTA_T`, `DELTA_OMEGA`: coincidence thresholds
- `SIGMA_T`, `SIGMA_OMEGA`: Gaussian kernel widths
- `SNR_SIGNAL_MU`, `SNR_SIGNAL_SIGMA`: GW SNR proxy distribution
- `FLUENCE_LOGNORM_MU`, `FLUENCE_LOGNORM_SIGMA`: GRB fluence proxy distribution
- `PRIOR_*`: hypothesis priors

### `src/simulate_gw.py`
Simulates GW triggers:
- times uniform over a 10,000-second span
- SNR drawn from a normal distribution
- RA and Dec drawn uniformly on the sphere
- writes `data/simulated/gw_triggers.csv`

### `src/simulate_grb.py`
Simulates GRB triggers:
- times uniform over a 10,000-second span
- fluence drawn from a log-normal distribution
- RA and Dec drawn uniformly on the sphere
- writes `data/simulated/grb_triggers.csv`

### `src/coincidence.py`
Finds GW-GRB coincidences and computes hypothesis proxies:
- angular separation via spherical cosine law
- time + sky thresholds
- overlap kernels in time and sky
- hypothesis likelihood proxies and ranking statistic
- writes `data/results/coincident_events.csv`

### `src/statistics.py`
Computes run-level summary stats:
- counts and angular separation stats
- mean and max Lambda and p(H1|D)
- writes `data/results/summary_stats.txt`

### `src/plotting.py`
Sky localization figures from simulated triggers:
- density maps, point maps, overlap map
- writes `figures/*.png`

### `src/analysis_plots.py`
Analysis plots for coincidences:
- histograms of delta_t, angle, Lambda, p(H1|D)
- scatter of delta_t vs angle
- writes `figures/*.png`

### `src/overlap_skymap.py`
Overlap visualization from real HEALPix FITS maps:
- reads GW and GRB sky maps
- writes an overlap FITS map and PNG

### `src/pipeline.py`
Optional Python entry point:
- runs simulations, coincidence, stats, and plots
- supports flags for sizes and seed

## 4) Data and outputs

See `docs/OUTPUTS.md` for full field definitions and example rows.

## 5) Typical workflow

1. Activate the WSL environment.
2. Run the full pipeline with `bash run_pipeline.sh`.
3. Inspect `data/results/` and `figures/`.

Optional:
- run `python -m src.pipeline --n-gw 1000 --n-grb 500 --seed 123`
- use `src/overlap_skymap.py` for real FITS overlap maps

## 6) Current state and limitations

- Core code is compact and educational.
- Coincidence search is O(N_gw * N_grb), suitable for small simulations.
- SNR and fluence are simulated proxies, not measured values.
- Triggers are point estimates, not full posteriors.

## 7) If you're starting from zero

Best first reading order:
1. `README.md`
2. `docs/DATA_FLOW.md`
3. `docs/OUTPUTS.md`
4. `docs/GLOSSARY.md`
5. `docs/methodology.md`
6. `src/simulate_gw.py` and `src/simulate_grb.py`
7. `src/coincidence.py`
8. `src/statistics.py`
