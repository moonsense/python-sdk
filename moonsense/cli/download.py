from multiprocessing import Process, Queue
from google.protobuf.json_format import MessageToJson
from retry import retry

from moonsense.client import Client

def run_download(filter_by, until, since,label):
    localdir = os.path.dirname(__file__)
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

    queue = Queue()
    number_of_processes = os.cpu_count() * 2

    valid_group_id = {}
    if filter_by:
        with open(filter_by, newline='') as csvfile:
            filter_by_rows = csv.DictReader(csvfile)
            for row in filter_by_rows:
                valid_group_id[row["group_id"]] = True

    all_procs = []
    for process_count in range(number_of_processes):
        local_process = Process(target=download_session, args=((queue),))
        local_process.start()

        all_procs.append(local_process)

    print("Downloading sessions in between", filter_by_since, filter_by_until)

    session_counter = 0
    labels = label if len(label) > 0 else None

    # listing is in reverse chronological order - newest are first.
    for session in moonsense_client.list_sessions(labels):
        group_id = session.client_session_group_id
        if group_id is None:
            continue

        created_at = datetime.fromtimestamp(session.created_at.seconds).date()

        if created_at > filter_by_until:
            continue

        if created_at < filter_by_since:
            print("Processed sessions", session_counter)
            print("Hit session that is newer than the since filter.")
            break

        if filter_by:
            if group_id not in valid_group_id:
                continue

        session_dir_path = os.path.join(datadir, created_at.strftime("%Y-%m-%d"), group_id, session.session_id)
        if not os.path.isdir(session_dir_path):
            os.makedirs(session_dir_path)

        session_counter += 1
        queue.put(session.session_id)

    for local_process in all_procs:
        queue.put('DONE')

    for local_process in all_procs:
        local_process.join()
