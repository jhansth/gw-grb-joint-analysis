import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from src import config

# Load data
bg  = np.load('data/results/background_lambdas.npy')
c   = pd.read_csv('data/results/coincident_events.csv')
grb = pd.read_csv('data/simulated/grb_triggers.csv')
m   = c.merge(grb[['event_id','is_correlated']], left_on='grb_event_id', right_on='event_id')
sig = m[m['is_correlated']==True]['rank_lambda'].values
bkg = m[m['is_correlated']==False]['rank_lambda'].values

# ── Plot 1: Lambda distributions ─────────────────────────────────
fig, ax = plt.subplots(figsize=(8,5))
bins = np.linspace(0, 6, 30)
ax.hist(bg,  bins=bins, alpha=0.6, color='steelblue', label=f'Background (time slides, n={len(bg)})', density=True)
ax.hist(sig, bins=bins, alpha=0.7, color='crimson',   label=f'Signal injections (n={len(sig)})',      density=True)
ax.hist(bkg, bins=bins, alpha=0.7, color='orange',    label=f'Foreground background (n={len(bkg)})',  density=True)
ax.axvline(np.min(sig), color='crimson', linestyle='--', alpha=0.5, label='Min signal Lambda')
ax.set_xlabel(r'$\log_{10}\,\Lambda$', fontsize=13)
ax.set_ylabel('Density', fontsize=13)
ax.set_title('GW-GRB Ranking Statistic Distribution', fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig('figures/lambda_signal_vs_background.png', dpi=150)
plt.close()
print('Saved lambda_signal_vs_background.png')

# ── Plot 2: FAR vs Lambda threshold ──────────────────────────────
T_slides = 200 * 365.25 * 86400   # matches 200 slides
thresholds = np.linspace(bg.min(), bg.max(), 200)
far_per_yr = np.array([np.sum(bg >= t) / T_slides * 365.25*86400 for t in thresholds])

fig, ax = plt.subplots(figsize=(8,5))
ax.semilogy(thresholds, far_per_yr + 1e-10, color='steelblue', lw=2)
for lam in sig:
    ax.axvline(lam, color='crimson', alpha=0.15, lw=0.8)
ax.axvline(np.min(sig), color='crimson', lw=2, linestyle='--', label='Loudest signal injection')
ax.set_xlabel(r'$\log_{10}\,\Lambda$ threshold', fontsize=13)
ax.set_ylabel('FAR (yr' + r'$^{-1}$' + ')', fontsize=13)
ax.set_title('False Alarm Rate vs Ranking Statistic Threshold', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/far_vs_lambda.png', dpi=150)
plt.close()
print('Saved far_vs_lambda.png')