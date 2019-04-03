import os.path
from fs import open_fs
from fs.errors import ResourceNotFound


def _filename_from_id(activity_id):
    return "{0}.fit".format(activity_id)


def _id_from_filename(filename):
    return int(os.path.basename(os.path.splitext(filename)[0]))


class FitStorage:
    MISSING_FILE = ".missing"

    def __init__(self, storage_dsn):
        self._fs = open_fs(storage_dsn)

    def close(self):
        self._fs.close()

    @property
    def activities(self):
        return self.stored_activities.union(self.missing_activities)

    @property
    def stored_activities(self):
        return {_id_from_filename(match.path) for match in self._fs.glob("*.fit")}

    @property
    def missing_activities(self):
        try:
            with self._fs.open(self.MISSING_FILE) as missing_file:
                return set(missing_file.readlines())
        except ResourceNotFound:
            return set()

    def save(self, activity_id, fit_data):
        filename = _filename_from_id(activity_id)
        self._fs.writebytes(filename, fit_data)

    def add_missing(self, activity_id):
        self._fs.appendtext(self.MISSING_FILE, "{0}\n".format(activity_id))
