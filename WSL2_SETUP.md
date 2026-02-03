# WSL2 Setup Guide for Windows

## Prerequisites
This project requires `healpy`, which does not have Windows binary wheels. Use WSL2 (Windows Subsystem for Linux).

## Step 1: Install WSL2

1. Open PowerShell as Administrator
2. Run:
   ```powershell
   wsl --install
   ```
3. Restart when prompted
4. Ubuntu will finish installing (may take a few minutes)

## Step 2: Set Up the Project in WSL

Once WSL2 is installed:

1. Open PowerShell (no admin required)
2. Enter WSL:
   ```powershell
   wsl
   ```
3. Navigate to the project:
   ```bash
   cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
   ```
4. Run the automated setup script:
   ```bash
   bash setup_wsl.sh
   ```

The script will:
- Update Ubuntu packages
- Install Python development tools
- Create a virtual environment in `~/venv_linux`
- Install all dependencies (including healpy)

## Step 3: Use the Environment

Activate the virtual environment:
```bash
source ~/venv_linux/bin/activate
```

Run the full pipeline:
```bash
bash run_pipeline.sh
```

Run scripts individually:
```bash
python src/simulate_grb.py
python src/simulate_gw.py
python src/coincidence.py
python src/statistics.py
python src/plotting.py
```

Run the notebook:
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

Deactivate when done:
```bash
deactivate
```

## Step 4: Accessing Files from Windows

Your Windows files are accessible in WSL at:
```
/mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
```

You can edit files in VS Code on Windows and they will sync with WSL.

## Troubleshooting

WSL will not install?
- Ensure virtualization is enabled in BIOS
- Some Windows editions may require additional features

Healpy not found?
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Remove WSL later:
```powershell
wsl --unregister Ubuntu
```
