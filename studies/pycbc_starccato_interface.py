import numpy
import matplotlib.pyplot as pp
import pycbc.waveform
from pycbc.types import TimeSeries
from starccato import generate_signals
import numpy as np

SAMPLING_FREQ = 4096
N_TIMESTAMPS = 256
DURATION = N_TIMESTAMPS / SAMPLING_FREQ
DT = 1.0 / SAMPLING_FREQ


def supernova_waveform(**args):
    flow = args['f_lower'] # Required parameter
    dt = args.get('dt', DT)   # Required parameter
    luminosity_distance = args.get('luminosity_distance', 10)# Required parameter
    seed = args.get('seed',0) # A new parameter for my model

    waveform = generate_signals(n=1, seed=seed)[0]
    scaling = 1e-21 * (10.0 / luminosity_distance)
    waveform = scaling * waveform
    offset = 55 * dt
    waveform = TimeSeries(waveform, delta_t=dt, epoch=-offset)

    return waveform.real(), waveform.imag()



pycbc.waveform.add_custom_waveform('gan_supernova', supernova_waveform, 'time', force=True)

# Let's plot what our new waveform looks like
hp, hc = pycbc.waveform.get_td_waveform(approximant="gan_supernova",
                                        f_lower=0, seed=0,
                                        delta_t=1.0/4096)
pp.figure(0)
pp.plot(hp.sample_times, hp)
pp.xlabel('Time (s)')
pp.savefig('supernova_waveform.png')

pp.figure(1)
hf = hp.to_frequencyseries()
pp.plot(hf.sample_frequencies, hf.real())
pp.xlabel('Frequency (Hz)')
pp.xscale('log')
pp.xlim(0, 2000)
pp.savefig('supernova_waveform_frequency.png')

from pycbc.filter.qtransform import qtiling, qplane
from scipy.interpolate import RectBivariateSpline as interp2d


def qtransform(ts:TimeSeries, delta_t=None, delta_f=None, logfsteps=None,
               frange=None, qrange=(4, 64), mismatch=0.2, return_complex=False):

    if frange is None:
        frange = (30, int(ts.sample_rate / 2 * 8))

    q_base = qtiling(ts, qrange, frange, mismatch)
    _, times, freqs, q_plane = qplane(q_base, ts.to_frequencyseries(),
                                      return_complex=return_complex)

    # check freq is strictly increasing
    if not np.all(np.diff(freqs) > 0):
        raise ValueError(f"Frequency series is not strictly increasing: {freqs}")

    if logfsteps and delta_f:
        raise ValueError("Provide only one (or none) of delta_f and logfsteps")

    # Interpolate if requested
    if delta_f or delta_t or logfsteps:
            interp = interp2d(freqs, times, q_plane, kx=1, ky=1)

    if delta_t:
        times = np.arange(float(ts.start_time),
                              float(ts.end_time), delta_t)
    if delta_f:
        freqs = np.arange(int(frange[0]), int(frange[1]), delta_f)
    if logfsteps:
        freqs = np.logspace(np.log10(frange[0]),
                                np.log10(frange[1]),
                                logfsteps)

    if delta_f or delta_t or logfsteps:
            q_plane = interp(freqs, times)

    return times, freqs, q_plane


times, freqs, power = qtransform(hp, logfsteps=256,
                                       frange=(10.0, 2048.0),
                                    return_complex=True
                                    )
pp.pcolormesh(times, freqs, power ** 0.5, vmax=5)
