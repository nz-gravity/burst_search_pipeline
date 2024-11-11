import warnings

import bilby
import matplotlib.pyplot as plt
import numpy as np
from bilby.gw import utils as gwutils
from scipy.signal import gausspulse

np.random.seed(2)

DATA_COL = 'tab:gray'
SIGNAL_COL = 'tab:orange'
PSD_COL = 'black'

warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")

SAMPLING_FREQ = 4096
N_TIMESTAMPS = 256
DURATION = N_TIMESTAMPS / SAMPLING_FREQ


def __glitch(time_array, luminosity_distance, **kwargs):
    """
    A source model that reads a simulation from a text file.

    This was originally intended for use with supernova simulations, but can
    be applied to any source class.

    Parameters
    ----------
    frequency_array: array-like
        Unused (but required by the source model interface)
    file_path: str
        Path to the file containing the NR simulation. The format of this file
        should be readable by :code:`numpy.loadtxt` and have four columns
        containing the real and imaginary components of the plus and cross
        polarizations.
    luminosity_distance: float
        The distance to the source in kpc, this scales the amplitude of the
        signal. The simulation is assumed to be at 10kpc.
    kwargs:
        extra keyword arguments, this should include the :code:`file_path`

    Returns
    -------
    dict:
        A dictionary containing the plus and cross components of the signal.
    """

    fc = kwargs.get('central_freq', 250)
    i,q, e= gausspulse(time_array, fc=fc, bw=0.5, bwr=-6, tpr=-100, retquad=True, retenv=True,)


    # waveforms generated at 10kpc, so scale to the luminosity distance
    scaling = 1e-21 * (10.0 / luminosity_distance)
    waveform = scaling * q
    return {'plus': waveform, 'cross': waveform}






def _get_waveform_generator():
    # Create the waveform_generator using a supernova source function
    waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
        duration=DURATION,
        sampling_frequency=SAMPLING_FREQ,
        time_domain_source_model=__glitch,
        parameter_conversion=lambda parameters: (parameters, list()),
        waveform_arguments=dict(central_freq=250),
    )
    return waveform_generator


GLITCH_GENERATOR = _get_waveform_generator()
