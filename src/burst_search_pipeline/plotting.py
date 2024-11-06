import bilby
import matplotlib.pyplot as plt
import numpy as np
from bilby.gw import utils as gwutils
from gwpy.timeseries import TimeSeries

np.random.seed(2)

DATA_COL = 'tab:gray'
SIGNAL_COL = 'tab:orange'
PSD_COL = 'black'


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
              label=f'Signal', alpha=0.5)
    ax.grid(True)
    ax.set_ylabel(r'Strain [strain/$\sqrt{\rm Hz}$]')
    ax.set_xlabel(r'Frequency [Hz]')
    ax.legend(loc='best')
    return ax


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
    return ax


def plot_time_and_freq_domain(ifo, time_signal, freq_signal, axes=None):
    if axes == None:
        fig, axes = plt.subplots(2,1, figsize=(5,8))
    optimal_snr = ifo.meta_data['optimal_SNR']
    matched_filter_snr = np.abs(ifo.meta_data['matched_filter_SNR'])
    plot_freq_domain(ifo, freq_signal, axes[0])
    plot_time_domain(ifo, time_signal, axes[1])
    plt.suptitle(f"Matched-filter SNR {matched_filter_snr:.2f}, Optimal SNR {optimal_snr:.2f}")
    plt.tight_layout()
    return axes


def q_transform(time_data:np.ndarray, time_array:np.ndarray):
    t = TimeSeries(time_data, times=time_array)
    qtransform = t.q_transform()
    qtransform.plot()