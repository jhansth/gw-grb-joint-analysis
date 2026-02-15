# Repository Tour (Beginner-Friendly)

This document explains what this repository contains, what each file does, and how the workflow fits together.

## 1) What this project is

This project simulates **gravitational-wave (GW)** and **gamma-ray burst (GRB)** trigger events and then checks for **coincidences** between the two populations.

A coincidence means:
- events happen close in time, and
- events are close in sky position.

The project is simulation-oriented and focused on conceptual multimessenger analysis.

## 2) Top-level files and folders

- `README.md`: Main introduction and setup/running instructions.
- `QUICKSTART.md`: Short command-first startup guide.
- `WSL2_SETUP.md`: Extra setup guidance for Windows+WSL2 users.
- `PROJECT_STATUS.md`: Cleanup/status snapshot of the repository.
- `CLEANUP_REPORT.md`: Earlier cleanup audit and recommendations.
- `requirements.txt`: Python dependencies (stored in UTF-16 encoding).
- `setup_wsl.sh`: Script to initialize a WSL environment.
- `src/`: Python source modules.
- `data/`: Data outputs (currently includes `coincidences_debug.csv`).
- `docs/`: Documentation files (`methodology.md` is currently empty).
- `figures/`: Generated visual assets.
- `notebooks/`: Jupyter notebook(s) for exploratory analysis.

## 3) Source code walkthrough (`src/`)

### `src/config.py`
Defines core thresholds used in coincidence logic:
- `DELTA_T = 5.0` seconds (time-window threshold)
- `DELTA_OMEGA = 0.2` radians (angular-separation threshold)

### `src/simulate_gw.py`
Function: `simulate_gw_events(n=50, t0=1.126e9)`
- Creates `n` random GW event times over a 10,000-second span.
- Creates random GW signal-to-noise ratios (`snr`) from a normal distribution.
- Creates random sky coordinates (`ra`, `dec`).
- Returns a pandas DataFrame with columns:
  - `time_gps`, `snr`, `ra`, `dec`.

### `src/simulate_grb.py`
Function: `simulate_grb_events(n=20, t0=1.126e9)`
- Creates `n` random GRB event times over a 10,000-second span.
- Creates random GRB fluence values from a lognormal distribution.
- Creates random sky coordinates (`ra`, `dec`).
- Returns a pandas DataFrame with columns:
  - `time_gps`, `fluence`, `ra`, `dec`.

### `src/coincidence.py`
Function: `angular_distance(ra1, dec1, ra2, dec2)`
- Computes great-circle angular separation (in radians) on the celestial sphere.

Function: `find_coincidences(gw, grb, dt, domega)`
- Brute-force loops over every GW event against every GRB event.
- First applies absolute time difference threshold `dt`.
- Then applies angular threshold `domega`.
- Stores accepted matches as tuples:
  - `(gw_time_gps, grb_time_gps, angular_distance_rad)`.

### `src/statistics.py`
Function: `ranking_statistic(p_signal, p_noise)`
- Minimal ranking score computed as ratio `p_signal / p_noise`.
- Intended as a placeholder/simple baseline statistic.

## 4) Data and outputs

### `data/coincidences_debug.csv`
Current debug output with columns:
- `gw_time`
- `grb_time`
- `angle_rad`

The values represent candidate coincidence pairs and their angular separations.

## 5) Typical workflow

1. Activate Python environment (WSL2 guidance is in README/QUICKSTART).
2. Simulate GW triggers with `simulate_gw_events`.
3. Simulate GRB triggers with `simulate_grb_events`.
4. Run `find_coincidences` using configured thresholds.
5. Optionally score/compare candidates using `ranking_statistic`.
6. Explore and visualize in notebook(s).

## 6) Current state and limitations

- Core code is intentionally compact and educational.
- Coincidence search is O(N_gw * N_grb), suitable for small simulations.
- `statistics.py` currently contains only a very simple ratio metric.
- `docs/methodology.md` exists but has no content yet.
- `requirements.txt` is UTF-16 encoded, which can look garbled in some terminals/editors.

## 7) If you're starting from zero

- Think of this as a toy multimessenger pipeline prototype.
- The repository is more about the **analysis flow** than production-scale performance.
- Best first reading order:
  1. `README.md`
  2. `src/simulate_gw.py`
  3. `src/simulate_grb.py`
  4. `src/coincidence.py`
  5. `src/statistics.py`
  6. notebook in `notebooks/`

