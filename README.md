# Burst search pipeline

Our burst-search pipeline for the [NSF HDR A3D3: Detecting Anomalous Gravitational Wave Signals](https://www.codabench.org/competitions/2626/) challenge.


## Provided Training Dataset
- Data from LVK O3a
- sampling rate: 4096 Hz
- blocks: data in blocks of 200 samples (50 milliseconds)
- channels: always 2 channels (H1, L1) of data

**Final shape: (Nblocks, 200 samples per block, 2 channels)**

Three files:
- *background.npz*: background noise from the O3a observation period (no GW signals, glitches)
- *bbh_for_challenge.npy*: synthetic BBH signals 
- *sglf_for_challenge.npy*:  low-frequency Sine-Gaussian signals 


## Expected predictions

Predicted probability for if there is an "anomalous" signal or not 

- Supernovae
- Continuous Waves from Spinning Neutron Stars
- Stochastic Background
- Cosmic Strings
- Primordial Gravitational Waves


