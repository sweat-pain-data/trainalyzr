from datetime import datetime, timedelta, timezone
import pytest
from trainalyzr.io.fit import FitReader
from trainalyzr.models import L0


@pytest.fixture(scope="module")
def model(golden_fit_file):
    reader = FitReader(golden_fit_file)
    return L0(reader.dataframe, reader.activity, reader.timezone_offset)


def test_l0_metadata(model):
    assert model.metadata.activity == "running"
    assert model.metadata.distance == 4872.56
    assert model.metadata.duration == 26 * 60 + 42
    assert model.metadata.start_time == datetime(2019, 3, 2, 9, 3, 25, 0, timezone(offset=timedelta(seconds=3600)))


def test_l0_statistics(model):
    assert model.statistics.heart_rate_average == 147.0519230769231
    assert model.statistics.heart_rate_max == 170
    assert model.statistics.power_average == 225.35433562071117
    assert model.statistics.power_variance == 0.1579386585848519
    assert model.statistics.speed_average == 2.986842170929507
    assert model.statistics.speed_variance == 0.0890258966814594
