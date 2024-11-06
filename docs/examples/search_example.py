"""
Example matched filter search using Starcatto
"""

import warnings

import matplotlib.pyplot as plt
import numpy as np
from bilby.gw.utils import matched_filter_snr

from burst_search_pipeline.snr import compute_snr
from burst_search_pipeline.waveform_generator import WAVEFORM_GENERATOR
from burst_search_pipeline.lvk_interferometers import load_interferometers_with_injection
from burst_search_pipeline.plotting import plot_freq_domain, plot_time_domain, plot_time_and_freq_domain

np.random.seed(1)

DATA_COL = 'tab:gray'
SIGNAL_COL = 'tab:orange'
PSD_COL = 'black'

warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")

# Specify the output directory and the name of the simulation.
outdir = "outdir"
label = "supernova"

injection_parameters = dict(
    luminosity_distance=2,  # kpc
    geocent_time=1126259642.413,
    ra=0,
    dec=0,
    psi=0
)
data = load_interferometers_with_injection(injection_parameters)
ax = plot_time_and_freq_domain(data.interferometers[0], data.time_domain_strain['plus'], data.frequency_domain_strain['plus'])
plt.savefig("supernova.png")




