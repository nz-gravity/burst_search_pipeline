from gwpy.timeseries import TimeSeries
# import numpy as np
# from burst_search_pipeline.plotting import q_transform
# import matplotlib.pyplot as plt


def test_qtransform(plt_dir, test_timeseries):
    # q_transform(
    #     time_data=test_timeseries.data,
    #     time_array=test_timeseries.time_array,
    # )
    # plt.savefig(f"{plt_dir}/qtransform.png")
    gwpy_timeseries = TimeSeries(test_timeseries.data, times=test_timeseries.time_array)
    qspecgram = gwpy_timeseries.q_transform(
        whiten=False
    )
    plot = qspecgram.plot(figsize=[8, 4])
    ax = plot.gca()
    ax.set_xscale('seconds')
    ax.set_yscale('log')
    ax.set_ylabel('Frequency [Hz]')
    ax.grid(True, axis='y', which='both')
    ax.colorbar(cmap='viridis', label='Normalized energy')
    plot.savefig(f"{plt_dir}/qtransform.png")

