from datetime import date, datetime
import signal

from moonsense import Platform
from moonsense.client import Client

MISSING_JOURNEY_ID = "missing-journey-id"
GRACE_PERIOD = 2
KILL_PERIOD = 30

moonsense_client = Client(tries=5)


def run_download(
    output: str,
    until: datetime,
    since: datetime,
    skip_days: list[str],
    incremental: bool,
    labels: list[str],
    platforms: list[str],
    with_journey_id: bool = False) -> None:
    """
    Download all sessions from a project based on the provided filters.

    :param output: Path to the output directory - either absolut or relative to the current
                    directory.
    :param until: Date in the YYYY-MM-DD format until the session data should be included.
                If not provided, the current day is used.
    :param since: Date in the YYYY-MM-DD format since the session data should be included.
                If not provided beginning of Moonsense time - 1st of January 2021 is used.
    :param skip_days: A list of days in the YYYY-MM-DD format that should be skipped.
    :param incremental: If set to True, only downloads sessions that are not already downloaded.
    :param labels: A list of labels to filter sessions by. A session needs to include at least
                one label in this list to be downloaded.
    :param platform: Filter downloaded sessions by the platforms they were produced:
                        web, ios, android or None for all.
    :param with_journey_id: If set to True, organizes the downloaded sessions by date and
                        journey id. Default: False.
    """

    filter_by_since = datetime
    if since is not None:
        filter_by_since = datetime.strptime(since, "%Y-%m-%d").date()
    else:
        # beginning of Moonsense time is 1st of January 2021.
        filter_by_since = datetime.strptime("2021-01-01", "%Y-%m-%d").date()

    if until is not None:
        filter_by_until = datetime.strptime(until, "%Y-%m-%d").date()
    else:
        filter_by_until = datetime.utcnow().date()

    filter_by_platforms = None
    if platforms is not None:
        filter_by_platforms = []
        for p in platforms:
            filter_by_platforms.append(Platform.from_str(p))
    
    filter_by_skip_days = []
    if skip_days is not None:
        for day in skip_days:
            parsed_day_to_skip = datetime.strptime(day, "%Y-%m-%d").date()
            filter_by_skip_days.append(parsed_day_to_skip)

    moonsense_client.download_all_sessions(
        output,
        filter_by_until,
        filter_by_since,
        filter_by_skip_days,
        incremental,
        labels,
        filter_by_platforms,
        with_journey_id)
