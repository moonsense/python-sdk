import os
from time import time, sleep
import signal
from functools import partial

from datetime import date, datetime
from multiprocessing import Process, JoinableQueue, Event
from queue import Empty

from google.protobuf.json_format import MessageToJson
from retry import retry

from moonsense.client import Client

MISSING_GROUP_ID = "missing-group-id"
GRACE_PERIOD = 2
KILL_PERIOD = 30


moonsense_client = Client()

@retry(Exception, tries=3, delay=0)
def download_data_into_folder(datadir, with_group_id, session_id):
    session = None
    try:
        session = moonsense_client.describe_session(session_id)
    except Exception as e:
        print("Error encountered while describing session", e)
        raise e
    group_id = session.client_session_group_id
    if group_id is None or len(group_id) == 0:
        group_id = MISSING_GROUP_ID
    
    session_as_json = MessageToJson(session)

    created_at = datetime.fromtimestamp(session.created_at.seconds).date()
    formatted_created_at = created_at.strftime("%Y-%m-%d")

    session_dir_path = os.path.join(datadir, formatted_created_at, session.session_id)
    if with_group_id:
        session_dir_path = os.path.join(datadir,
            created_at.strftime("%Y-%m-%d"),
            group_id,
            session.session_id)

    metadata_path = os.path.join(session_dir_path, "metadata.json")
    with open(metadata_path, "w") as metadata_file:
      metadata_file.write(session_as_json)

    raw_sealed_bundles_path = os.path.join(session_dir_path, "raw_sealed_bundles.json")
    pcap_path = os.path.join(session_dir_path, "packets.pcap")

    try:
        print(f"Downloading session {session_id} from {formatted_created_at}")
        moonsense_client.download_session(session_id, raw_sealed_bundles_path)
        if 'packet' in session.counters:
            moonsense_client.download_pcap_data(session_id, pcap_path)
    except Exception as e:
        print("Error encountered while downloading session", e)
        raise e


def download_session(queue, stop_event, with_group_id):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    localdir = os.getcwd()
    datadir = os.path.join(localdir, "data")

    while True:
        if stop_event.is_set():
            break

        try:
            msg = queue.get(timeout=.01)
        except Empty:
            # Run next iteration of loop
            continue

        if msg is None:
            queue.task_done()

        try:
            session_id = msg
            download_data_into_folder(datadir, with_group_id, session_id)
        finally:
            queue.task_done()


def fetch_group_id(session):
    return session.client_session_group_id


def handler(signalname):
    def wrapper_handler(signal_received, frame):
        raise KeyboardInterrupt(f"{signalname} received")
    return wrapper_handler

def run_download(until: str, since: str, labels: list[str], with_group_id: bool = False):
    """
    Download sessions from a project.

    :param until: Date in the YYYY-MM-DD format until the session data should be included.
                  If not provided, the current day is used.
    :param since: Date in the YYYY-MM-DD format since the session data should be included.
                  If not provided beginning of Moonsense time - 1st of January 2021 is used.
    :param labels: A list of labels to filter sessions by. A session needs to include at least
                   one label in this list to be downloaded.
    :param with_group_id: If set to True, organizes the downloaded sessions by date and
                          client session group id. Default: False.
    """
    signal.signal(signal.SIGINT, handler("SIGINT"))
    signal.signal(signal.SIGTERM, handler("SIGTERM"))

    localdir = os.getcwd()
    datadir = os.path.join(localdir, "data")
    os.makedirs(datadir, exist_ok=True)

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

    queue = JoinableQueue()
    stop_event = Event()
    number_of_processes = os.cpu_count() * 2

    all_procs = []
    for process_count in range(number_of_processes):
        local_process = Process(target=download_session,
            daemon=True,
            args=((queue, stop_event, with_group_id)))
        all_procs.append(local_process)
        local_process.start()

    print("Downloading sessions in between", filter_by_since, filter_by_until)

    session_counter = 0
    filter_by_labels = labels if len(labels) > 0 else None

    try:
        # listing is in reverse chronological order - newest are first. 
        for session in moonsense_client.list_sessions(filter_by_labels):        
                group_id = session.client_session_group_id
                if group_id is None or len(group_id) == 0:
                    group_id = MISSING_GROUP_ID

                created_at = datetime.fromtimestamp(session.created_at.seconds).date()

                if created_at > filter_by_until:
                    continue

                if created_at < filter_by_since:
                    print("Processed sessions", session_counter)
                    print("Hit session that is newer than the since filter.")
                    break

                session_dir_path = os.path.join(datadir, created_at.strftime("%Y-%m-%d"), session.session_id)
                if with_group_id:
                    session_dir_path = os.path.join(datadir,
                        created_at.strftime("%Y-%m-%d"),
                        group_id,
                        session.session_id)

                if not os.path.isdir(session_dir_path):
                    os.makedirs(session_dir_path)

                session_counter += 1
                queue.put(session.session_id)
        
        for local_process in all_procs:
            queue.put(None)
        
        queue.join()
    except KeyboardInterrupt:
        stop_event.set()
        t = time()
        while alive_procs := [p for p in all_procs if p.is_alive()]:
            if time() > t + GRACE_PERIOD:
                for p in alive_procs:
                    os.kill(p.pid, signal.SIGINT)
            elif time() > t + KILL_PERIOD:
                for p in alive_procs:
                    p.kill()
            sleep(.01)