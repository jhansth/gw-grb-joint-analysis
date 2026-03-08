# Data Flow and Assumptions

This page gives a one-screen summary of how data moves through the project and the core assumptions.

## Data flow (simulation)
```text
simulate_gw.py + simulate_grb.py
  -> data/simulated/gw_triggers.csv
  -> data/simulated/grb_triggers.csv
    -> coincidence.py
      -> data/results/coincident_events.csv
        -> statistics.py
          -> data/results/summary_stats.txt
        -> plotting.py + analysis_plots.py
          -> figures/*.png
```

## Data flow (real data variant)
```text
GW catalog + GRB catalog
  -> normalize time formats to GPS
  -> extract representative sky positions
  -> write gw_triggers.csv + grb_triggers.csv
    -> coincidence.py
      -> statistics.py
      -> plotting.py + analysis_plots.py
```

## Assumptions
- Triggers are point estimates in time and sky position.
- GW SNR and GRB fluence are simulated proxies, not measured values.
- Overlap is approximated with Gaussian kernels in time and sky.
- Noise rates are estimated from the simulated time span.
- Coincidence is defined by fixed thresholds `DELTA_T` and `DELTA_OMEGA`.
