# Quick Start Guide - GW-GRB Joint Analysis

## ⚡ Fast Setup (Already Done!)

Your environment is ready. **Healpy 1.19.0 is installed and working.**

---

## 🚀 Every Time You Work

### 1. Enter WSL from Windows PowerShell:
```powershell
wsl
```

### 2. Activate Python environment:
```bash
source ~/venv_linux/bin/activate
```

Your prompt will show: `(venv_linux) extenn@NextGen:~$`

### 3. Go to project:
```bash
cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis
```

---

## 🔧 Common Commands

### Run simulations:
```bash
python src/simulate_grb.py
python src/simulate_gw.py
python src/coincidence.py
```

### Run Jupyter notebook:
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

### Check package versions:
```bash
pip list | grep -E "healpy|numpy|pandas"
```

### Deactivate environment:
```bash
deactivate
```

### Exit WSL back to Windows:
```bash
exit
```

---

## 🎯 Environment Location

- **Virtual Environment:** `~/venv_linux` (in WSL home directory)
- **Project Files:** `/mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis`
- **Notebooks:** `/mnt/c/.../gw-grb-joint-analysis/notebooks/`

---

## ✅ Verified Working

- ✅ Python 3.12.3
- ✅ Healpy 1.19.0
- ✅ Numpy 1.26.4
- ✅ Pandas 2.3.3
- ✅ Scipy 1.13.1
- ✅ Matplotlib 3.9.4
- ✅ Astropy 6.0.1

---

## 💡 Pro Tips

### Create an alias for faster activation:
```bash
echo "alias proj='cd /mnt/c/Users/NextGenn/Research/PP/gw-grb-joint-analysis && source ~/venv_linux/bin/activate'" >> ~/.bashrc
source ~/.bashrc
```

Then just type: `proj`

### Check if environment is active:
```bash
which python  # Should show ~/venv_linux/bin/python
```

### List all installed packages:
```bash
pip list
```

---

## 🐛 Troubleshooting

**Q: `command not found: source`**
A: Make sure you're in WSL bash, not PowerShell

**Q: `ModuleNotFoundError: No module named healpy`**
A: Activate environment: `source ~/venv_linux/bin/activate`

**Q: Terminal frozen?**
A: Press `Ctrl+C`, then close WSL and open new PowerShell window with `wsl`

---

**Last Updated:** 2026-02-01
**Status:** ✅ Ready for development
