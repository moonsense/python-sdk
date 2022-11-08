"""
Copyright 2022 Moonsense, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

""" Moonsense Cloud API - Download all sessions"""


import os
from time import time, sleep
import signal
from functools import partial

from datetime import date, datetime
from multiprocessing import Process, JoinableQueue, Event
from queue import Empty

from google.protobuf.json_format import MessageToJson
from retry import retry

from . import Platform

MISSING_GROUP_ID = "missing-group-id"
GRACE_PERIOD = 2
KILL_PERIOD = 30

def handler(signalname):
    def wrapper_handler(signal_received, frame):
        raise KeyboardInterrupt(f"{signalname} received")
    return wrapper_handler


class DownloadAllSessions(object):
    def __init__(
        self,
        moonsense_client) -> None:
        self.moonsense_client = moonsense_client
        self.queue = JoinableQueue()
        self.stop_event = Event()
    
    @retry(Exception, tries=3, delay=0)
    def download_data_into_folder(
        self,
        datadir: str,
        with_group_id: bool,
        session_id: str) -> None:

        session = None
        try:
            session = self.moonsense_client.describe_session(session_id)
        except Exception as e:
            print("Error encountered while describing session", e)
            raise e

        group_id = session.client_session_group_id
        if group_id is None or len(group_id) == 0:
            group_id = MISSING_GROUP_ID
        
        session_as_json = MessageToJson(session)

        created_at = datetime.fromtimestamp(session.created_at.seconds).date()
        formatted_created_at = created_at.strftime("%Y-%m-%d")

        print("Downloading session", session_id, "created at", formatted_created_at)

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
            self.moonsense_client.download_session(session_id, raw_sealed_bundles_path)
            if 'packet' in session.counters:
                self.moonsense_client.download_pcap_data(session_id, pcap_path)
        except Exception as e:
            print("Error encountered while downloading session", e)
            raise e

    def download_session(self, queue, stop_event, datadir, with_group_id):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

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
                continue

            try:
                session_id = msg
                self.download_data_into_folder(datadir, with_group_id, session_id)
            finally:
                queue.task_done()
    
    def download(
        self,
        output: str,
        until: datetime,
        since: datetime,
        labels: list[str],
        platforms: list[Platform],
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
        :param platforms: Filter downloaded sessions by the platforms they were produced:
                         web, ios, android or None for all.
        :param with_group_id: If set to True, organizes the downloaded sessions by date and
                            client session group id. Default: False.
        """
        signal.signal(signal.SIGINT, handler("SIGINT"))
        signal.signal(signal.SIGTERM, handler("SIGTERM"))

        localdir = os.getcwd()
        datadir = os.path.join(localdir, "data")
        # if output is present, check if it's absolute or relative
        if output is not None:
            if os.path.isabs(output):
                datadir = output
            else:
                datadir = os.path.join(os.getcwd(), output)
        
        # if path not present create it
        if not os.path.isdir(datadir):
            os.makedirs(datadir, exist_ok=True)

        number_of_processes = os.cpu_count() * 2

        if since > until:
            raise ValueError("Since value larger than until value")

        all_procs = []
        for process_count in range(number_of_processes):
            local_process = Process(target=self.download_session,
                daemon=True,
                args=((self.queue, self.stop_event, datadir, with_group_id)))
            all_procs.append(local_process)
            local_process.start()

        session_counter = 0
        filter_by_labels = labels if len(labels) > 0 else None

        try:
            # listing is in reverse chronological order - newest are first. 
            for session in self.moonsense_client.list_sessions(filter_by_labels, platforms=platforms, since=since, until=until):
                group_id = session.client_session_group_id
                if group_id is None or len(group_id) == 0:
                    group_id = MISSING_GROUP_ID

                created_at = datetime.fromtimestamp(session.created_at.seconds).date()

                if created_at > until:
                    continue

                if created_at < since:
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
                self.queue.put(session.session_id)
            
            for local_process in all_procs:
                self.queue.put(None)
            
            self.queue.join()
        except KeyboardInterrupt:
            self.stop_event.set()
            t = time()
            while alive_procs := [p for p in all_procs if p.is_alive()]:
                if time() > t + GRACE_PERIOD:
                    for p in alive_procs:
                        os.kill(p.pid, signal.SIGINT)
                elif time() > t + KILL_PERIOD:
                    for p in alive_procs:
                        p.kill()
                sleep(.01)