# Quick Start Guide - GW-GRB Joint Analysis

## 60-Second Run
```powershell
wsl
```
```bash
source ~/venv_linux/bin/activate
cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
bash run_pipeline.sh
```

Outputs appear in `data/` and `figures/`.

---

## Every Time You Work

1. Enter WSL from Windows PowerShell:
```powershell
wsl
```

2. Activate Python environment:
```bash
source ~/venv_linux/bin/activate
```
Your prompt will show `(venv_linux) user@computer:~$`.

3. Go to the project:
```bash
cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
```

---

## Common Commands

### Run the full pipeline (simulations + analysis + plots)
```bash
bash run_pipeline.sh
```
This runs:
- `python -m src.pipeline` (which internally runs all steps)

Figures are saved to `figures/`.

### Run the pipeline in Python (optional)
```bash
python -m src.pipeline --n-gw 100 --n-grb 500 --seed 123
```
Defaults are `n-gw=100` and `n-grb=500` if you omit flags.

### Run simulations only
```bash
python src/simulate_grb.py
python src/simulate_gw.py
python src/coincidence.py
```

### Run Jupyter notebook
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

### Analysis plots
`src/analysis_plots.py` creates additional figures in `figures/`:
- `analysis_delta_t_hist.png`: histogram of time offsets (Delta t)
- `analysis_angle_hist.png`: histogram of angular separation (theta)
- `analysis_rank_lambda_hist.png`: histogram of log10 Lambda ranking statistic
- `analysis_pH1_hist.png`: histogram of posterior signal probability p(H1 | D)
- `analysis_dt_vs_angle.png`: scatter of Delta t versus angular separation

### Sky plots
`src/plotting.py` creates sky localization figures in `figures/`:
- `gw_grb_density.png`: combined density map
- `gw_density.png`: GW-only density map
- `grb_density.png`: GRB-only density map
- `gw_grb_overlap.png`: overlap map (normalized density product)
- `gw_density_smoothed.png`: GW density smoothed (large localization)
- `grb_density_smoothed.png`: GRB density smoothed (small localization)
- `gw_grb_overlap_smoothed.png`: overlap using smoothed maps
- `gw_grb_overlap_with_coincidences.png`: overlap with coincidence points
- `gw_points_snr.png`: GW points colored by SNR
- `grb_points_fluence.png`: GRB points colored by fluence
- `gw_grb_publication.png`: combined GW+GRB points

### Overlap from real HEALPix sky maps (FITS)
```bash
python src/overlap_skymap.py --gw-map path/to/gw_skymap.fits --grb-map path/to/grb_skymap.fits
```
Outputs:
- `figures/gw_grb_overlap_fits.png`
- `data/results/gw_grb_overlap_map.fits`

### Check package versions
```bash
pip list | grep -E "healpy|numpy|pandas"
```

### Deactivate environment
```bash
deactivate
```

### Exit WSL back to Windows
```bash
exit
```

---

## Environment Location
- Virtual environment: `~/venv_linux`
- Project files: `/mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis`
- Notebooks: `/mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis/notebooks/`

---

## Verified Working
- Python 3.12.3
- Healpy 1.19.0
- Numpy 1.26.4
- Pandas 2.3.3
- Scipy 1.13.1
- Matplotlib 3.9.4
- Astropy 6.0.1

---

## Pro Tips

### Create an alias for faster activation
```bash
echo "alias proj='cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis && source ~/venv_linux/bin/activate'" >> ~/.bashrc
source ~/.bashrc
```
Then just type: `proj`.

### Check if environment is active
```bash
which python  # Should show ~/venv_linux/bin/python
```

### List all installed packages
```bash
pip list
```

---

## Troubleshooting

Q: `command not found: source`
A: Make sure you are in WSL bash, not PowerShell.

Q: `ModuleNotFoundError: No module named healpy`
A: Activate the environment: `source ~/venv_linux/bin/activate`.

Q: Terminal frozen?
A: Press `Ctrl+C`, then close WSL and open a new PowerShell window with `wsl`.

---

Last Updated: 2026-03-01
Status: Ready for development
