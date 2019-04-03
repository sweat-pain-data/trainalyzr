import sys
import click
from trainalyzr.io.storage import FitStorage
from trainalyzr.io.connect import ConnectClient


@click.group()
def ingest():
    pass


@ingest.command()
@click.option("--account", required=True, prompt=True, envvar="TRAINALYZR_GARMIN_ACCOUNT",
              help="Read from TRAINALYZR_GARMIN_ACCOUNT")
@click.option("--password", required=True, prompt=True, hide_input=True, confirmation_prompt=True,
              envvar="TRAINALYZR_GARMIN_PASSWORD", help="Read from TRAINALYZR_GARMIN_PASSWORD")
@click.option("--raw-fs-dsn", required=True, envvar="TRAINALYZR_RAW_FS_DSN", help="Read from TRAINALYZR_RAW_FS_DSN")
@click.option("--max-retries", type=int, default=3, envvar="TRAINALYZR_MAX_RETRIES",
              help="Read from TRAINALYZR_MAX_RETRIES")
def pull(account, password, raw_fs_dsn, max_retries):
    """
    Will pull activities from Garmin Connect.

    Activities which are either locally available or marked as missing are skipped.

    Exit codes:

    0: All good.
    128: Downloaded with some marked as missing
    """
    storage = FitStorage(raw_fs_dsn)
    with ConnectClient(account, password, max_retries=max_retries) as client:
        local_activities = storage.activities
        remote_activities = client.activities
        missed_activities = 0
        synced_activities = 0

        with click.progressbar(remote_activities) as activity_ids:
            for activity_id in activity_ids:
                if activity_id in local_activities:
                    continue
                fit_data = client.download_activity(activity_id)
                if fit_data is not None:
                    storage.save(activity_id, fit_data)
                    synced_activities += 1
                else:
                    storage.add_missing(activity_id)
                    missed_activities += 1

    size = len(str(len(remote_activities)))
    click.echo(
        click.style(("remote activities:  {:" + str(size) + "d}").format(len(remote_activities)), fg="green"))
    click.echo(
        click.style(("synced activities:  {:" + str(size) + "d}").format(synced_activities), fg="bright_blue"))
    click.echo(
        click.style(("missed activities:  {:" + str(size) + "d}").format(missed_activities), fg="red"))
    click.echo(
        click.style(("local activities:   {:" + str(size) + "d}").format(len(storage.stored_activities)), fg="green"))
    click.echo(
        click.style(("missing activities: {:" + str(size) + "d}").format(len(storage.missing_activities)), fg="red"))

    storage.close()

    if missed_activities > 0:
        sys.exit(128)
