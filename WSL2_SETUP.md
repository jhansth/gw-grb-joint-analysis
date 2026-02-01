# WSL2 Setup Guide for Windows

## Prerequisites
Your project requires **healpy**, which doesn't have Windows binary wheels. The solution is to use **WSL2 (Windows Subsystem for Linux)**.

## Step 1: Install WSL2

1. Open **PowerShell as Administrator**
2. Run:
   ```powershell
   wsl --install
   ```
3. This installs WSL2 with Ubuntu by default
4. **Restart your computer** when prompted
5. After restart, Ubuntu will finish installing (may take several minutes)

## Step 2: Set Up Your Project in WSL

Once WSL2 is installed:

1. Open a **PowerShell** terminal (no admin required)
2. Enter WSL:
   ```powershell
   wsl
   ```
3. Navigate to your project:
   ```bash
   cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
   ```
4. Run the automated setup script:
   ```bash
   bash setup_wsl.sh
   ```

This script will:
- Update Ubuntu packages
- Install Python development tools
- Create a virtual environment
- Install all dependencies (including healpy)

## Step 3: Using the Environment

### Activate the Virtual Environment
```bash
source venv_linux/bin/activate
```

### Run Python Scripts
```bash
python src/simulate_grb.py
python src/simulate_gw.py
```

### Run Jupyter Notebooks
```bash
jupyter notebook notebooks/exploration.ipynb
```

### Deactivate When Done
```bash
deactivate
```

## Step 4: Accessing Files from Windows

All your files in `C:\Users\NextGenn\Research\PP\gw-grb-joint-analysis` are accessible in WSL at:
```
/mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
```

You can edit files in VS Code on Windows, and they'll automatically sync with WSL.

## Troubleshooting

**WSL won't install?**
- Ensure virtualization is enabled in BIOS
- Windows Pro/Enterprise may be required (not Home edition)

**Still can't find healpy?**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Want to remove WSL later?**
```powershell
wsl --unregister Ubuntu
```
