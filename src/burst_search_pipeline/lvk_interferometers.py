import bilby
from bilby.gw.detector import InterferometerList
from .waveform_generator import WAVEFORM_GENERATOR
from typing import Dict
from dataclasses import dataclass

DEFAULT_INJECTION= dict(

)

@dataclass
class IFODataStream:
    interferometers: InterferometerList
    time_domain_strain: Dict[str, float]
    frequency_domain_strain: Dict[str, float]

def load_interferometers(t0=0) -> InterferometerList:
    """Returns up interferometer objects (LIGO-Hanford (H1) and LIGO-Livingston (L1))"""
    ifos = InterferometerList(["H1", "L1"])
    ifos.set_strain_data_from_power_spectral_densities(
        sampling_frequency=WAVEFORM_GENERATOR.sampling_frequency,
        duration=WAVEFORM_GENERATOR.duration,
        start_time=t0
    )
    return ifos


def load_interferometers_with_injection(
        injection_parameters: Dict[str, float] = None
) -> IFODataStream:
    injection_strain_time = WAVEFORM_GENERATOR.time_domain_strain(injection_parameters)
    injection_strain = WAVEFORM_GENERATOR.frequency_domain_strain(injection_parameters)
    ifos = load_interferometers(t0=injection_parameters['geocent_time'])
    ifos.inject_signal(
        parameters=injection_parameters,
        raise_error=False,
        injection_polarizations=injection_strain
    )
    return IFODataStream(ifos, injection_strain_time, injection_strain)
