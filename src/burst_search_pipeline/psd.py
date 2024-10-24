import os

import numpy as np
from scipy.interpolate import interp1d
from bilby.core import utils
import matplotlib.pyplot as plt
from sympy.abc import alpha

HERE = os.path.dirname(os.path.abspath(__file__))

ALIGO_O4_FN = f"{HERE}/data/aLIGO_O4_high_asd.txt"

class LIGO_PSD(object):

    def __init__(self):

        self.frequency_array, self.psd_array = np.genfromtxt(ALIGO_O4_FN).T
        # self.psd_array = self.asd_array ** 0.5
        self.power_spectral_density_interpolated = interp1d(self.frequency_array,
                                                              self.psd_array,
                                                              bounds_error=False,
                                                              fill_value=np.inf)


    def get_noise_realisation(self, sampling_frequency, duration):
        """
        Generate frequency Gaussian noise scaled to the power spectral density.

        Parameters
        ==========
        sampling_frequency: float
            sampling frequency of noise
        duration: float
            duration of noise

        Returns
        =======
        array_like: frequency domain strain of this noise realisation
        array_like: frequencies related to the frequency domain strain
        """
        white_noise, frequencies = utils.create_white_noise(sampling_frequency, duration)
        with np.errstate(invalid="ignore"):
            frequency_domain_strain = self.power_spectral_density_interpolated(frequencies) ** 0.5 * white_noise
        out_of_bounds = (frequencies < min(self.frequency_array)) | (frequencies > max(self.frequency_array))
        frequency_domain_strain[out_of_bounds] = 0 * (1 + 1j)
        return frequency_domain_strain, frequencies


    def plot(self, noise_instance=False):
        fig = plt.figure()
        plt.loglog(self.frequency_array, self.psd_array)
        if noise_instance:
            noise, freq = self.get_noise_realisation(1024, 4)
            plt.loglog(freq, noise, alpha=0.1, zorder=-1)
        plt.xlabel("Freq [Hz]")
        plt.ylabel("Strain [sqrt Hz]")
        return fig



def create_white_noise(sampling_frequency, duration):
    """ Create white_noise which is then coloured by a given PSD

    Parameters
    ==========
    sampling_frequency: float
    duration: float
        duration of the data

    Returns
    =======
    array_like: white noise
    array_like: frequency array
    """

    number_of_samples = duration * sampling_frequency
    number_of_samples = int(np.round(number_of_samples))

    frequencies = create_frequency_series(sampling_frequency, duration)

    norm1 = 0.5 * duration**0.5
    re1, im1 = np.random.normal(0, norm1, (2, len(frequencies)))
    white_noise = re1 + 1j * im1

    # set DC and Nyquist = 0
    white_noise[0] = 0
    # no Nyquist frequency when N=odd
    if np.mod(number_of_samples, 2) == 0:
        white_noise[-1] = 0

    # python: transpose for use with infft
    white_noise = np.transpose(white_noise)
    frequencies = np.transpose(frequencies)

    return white_noise, frequencies

def create_frequency_series(sampling_frequency, duration):
    """ Create a frequency series with the correct length and spacing.

    Parameters
    ==========
    sampling_frequency: float
    duration: float

    Returns
    =======
    array_like: frequency series

    """
    num = sampling_frequency * duration
    if np.abs(num - np.round(num)) > 10**(-14):
        raise ValueError(
            '\nYour sampling frequency and duration must multiply to a number'
            'up to (tol = {}) decimals close to an integer number. '
            '\nBut sampling_frequency={} and  duration={} multiply to {}'.format(
                14, sampling_frequency, duration,
                sampling_frequency * duration
            )
        )
    number_of_samples = int(np.round(duration * sampling_frequency))
    number_of_frequencies = int(np.round(number_of_samples / 2) + 1)

    return np.linspace(start=0,
                       stop=sampling_frequency / 2,
                       num=number_of_frequencies)






if __name__ == '__main__':
    psd = LIGO_PSD()
    psd.plot(True).show()
