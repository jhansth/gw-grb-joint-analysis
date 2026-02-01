# GW_GRB_Joint_Simulation

Simulated joint analysis of gravitational-wave and gamma-ray burst events using coincidence statistics.

## Project Overview
This project aims to simulate gravitational-wave (GW) and gamma-ray burst (GRB) events and perform joint analysis using coincidence statistics. The goal is to understand how multimessenger astronomy can identify astrophysical events with GW and GRB signals.


## Objectives
- Simulate GW and GRB trigger populations
- Implement temporal and spatial coincidence tests
- Compute joint ranking statistics and false alarm probabilities
- Build conceptual understanding of multimessenger pipelines

## Status
Simulation-only, private research repository.

## Folder Structure
- `data/`: simulated GW and GRB triggers
- `src/`: Python scripts
- `notebooks/`: Jupyter notebooks for analysis
- `results/`: graphs and tables
- `docs/`: documentation
- `figures/` : Plots and visualizations  
- `requirements.txt` : Python packages  
- `.gitignore` : Files/folders to ignore in Git 

## Setup (Windows with WSL2)

**Important:** This project requires `healpy`, which doesn't have Windows binary wheels. Use **WSL2 (Windows Subsystem for Linux)** for proper installation.

### Step 1: Install WSL2
1. Open **PowerShell as Administrator**
2. Run: `wsl.exe --install Ubuntu`
3. **Restart your computer** when prompted
4. Ubuntu will finish installing (may take several minutes)

### Step 2: Set Up Project Environment
1. Open PowerShell and enter WSL:
   ```powershell
   wsl
   ```

2. Navigate to the project:
   ```bash
   cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
   ```

3. Run the automated setup (installs Python, all dependencies, and healpy):
   ```bash
   bash setup_wsl.sh
   ```

## How to Run

### Activate the Environment
Every time you start working, activate the virtual environment:
```bash
wsl                                    # Enter WSL (if not already there)
cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
source venv_linux/bin/activate        # Activate virtual environment
```

### Run Python Scripts
```bash
python src/simulate_grb.py
python src/simulate_gw.py
python src/coincidence.py
```

### Run Jupyter Notebooks
```bash
jupyter notebook notebooks/exploration.ipynb
```

### Deactivate When Done
```bash
deactivate
```

## About venv_linux

**venv_linux automatically includes ALL dependencies** from `requirements.txt`:
- ✅ numpy, pandas, scipy, matplotlib
- ✅ astropy
- ✅ **healpy** (reason for using WSL)

**You don't need venv39 or venv310 anymore** — they can't run healpy on Windows. Only use venv_linux in WSL.

## Quick Reference
| Task | Command |
|------|---------|
| Enter WSL | `wsl` |
| Activate environment | `source venv_linux/bin/activate` |
| Run scripts | `python src/script.py` |
| Jupyter notebook | `jupyter notebook notebooks/exploration.ipynb` |
| Deactivate | `deactivate` |
| Exit WSL | `exit` |
