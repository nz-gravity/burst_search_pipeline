# Burst search pipeline

Our burst-search pipeline for the [NSF HDR A3D3: Detecting Anomalous Gravitational Wave Signals](https://www.codabench.org/competitions/2626/) challenge.


## Dataset
- Data from LVK O3a
- sampling rate: 4096 Hz
- blocks: data in blocks of 200 samples (50 milliseconds)
- channels: always 2 channels (H1, L1) of data

**Final shape: (Nblocks, 200 samples per block, 2 channels)**



## Types of Data in the Dataset:
- Binaries: This dataset includes simulated signals from Binary Black Holes (BBH). These are synthetic signals that mimic the gravitational waves expected from black holes orbiting and eventually merging into each other. These simulated BBH signals are injected into real background noise to help train the models.
  
- Background: This dataset consists of background noise from the O3a observation period. Importantly, any known gravitational wave events and other excess power glitches have been removed from this data. This "cleaned" background noise is what participants will primarily use to train their models to detect anomalies.
  
- Sine-Gaussian: This dataset includes a type of simulated signal known as a Sine-Gaussian. These are generic low-frequency signals used to represent potential gravitational wave sources that do not fit into the well-understood categories like BBH. These signals are useful for testing how well models can detect unexpected types of gravitational waves.


By using these different datasets, participants can train and refine their models to detect anomalous gravitational wave signals that may not match any pre-defined templates. This challenge aims to push the boundaries of what we can detect in the cosmos, merging the fields of astrophysics and machine learning.
