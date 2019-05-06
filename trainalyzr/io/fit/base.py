from datetime import timezone
import fitdecode
from geopandas import GeoDataFrame
from shapely.geometry import Point


SEMICIRLE_TO_DEGREE = 180 / pow(2, 31)


def default_getter(frame, field):
    try:
        source_field = field.get('source_field', field['name'])
        return frame.get_field(source_field).value
    except KeyError:
        return None


def get_position(frame, _):
    try:
        longitude = frame.get_field('position_long').value
        latitude = frame.get_field('position_lat').value
        if longitude is None or latitude is None:
            raise KeyError

        return Point(
            SEMICIRLE_TO_DEGREE * longitude,
            SEMICIRLE_TO_DEGREE * latitude,
        )
    except KeyError:
        return None


RECORD_FIELDS = [{
    "name": "timestamp",
}, {
    "name": "position",
    "getter": get_position,
}, {
    "name": "distance",
}, {
    "name": "speed",
    "source_field": "enhanced_speed",
}, {
    "name": "altitude",
    "source_field": "enhanced_altitude",
}, {
    "name": "heart_rate",
}, {
    "name": "power",
    "source_field": "Power",
}]


class FitReader():
    def __init__(self, fit_fileish):
        with fitdecode.FitReader(fit_fileish) as fit:
            self._fit_frames = list([frame for frame in fit])

    @property
    def dataframe(self):
        if not hasattr(self, "_dataframe"):
            dataframe = self._load_fit_frames()
            self._extend_dataframe(dataframe)
            self._dataframe = dataframe
        return self._dataframe

    @property
    def activity(self):
        return next(self._get_data_frame_field('sport', 'sport'))

    @property
    def timezone_offset(self):
        if not hasattr(self, "_timezone_offset_cache"):
            local_time = next(self._get_data_frame_field('activity', 'local_timestamp'))
            utc_time = next(self._get_data_frame_field('activity', 'timestamp'))
            self._timezone_offset_cache = local_time.replace(tzinfo=timezone.utc) - utc_time
        return self._timezone_offset_cache

    def _load_fit_frames(self):
        data = {field['name']: [] for field in RECORD_FIELDS}
        for frame in self._get_data_frames('record'):
            for field in RECORD_FIELDS:
                getter = field.get('getter', default_getter)
                data[field['name']].append(getter(frame, field))

        dataframe = GeoDataFrame.from_dict(data)
        return dataframe

    def _extend_dataframe(self, dataframe):
        dataframe['duration'] = [(t - dataframe['timestamp'][0]).total_seconds() for t in dataframe['timestamp']]

    def _get_data_frames(self, name):
        return filter(
            lambda frame: frame.name == name,
            filter(
                lambda frame: isinstance(frame, fitdecode.records.FitDataMessage),
                self._fit_frames)
        )

    def _get_data_frame_field(self, frame_name, field_name):
        return map(
            lambda frame: frame.get_field(field_name).value,
            self._get_data_frames(frame_name)
        )
