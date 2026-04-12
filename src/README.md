# Source Code

This folder contains the Python scripts that run the simulation and analysis.

Core scripts:
- `simulate_gw.py`: generates GW trigger catalog
- `simulate_grb.py`: generates GRB trigger catalog
- `coincidence.py`: finds coincident GW–GRB pairs and ranks them
- `statistics.py`: summarizes the run in `summary_stats.txt`
- `plotting.py`: creates sky maps from simulated triggers
- `analysis_plots.py`: creates histograms and scatter plots
- `overlap_skymap.py`: overlap of real FITS sky maps (optional)
- `pipeline.py`: one-command pipeline runner
