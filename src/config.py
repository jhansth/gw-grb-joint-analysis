"""Central configuration for thresholds, distributions, and priors."""

# Time coincidence window (seconds)
DELTA_T = 5.0

# Sky coincidence threshold (radians)
DELTA_OMEGA = 0.2

# Overlap kernel widths (Gaussian)
SIGMA_T = DELTA_T / 2.0
SIGMA_OMEGA = DELTA_OMEGA / 2.0

# Signal distribution parameters (match simulation)
SNR_SIGNAL_MU = 10.0
SNR_SIGNAL_SIGMA = 2.0

FLUENCE_LOGNORM_MU = -7.0
FLUENCE_LOGNORM_SIGMA = 0.5

# Correlated GRB settings (make simulations more realistic)
# A fraction of GRBs are tied to GW events with small time/sky offsets.
ENABLE_CORRELATED_GRB = True
CORRELATED_GRB_FRACTION = 0.2
GRB_DELAY_MU = 0.0
GRB_DELAY_SIGMA = 0.5
GRB_SKY_SIGMA_DEG = 2.0

# Sky map smoothing (to reflect GW large maps vs GRB small maps)
GW_SKY_SMOOTH_FWHM_DEG = 15.0
GRB_SKY_SMOOTH_FWHM_DEG = 2.0

# Hypothesis priors (sum to 1.0)
PRIOR_HSN = 0.01
PRIOR_HNS = 0.01
PRIOR_HSS = 0.009
PRIOR_HC = 0.001
PRIOR_HNN = 1.0 - (PRIOR_HSN + PRIOR_HNS + PRIOR_HSS + PRIOR_HC)
