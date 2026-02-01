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

## Setup (Windows with WSL2 - REQUIRED)

### Why WSL2?
This project uses **healpy** for HEALPix spherical data analysis. On Windows, `pip install healpy` fails because:
- Healpy has NO pre-built Windows wheels on PyPI
- It requires C++ compilation with external libraries (cfitsio, healpix_cxx, sharp)
- These libraries don't compile properly on Windows

**Solution:** Use **WSL2 (Windows Subsystem for Linux)** where healpy installs with one command.

### Step 1: Install WSL2 (One-time Setup)

**Option A: Automatic (Recommended)**
1. Open **PowerShell as Administrator** (right-click → Run as Administrator)
2. Run: `wsl.exe --install Ubuntu`
3. **Restart your computer** when prompted
4. Ubuntu will finish installing automatically (may take 5-10 minutes)
5. Create a WSL username and password

**Option B: Manual (if automatic fails)**
1. Open PowerShell as Administrator
2. Run: `wsl.exe --install --distribution Ubuntu`
3. Restart computer
4. Follow on-screen setup

**Verify installation:**
```powershell
wsl --list --verbose
```
You should see Ubuntu with version 2.

### Step 2: Create Project Environment (One-time Setup)

1. **Open PowerShell (regular, not admin)**
2. **Enter WSL:**
   ```powershell
   wsl
   ```
   You're now in Linux bash shell (prompt shows `user@computer:/mnt/c/...`)

3. **Navigate to project:**
   ```bash
   cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
   ```

4. **Run setup script (installs everything automatically):**
   ```bash
   bash setup_wsl.sh
   ```
   This script will:
   - Update Ubuntu packages
   - Install Python 3 development tools
   - Create `venv_linux` virtual environment
   - Install all dependencies from `requirements.txt` (including healpy)
   
   **This takes 5-10 minutes. Wait for completion.**

5. **Verify healpy is installed:**
   ```bash
   source venv_linux/bin/activate
   python -c "import healpy; print('healpy version:', healpy.__version__)"
   ```
   You should see: `healpy version: 1.X.X`

### Step 3: Use venv_linux for All Project Work

**IMPORTANT:** Delete or ignore `venv39` and `venv310`. They can't run healpy. Use **only venv_linux in WSL2**.

## How to Run

### Every Session: Activate Environment

**Open PowerShell and run:**
```powershell
wsl
cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
source venv_linux/bin/activate
```

After activation, your prompt will show: `(venv_linux) user@computer:...`

### Run Python Scripts
```bash
python src/simulate_grb.py
python src/simulate_gw.py
python src/coincidence.py
python src/statistics.py
```

### Run Jupyter Notebooks
```bash
jupyter notebook notebooks/exploration.ipynb
```
This opens Jupyter in your browser. Access via `http://localhost:8888`

### Run Plotting Scripts
```bash
python src/plotting.py
```

### Deactivate When Done
```bash
deactivate
exit
```

## Troubleshooting

### Problem: "WSL is not installed"
**Solution:** Run in PowerShell as Admin: `wsl.exe --install Ubuntu`

### Problem: "bash: setup_wsl.sh: command not found"
**Solution:** Check your location with `pwd`. Should be in `/mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis`

### Problem: "healpy: No module named healpy"
**Solution:** Make sure to activate venv_linux: `source venv_linux/bin/activate`

### Problem: Jupyter won't start
**Solution:** Install jupyter first: `pip install jupyter`

### Problem: Want to go back to Windows?
**Solution:** Type `exit` in WSL to return to PowerShell

## File Locations

Your files are accessible in both Windows and WSL:
- **Windows:** `C:\Users\NextGenn\Research\PP\gw-grb-joint-analysis\`
- **WSL:** `/mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis/`

Edit files in VS Code on Windows, and they automatically sync with WSL.

## Virtual Environment Details

**venv_linux includes ALL packages from requirements.txt:**
- ✅ Data: numpy, pandas, scipy, astropy
- ✅ Plotting: matplotlib, pillow
- ✅ **HEALPix: healpy** (why we need WSL2)
- ✅ Utilities: PyYAML, python-dateutil, etc.

**You do NOT need to:**
- Install anything else
- Use pip install for individual packages
- Worry about venv39/venv310
- Worry about Windows package versions
