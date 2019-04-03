from datetime import timedelta
from garminexport.garminclient import GarminClient
from garminexport.retryer import Retryer, ExponentialBackoffDelayStrategy, MaxRetriesStopStrategy


class ConnectClient:
    _active = False

    def __init__(self, username, password, initial_delay=timedelta(seconds=1), max_retries=3):
        self._client = GarminClient(username, password)
        self._retryer = Retryer(
            delay_strategy=ExponentialBackoffDelayStrategy(initial_delay=initial_delay),
            stop_strategy=MaxRetriesStopStrategy(max_retries))

    def __enter__(self):
        self._client.__enter__()
        self._active = True
        return self

    def __exit__(self, *args):
        self._active = False
        self._client.__exit__(*args)

    @property
    def activities(self):
        """
        return set of (activity_id:int, start_time:datetime) tuples
        """
        if not self._active:
            raise RuntimeError("Context manager not active")

        return {rv[0] for rv in self._retryer.call(self._client.list_activities)}

    def download_activity(self, activity_id):
        """
        returns fit data or None
        """
        if not self._active:
            raise RuntimeError("Context manager not active")

        return self._retryer.call(self._client.get_activity_fit, activity_id)
