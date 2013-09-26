import numpy as np
from numpy.testing import assert_equal
from pylinkparse import Raw
from pylinkparse.constants import EDF

path = 'pylinkparse/tests/data/'
fname = path + 'test_raw.asc'


def test_raw_io():
    """Test essential basic IO functionality"""
    raw = Raw(fname)
    print raw  # test repr works

    # tests dtypes are parsed correctly that is double only
    dtypes = raw._samples.dtypes.unique()
    assert_equal(len(dtypes), 1)
    assert_equal(dtypes[0], np.float64)

    for actual, desired in zip(raw._saccades.dtypes, EDF.SAC_DTYPES.split()):
        assert_equal(actual, np.dtype(desired))

    for actual, desired in zip(raw._blinks.dtypes, EDF.BLINK_DTYPES.split()):
        assert_equal(actual, np.dtype(desired))

    for actual, desired in zip(raw._fixations.dtypes, EDF.FIX_DTYPES.split()):
        assert_equal(actual, np.dtype(desired))
    for attr in ['_samples', '_saccades', '_fixations', '_blinks']:
        key = 'time' if attr == '_samples' else ['stime', 'etime']
        assert_equal(getattr(raw, attr)[key][0], 0.0)


def tets_access_data():
    """Test slicing and indexing"""
    raw = Raw(fname)
    for idx in [1, [1, 3], slice(50)]:
        data, times = raw[idx]
        assert_equal(len(data), len(times))

    # test for monotonous continuity
    deltas = np.unique(np.diff(times))
    assert_equal(len(deltas), 1)
    assert_equal(deltas[0], 1.0)