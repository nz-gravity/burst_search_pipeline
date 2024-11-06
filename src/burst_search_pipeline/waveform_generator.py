import warnings

import bilby
import matplotlib.pyplot as plt
import numpy as np
from bilby.gw import utils as gwutils
from starccato import generate_signals

np.random.seed(2)

DATA_COL = 'tab:gray'
SIGNAL_COL = 'tab:orange'
PSD_COL = 'black'

warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")

SAMPLING_FREQ = 4096
N_TIMESTAMPS = 256
DURATION = N_TIMESTAMPS / SAMPLING_FREQ


def __supernova(time_array, luminosity_distance, **kwargs):
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

    n = kwargs.get('n', 1)
    seed = kwargs.get('seed', 0)
    waveform = generate_signals(n=n, seed=seed)

    if n == 1:
        waveform = waveform[0]

    # waveforms generated at 10kpc, so scale to the luminosity distance
    scaling = 1e-21 * (10.0 / luminosity_distance)
    waveform = scaling * waveform
    return {'plus': waveform, 'cross': waveform}






def _get_waveform_generator():
    # Create the waveform_generator using a supernova source function
    waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
        duration=DURATION,
        sampling_frequency=SAMPLING_FREQ,
        time_domain_source_model=__supernova,
        parameter_conversion=lambda parameters: (parameters, list()),
        waveform_arguments=dict(seed=0),
    )
    return waveform_generator


WAVEFORM_GENERATOR = _get_waveform_generator()
