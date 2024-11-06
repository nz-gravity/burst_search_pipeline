import os
import pytest
import numpy as np
from collections import namedtuple

TIMESERIES = namedtuple('TIMESERIES', ['data', 'time_array'])

__HERE__ = os.path.dirname(os.path.abspath(__file__))



@pytest.fixture
def plt_dir():
    d = os.path.join(__HERE__, 'out_plots')
    os.makedirs(d, exist_ok=True)
    return d

@pytest.fixture
def test_timeseries()->TIMESERIES:
    data = np.loadtxt(os.path.join(__HERE__, 'test_data/time_domain_strain.txt'))
    return TIMESERIES(data=data[:, 1], time_array=data[:, 0])