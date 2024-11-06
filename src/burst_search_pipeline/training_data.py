from dataclasses import dataclass
import numpy as np
from .lvk_interferometers import load_interferometers_with_injection

from enum import Enum

class BurstType(Enum):
    NOISE = 0
    GLITCH = 1
    SIGNAL = 2


@dataclass
class TrainingData:
    label: BurstType
    time_domain_strain: np.ndarray
    qgram: np.ndarray = None

    def generate(self, seed=0):
        np.random.seed(seed)
        IFO_data = load_interferometers_with_injection()

        return self
