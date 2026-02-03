#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_HOME="$HOME/venv_linux"
VENV_LOCAL="$ROOT_DIR/venv_linux"

if [ -f "$VENV_HOME/bin/activate" ]; then
  # Preferred: venv in WSL home for speed and stability
  source "$VENV_HOME/bin/activate"
elif [ -f "$VENV_LOCAL/bin/activate" ]; then
  # Fallback: venv inside the repo
  source "$VENV_LOCAL/bin/activate"
else
  echo "Could not find venv_linux. Run setup_wsl.sh first." >&2
  exit 1
fi

cd "$ROOT_DIR"

python src/simulate_grb.py
python src/simulate_gw.py
python src/coincidence.py
python src/statistics.py
python src/plotting.py

echo "Pipeline complete. Figures saved to $ROOT_DIR/figures"
