import numpy as np
import matplotlib.pyplot as plt

# Constants for the models
f_0_ligo = 215  # Reference frequency for LIGO (Hz)
f_0_virgo = 500  # Reference frequency for Virgo (Hz)
f_0_kagra = 500  # Reference frequency for KAGRA (Hz)

# LIGO (Advanced LIGO design sensitivity) PSD
def ligo_psd(f):
    x = f / f_0_ligo
    S_0 = 1e-49  # Normalization constant in Hz^(-1)
    return S_0 * (x**(-4.14) - 5 * x**(-2) + 111 * ((1 - x**2 + (x**4) / 2) / (1 + (x**2) / 2)))


# Frequency range for plotting the PSD
frequencies = np.logspace(1, 4, 1000)  # Frequency range from 10 Hz to 10 kHz

# Compute the PSD for each detector
psd_ligo = ligo_psd(frequencies)
# Plot the PSDs
plt.figure(figsize=(10, 6))
plt.loglog(frequencies, psd_ligo, label="LIGO (Design Sensitivity)")
plt.show()