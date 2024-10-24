"""
Example matched filter search using Starcatto
"""

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


def starccato_signal_generator(n: int, luminosity_distance, **kwargs):
    return


def supernova(time_array, luminosity_distance, **kwargs):
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


def plot_freq_domain(ifo: bilby.gw.detector.Interferometer, freq_signal, ax=None):
    if ax == None:
        fig, ax = plt.subplots()
    df = ifo.strain_data.frequency_array[1] - ifo.strain_data.frequency_array[0]
    asd = gwutils.asd_from_freq_series(
        freq_data=ifo.strain_data.frequency_domain_strain, df=df)

    ax.loglog(ifo.strain_data.frequency_array[ifo.strain_data.frequency_mask],
              asd[ifo.strain_data.frequency_mask],
              color=DATA_COL, label=f"{ifo.name} Data", alpha=0.5, lw=3)
    ax.loglog(ifo.strain_data.frequency_array[ifo.strain_data.frequency_mask],
              ifo.amplitude_spectral_density_array[ifo.strain_data.frequency_mask],
              color=PSD_COL, lw=1.0, label=ifo.name + ' ASD')

    signal_asd = gwutils.asd_from_freq_series(
        freq_data=freq_signal, df=df)

    ax.loglog(ifo.strain_data.frequency_array[ifo.strain_data.frequency_mask],
              signal_asd[ifo.strain_data.frequency_mask],
              color=SIGNAL_COL,
              label=f'Signal (SNR: {ifo.meta_data["optimal_SNR"]:.2f})', alpha=0.5)
    ax.grid(True)
    ax.set_ylabel(r'Strain [strain/$\sqrt{\rm Hz}$]')
    ax.set_xlabel(r'Frequency [Hz]')
    ax.legend(loc='best')


def plot_time_domain(ifo, time_signal, ax=None):
    if ax == None:
        fig, ax = plt.subplots()
    strain = ifo.strain_data.time_domain_strain
    t0 = ifo.strain_data.start_time
    x = ifo.strain_data.time_array - t0
    xlabel = f'GPS time [s] - {t0}'
    # unroll raw data
    strain = np.roll(strain, 55)
    ax.plot(x, strain, color=DATA_COL, label=f"{ifo.name} Data", alpha=0.5, lw=3)
    ax.plot(x, time_signal, color=SIGNAL_COL, label=f'Signal', alpha=0.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Strain')
    ax.legend()


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


sampling_frequency = 4096
n_timestamps = 256
duration = n_timestamps / sampling_frequency
time = np.linspace(0, duration, n_timestamps)

# Specify the output directory and the name of the simulation.
outdir = "outdir"
label = "supernova"
bilby.core.utils.setup_logger(outdir=outdir, label=label)

# We are going to inject a supernova waveform.  We first establish a dictionary
# of parameters that includes all of the different waveform parameters. It will
# read in a signal to inject from a txt file.

injection_parameters = dict(
    luminosity_distance=1,  # kpc
    geocent_time=1126259642.413,
    ra=0,
    dec=0,
    psi=0,
    seed=0
)

# Create the waveform_generator using a supernova source function
waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
    duration=duration,
    sampling_frequency=sampling_frequency,
    time_domain_source_model=supernova,
    parameters=injection_parameters,
    parameter_conversion=lambda parameters: (parameters, list()),
    waveform_arguments=dict(seed=0),
)

# Set up interferometers (LIGO-Hanford (H1) and LIGO-Livingston (L1))
ifos = bilby.gw.detector.InterferometerList(["H1", "L1"])
ifos.set_strain_data_from_power_spectral_densities(
    sampling_frequency=sampling_frequency,
    duration=duration,
    start_time=injection_parameters["geocent_time"],
)

injection_strain_time = waveform_generator.time_domain_strain(injection_parameters)
injection_strain = waveform_generator.frequency_domain_strain(injection_parameters)

ifos.inject_signal(
    parameters=injection_parameters,
    raise_error=False,
    injection_polarizations=injection_strain
)

snr_kwgs = dict(
    data=ifos[0].frequency_domain_strain,
    psd=ifos[0].power_spectral_density_array,
    freq=ifos[0].frequency_array,
    fmask=ifos[0].strain_data.frequency_mask
)

best_snr = compute_snr(signal=injection_strain['plus'], **snr_kwgs)

fig, axes = plt.subplots(2, 1, figsize=(5, 8))
plot_freq_domain(ifos[0], injection_strain['plus'], axes[0])
plot_time_domain(ifos[0], injection_strain_time['plus'], axes[1])
plt.suptitle(f"Matched-filter SNR {best_snr[0]:.2f}, Optimal SNR {best_snr[1]:.2f}")
plt.tight_layout()
plt.savefig('supernova.png')


signals = supernova(None, 10, n=100)
snrs = [
    compute_snr(s, **snr_kwgs) for s in signals['plus']
]



