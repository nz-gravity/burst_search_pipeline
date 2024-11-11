from gwpy.timeseries import TimeSeries
from scipy.signal import spectrogram
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np


SAMPLING_FREQ = 4096


def test_qtransform(plt_dir, test_timeseries):
    # q_transform(
    #     time_data=test_timeseries.data,
    #     time_array=test_timeseries.time_array,
    # )
    # plt.savefig(f"{plt_dir}/qtransform.png")

    # interpolate the data

    interp = interp1d(
        x=test_timeseries.time_array,
        y=test_timeseries.data,
        kind='cubic'
    )
    new_fs = SAMPLING_FREQ * 2

    # increase FS from 4096 to 8192
    new_times = np.linspace(
        test_timeseries.time_array[0],
        test_timeseries.time_array[-1],
        new_fs
    )
    new_data = interp(new_times)

    # plot old and nnew
    plt.plot(test_timeseries.time_array, test_timeseries.data)
    plt.plot(new_times, new_data)
    plt.savefig(f"{plt_dir}/interpolated.png")

    # scipy.signal.spectrogram
    f, t, Sxx = spectrogram(
        new_data,
        fs=new_fs,
        nperseg=256,
        noverlap=128,
        nfft=256,
        scaling='spectrum',
        mode='magnitude',
    )
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.yscale('log')
    plt.ylim([20, 512])
    plt.colorbar(label='Energy')
    plt.savefig(f"{plt_dir}/spectrogram.png")


    gwpy_timeseries = TimeSeries(
        new_data,
        times=new_times,
    )

    qspecgram = gwpy_timeseries.q_transform(
        whiten=False,
        frange=(10, 512),
        qrange=(4, 64),
    )
    plot = qspecgram.plot(figsize=[8, 4], )




from burst_search_pipeline.lvk_interferometers import load_interferometers_with_injection
from burst_search_pipeline.plotting import plot_time_domain
import numpy as np

def test_frm_scratch(plt_dir):
    np.random.seed(1)
    injection_parameters = dict(
        luminosity_distance=2,  # kpc
        geocent_time=1126259642.413,
        ra=0,
        dec=0,
        psi=0
    )

    data = load_interferometers_with_injection(injection_parameters)

    y = data.interferometers[0].strain_data.time_domain_strain
    t0 = data.interferometers[0].strain_data.start_time
    x = data.interferometers[0].strain_data.time_array - t0
    y = np.roll(y, 55)

    interp = interp1d(x=x, y=y,kind='cubic')
    new_fs = SAMPLING_FREQ * 2
    # increase FS from 4096 to 8192
    xinterp = np.linspace(x[0],x[-1],new_fs)
    yinterp = interp(xinterp)

    specf, spect, Sxx = spectrogram(
        yinterp,
        fs=new_fs,
        # nperseg=128,
        # noverlap=64,
        # nfft=256,
        scaling='spectrum',
        mode='magnitude',
    )
    gwpy_timeseries = TimeSeries(yinterp, times=xinterp,)

    qspecgram = gwpy_timeseries.q_transform(
        whiten=False,
        frange=(10, 512),
        qrange=(4, 64),
    )

    fig, axes = plt.subplots(3, 1, figsize=(8, 6), sharex=True)

    plot_time_domain(
        data.interferometers[0],
        data.time_domain_strain['plus'],
        axes[0],
    )
    axes[1].pcolormesh(spect, specf, Sxx)
    axes[1].set_yscale('log')
    axes[1].ylim([20, 512])
    axes[2].plot(qspecgram)
    plt.subplots_adjust(hspace=0.)
    plt.savefig(f"{plt_dir}/spectogram_compare.png")