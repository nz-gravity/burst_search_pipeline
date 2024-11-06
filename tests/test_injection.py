from burst_search_pipeline.lvk_interferometers import load_interferometers_with_injection
from burst_search_pipeline.plotting import plot_time_and_freq_domain
import numpy as np

def test_load_interferometers_with_injection(plt_dir):
    np.random.seed(1)
    injection_parameters = dict(
        luminosity_distance=2,  # kpc
        geocent_time=1126259642.413,
        ra=0,
        dec=0,
        psi=0
    )

    data = load_interferometers_with_injection(injection_parameters)
    plot_time_and_freq_domain(
        data.interferometers[0],
        data.time_domain_strain['plus'],
        data.frequency_domain_strain['plus']
    )[0].get_figure().savefig(f"{plt_dir}/supernova.png")


def __save_timeseries(ifo):
    strain = ifo.strain_data.time_domain_strain
    t0 = ifo.strain_data.start_time
    x = ifo.strain_data.time_array - t0
    strain = np.roll(strain, 55)
    # save txt with time, strain
    np.savetxt('time_domain_strain.txt', np.array([x, strain]).T)

