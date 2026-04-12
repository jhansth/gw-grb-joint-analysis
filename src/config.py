"""Central configuration for thresholds, distributions, and priors."""

# Time coincidence window (seconds)
DELTA_T  = 5.0        # standard BNS-sGRB search window
SIGMA_T  = 1.5        # GRB 170817A arrived at +1.74s, sigma ~1-2s

# Sky coincidence threshold (radians)
DELTA_OMEGA = 1.0     # ~57 deg pre-filter, gives ~12x more background pairs
SIGMA_OMEGA = 0.20        # GW localization uncertainty (~6 deg)

# Signal distribution parameters (match simulation)
SNR_SIGNAL_MU = 10.0
SNR_SIGNAL_SIGMA = 2.0

FLUENCE_LOGNORM_MU = -7.0
FLUENCE_LOGNORM_SIGMA = 0.5

# Correlated GRB settings (make simulations more realistic)
# A fraction of GRBs are tied to GW events with small time/sky offsets.
ENABLE_CORRELATED_GRB = True
CORRELATED_GRB_FRACTION = 0.001   # 0.1% → ~20 signal GRBs in 20000
GRB_DELAY_MU = 1.7
GRB_DELAY_SIGMA = 0.5
GRB_SKY_SIGMA_DEG = 5.0          # realistic Fermi localization


# Sky map smoothing (to reflect GW large maps vs GRB small maps)
GW_SKY_SMOOTH_FWHM_DEG = 15.0
GRB_SKY_SMOOTH_FWHM_DEG = 2.0

# Hypothesis priors (sum to 1.0)
PRIOR_HSN = 0.01
PRIOR_HNS = 0.01
PRIOR_HSS = 0.009
PRIOR_HC = 0.001
PRIOR_HNN = 1.0 - (PRIOR_HSN + PRIOR_HNS + PRIOR_HSS + PRIOR_HC)
