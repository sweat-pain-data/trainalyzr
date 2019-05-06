from datetime import timezone
from math import ceil
from trainalyzr import math


class L0Metadata():
    def __init__(self, activity, distance, duration,  start_time):
        self.activity = activity
        self.distance = distance
        self.duration = duration
        self.start_time = start_time


class L0Statistics():
    def __init__(self,
                 heart_rate_average,
                 heart_rate_max,
                 power_average,
                 power_variance,
                 speed_average,
                 speed_variance):
        self.heart_rate_average = heart_rate_average
        self.heart_rate_max = heart_rate_max
        self.power_average = power_average
        self.power_variance = power_variance
        self.speed_average = speed_average
        self.speed_variance = speed_variance


class L0():
    def __init__(self, dataframe, activity, timezone_offset):
        self.dataframe = dataframe
        self._activity = activity
        self._timezone_offset = timezone_offset

    @property
    def metadata(self):
        if not hasattr(self, "_metadata"):
            self._metadata = L0Metadata(
                self._activity,
                self._distance,
                self._duration,
                self._start_time,
            )
        return self._metadata

    @property
    def statistics(self):
        if not hasattr(self, "_statistics"):
            self._statistics = L0Statistics(
                math.average(self.dataframe['heart_rate']),
                math.max(self.dataframe['heart_rate']),
                math.average(self.dataframe['power']),
                math.variance(self.dataframe['power']),
                math.average(self.dataframe['speed']),
                math.variance(self.dataframe['speed']),
            )
        return self._statistics

    @property
    def _distance(self):
        return self.dataframe['distance'].iloc[-1]

    @property
    def _duration(self):
        return ceil((self.dataframe['timestamp'].iloc[-1] - self.dataframe['timestamp'][0]).total_seconds())

    @property
    def _start_time(self):
        return datetime_set_offset(self.dataframe['timestamp'][0].to_pydatetime(), self._timezone_offset)


def datetime_set_offset(datetime, offset):
    return datetime.replace(tzinfo=timezone(offset)) + offset
