from datetime import date, datetime
import signal

from moonsense import Platform
from moonsense.client import Client

MISSING_GROUP_ID = "missing-group-id"
GRACE_PERIOD = 2
KILL_PERIOD = 30

moonsense_client = Client()


def handler(signalname):
    def wrapper_handler(signal_received, frame):
        raise KeyboardInterrupt(f"{signalname} received")
    return wrapper_handler

def run_download(
    output: str,
    until: datetime,
    since: datetime,
    labels: list[str],
    platforms: list[str],
    with_group_id: bool = False) -> None:
    """
    Download all sessions from a project based on the provided filters.

    :param output: Path to the output directory - either absolut or relative to the current
                    directory.
    :param until: Date in the YYYY-MM-DD format until the session data should be included.
                If not provided, the current day is used.
    :param since: Date in the YYYY-MM-DD format since the session data should be included.
                If not provided beginning of Moonsense time - 1st of January 2021 is used.
    :param labels: A list of labels to filter sessions by. A session needs to include at least
                one label in this list to be downloaded.
    :param platform: Filter downloaded sessions by the platforms they were produced:
                        web, ios, android or None for all.
    :param with_group_id: If set to True, organizes the downloaded sessions by date and
                        client session group id. Default: False.
    """
    signal.signal(signal.SIGINT, handler("SIGINT"))
    signal.signal(signal.SIGTERM, handler("SIGTERM"))

    filter_by_since = datetime
    if since is not None:
        filter_by_since = datetime.strptime(since, "%Y-%m-%d").date()
    else:
        # beginning of Moonsense time is 1st of January 2021.
        filter_by_since = datetime.strptime("2021-01-01", "%Y-%m-%d").date()

    if until is not None:
        filter_by_until = datetime.strptime(until, "%Y-%m-%d").date()
    else:
        filter_by_until = date.today()
    
    filter_by_platforms = None
    if platforms is not None:
        filter_by_platforms = []
        for p in platforms:
            filter_by_platforms.append(Platform.from_str(p))

    print("Downloading sessions in between", filter_by_since, filter_by_until)

    moonsense_client.download_all_sessions(
        output,
        filter_by_until,
        filter_by_since,
        labels,
        filter_by_platforms,
        with_group_id)
