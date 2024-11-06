import numpy as np
import matplotlib.pyplot as plt

import warnings

import bilby
import matplotlib.pyplot as plt
import numpy as np
from bilby.gw import utils as gwutils
from starccato import generate_signals
"""
# # single interferometer
# snr_kwgs = dict(
#     data=ifos[0].frequency_domain_strain,
#     psd=ifos[0].power_spectral_density_array,
#     freq=ifos[0].frequency_array,
#     fmask=ifos[0].strain_data.frequency_mask
# )
# best_snr = compute_snr(signal=injection_strain['plus'], **snr_kwgs)
"""

np.random.seed(2)




def inner_product(aa, bb, frequency, PSD):
    integrand = np.conj(aa) * bb / PSD
    df = frequency[1] - frequency[0]
    integral = np.sum(integrand) * df
    return 4. * np.real(integral)


def compute_snr(signal, data, freq, psd, fmask):
    """

    matched_filter_snr = <d|h> / sqrt <h|h>
    optimal_snr = sqrt <h|h>
    """
    d = data.astype(np.complex128)[fmask]
    h = signal.astype(np.complex128)[fmask]
    dh = inner_product(d, h, freq[fmask], psd[fmask])
    hh = inner_product(h, h, freq[fmask], psd[fmask])
    o_snr = np.sqrt(hh)
    mf_snr = dh / o_snr
    return mf_snr, o_snr
