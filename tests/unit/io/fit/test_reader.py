from datetime import timedelta
import pandas as pd
from pandas.api import types
import pytest
from trainalyzr.io.fit import FitReader


@pytest.fixture(scope="module")
def reader(golden_fit_file):
    return FitReader(golden_fit_file)


def test_reader_dataframe(reader):
    dataframe = reader.dataframe
    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape == (1603, 8)
    dtypes = dataframe.dtypes
    names = list(dataframe)

    assert names[0] == "timestamp"
    assert types.is_datetime64tz_dtype(dtypes[0])
    assert names[1] == "position"
    assert types.is_object_dtype(dtypes[1])  # is GeoSeries?!?
    assert names[2] == "distance"
    assert types.is_float_dtype(dtypes[2])
    assert names[3] == "speed"
    assert types.is_float_dtype(dtypes[3])
    assert names[4] == "altitude"
    assert types.is_float_dtype(dtypes[4])
    assert names[5] == "heart_rate"
    assert types.is_float_dtype(dtypes[5])
    assert names[6] == "power"
    assert types.is_unsigned_integer_dtype(dtypes[6])


def test_reader_activity(reader):
    assert reader.activity == "running"


def test_reader_timezone_offset(reader):
    assert reader.timezone_offset == timedelta(seconds=3600)
