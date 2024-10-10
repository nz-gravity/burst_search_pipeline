# Burst search pipeline

Our burst-search pipeline for the [NSF HDR A3D3: Detecting Anomalous Gravitational Wave Signals](https://www.codabench.org/competitions/2626/) challenge.


## Dataset
- Data from LVK O3a
- sampling rate: 4096 Hz
- blocks: data in blocks of 200 samples (50 milliseconds)
- channels: always 2 channels (H1, L1) of data

**Final shape: (Nblocks, 200 samples per block, 2 channels)**
