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
import signal
import json
from time import time, sleep
from functools import partial

from datetime import date, datetime, timedelta
from multiprocessing import Process, JoinableQueue, Event
from queue import Empty

from google.protobuf.json_format import MessageToJson
from retry import retry

from . import Platform

MISSING_JOURNEY_ID = "missing-journey-id"
GRACE_PERIOD = 2
KILL_PERIOD = 30

MAX_TIMESTAMP_FILENAME = "max_timestamp"


class DownloadAllSessions(object):
    def __init__(
        self,
        moonsense_client) -> None:
        self.moonsense_client = moonsense_client
        self.queue = JoinableQueue(maxsize=25)
        self.stop_event = Event()

    @retry(Exception, tries=3, delay=0)
    def download_data_into_folder(
        self,
        datadir: str,
        with_journey_id: bool,
        session_id: str) -> None:

        session = None
        try:
            session = self.moonsense_client.describe_session(session_id)
        except Exception as e:
            print("Error encountered while describing session", e)
            raise e


        journey_id = session.journey_id
        if journey_id is None or len(journey_id) == 0:
            journey_id = MISSING_JOURNEY_ID

        session_as_json = MessageToJson(session)

        created_at = datetime.fromtimestamp(session.created_at.seconds).date()
        formatted_created_at = created_at.strftime("%Y-%m-%d")

        print("Downloading session", session_id, "created at", formatted_created_at)

        session_dir_path = os.path.join(datadir, formatted_created_at, session.session_id)
        if with_journey_id:
            session_dir_path = os.path.join(datadir,
                created_at.strftime("%Y-%m-%d"),
                journey_id,
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

    def download_session(self, queue, stop_event, datadir, with_journey_id):
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
                self.download_data_into_folder(datadir, with_journey_id, session_id)
            finally:
                queue.task_done()

    def _read_metadata_file_for_created_at(self, metadata_file_path: str) -> int:
        with open(metadata_file_path, "r") as metadata_file:
            metadata = json.load(metadata_file)
            created_at = datetime.strptime(metadata["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
            return int(created_at.timestamp())

    def get_max_timestamp(self, datadir: str, with_journey_id: bool) -> int:
        max_date = None
        for dated_dir in os.listdir(datadir):
            try:
                date = datetime.strptime(dated_dir, "%Y-%m-%d")
                if max_date is None or date > max_date:
                    max_date = date
            except ValueError:
                continue

        if max_date is None:
            return None

        # within the folder with max date - do we have the max_timestamp file? if so read that and return
        max_timestamp_file_path = os.path.join(datadir, max_date.strftime("%Y-%m-%d"), MAX_TIMESTAMP_FILENAME)
        if os.path.isfile(max_timestamp_file_path):
            with open(max_timestamp_file_path, "r") as max_timestamp_file:
                max_timestamp = max_timestamp_file.read()
        else:
            # if there is no max_timestamp file, look through the max_date folder and find the max timestamp
            # by reading the created_at field from the metadata.json file
            max_folder_path = os.path.join(datadir, max_date.strftime("%Y-%m-%d"))
            for folder_name in os.listdir(max_folder_path):
                # folder name can be either a session_id or a journey_id depending if with_journey_id is set
                if with_journey_id:
                    # if with_journey_id is set, the folder name is a journey_id
                    for session_id in os.listdir(os.path.join(max_folder_path, folder_name)):
                        metadata_file_path = os.path.join(max_folder_path, folder_name, session_id, "metadata.json")
                        if os.path.isfile(metadata_file_path):
                            max_timestamp = self._read_metadata_file_for_created_at(metadata_file_path)
                else:
                    # if with_journey_id is not set, the folder name is a session_id
                    metadata_file_path = os.path.join(max_folder_path, folder_name, "metadata.json")
                    max_timestamp = self._read_metadata_file_for_created_at(metadata_file_path)

        return max_timestamp


    def _write_max_timestamp_file(self, datadir: str, created_at_str: str, max_timestamp: int):
        max_timestamp_file_path = os.path.join(datadir, created_at_str, MAX_TIMESTAMP_FILENAME)
        with open(max_timestamp_file_path, "w") as f:
            f.write(str(max_timestamp))


    def download(
        self,
        output: str,
        until: datetime,
        since: datetime,
        skip_days: list[date],
        incremental: bool,
        labels: list[str],
        platforms: list[Platform],
        with_journey_id: bool = False) -> None:
        """
        Download all sessions from a project based on the provided filters.

        :param output: Path to the output directory - either absolut or relative to the current
                       directory.
        :param until: Date in the YYYY-MM-DD format until the session data should be included.
                    If not provided, the current day is used.
        :param skip_days: A list of dates that should be skipped.
        :param incremental: If set to True, only downloads sessions that are not already downloaded.
        :param since: Date in the YYYY-MM-DD format since the session data should be included.
                    If not provided beginning of Moonsense time - 1st of January 2021 is used.
        :param labels: A list of labels to filter sessions by. A session needs to include at least
                    one label in this list to be downloaded.
        :param platforms: Filter downloaded sessions by the platforms they were produced:
                         web, ios, android or None for all.
        :param with_journey_id: If set to True, organizes the downloaded sessions by date and
                            journey id. Default: False.
        """
        localdir = os.getcwd()
        datadir = os.path.join(localdir, "data")
        # if output is present, check if it's absolute or relative
        if output is not None:
            if os.path.isabs(output):
                datadir = output
            else:
                datadir = os.path.join(os.getcwd(), output)

        if not isinstance(since, datetime):
            since = datetime.combine(since, datetime.min.time())

        if not isinstance(until, datetime):
            until = datetime.combine(until, datetime.max.time())

        # if path not present create it
        if not os.path.isdir(datadir):
            os.makedirs(datadir, exist_ok=True)

        # MOONSENSE_DOWNLOAD_PARALLELISM is the number of parallel processes to use
        # if not set, use the number of cores * 2    
        number_of_processes = int(os.environ.get("MOONSENSE_DOWNLOAD_PARALLELISM", os.cpu_count() * 2))

        max_timestamp = None
        if incremental:
            max_timestamp = self.get_max_timestamp(datadir, with_journey_id)
            if max_timestamp is not None:
                max_timestamp = datetime.fromtimestamp(int(max_timestamp))
                # if we have a max_timestamp, we need to add 1 second to it
                # so that we don't download the same session again
                max_timestamp = max_timestamp + timedelta(seconds=1)
                since = max_timestamp

        if since > until:
            raise ValueError("Since value larger than until value")

        all_procs = []
        for process_count in range(number_of_processes):
            local_process = Process(target=self.download_session,
                daemon=True,
                args=((self.queue, self.stop_event, datadir, with_journey_id)))
            all_procs.append(local_process)
            local_process.start()

        session_counter = 0
        filter_by_labels = labels if len(labels) > 0 else None

        max_timestamp_per_day = {}

        print("Downloading sessions from {} to {}".format(since, until))

        try:
            # listing is in reverse chronological order - newest are first.
            for session in self.moonsense_client.list_sessions(filter_by_labels, platforms=platforms, since=since,
                                                               until=until):
                journey_id = session.journey_id
                if journey_id is None or len(journey_id) == 0:
                    journey_id = MISSING_JOURNEY_ID

                created_at_datetime = datetime.fromtimestamp(session.created_at.seconds)
                created_at_timestamp = int(created_at_datetime.timestamp())

                if skip_days is not None:
                    matched = False
                    for skip_day in skip_days:
                        if (created_at_datetime.date() - skip_day).days == 0:
                            print("Skipping sessions id {} because it was created on {}".format(session.session_id, skip_day))
                            matched = True
                            break

                    if matched:
                        continue

                if created_at_datetime > until:
                    continue

                if created_at_datetime < since:
                    break

                created_at_str = created_at_datetime.date().strftime("%Y-%m-%d")

                session_dir_path = os.path.join(datadir, created_at_str, session.session_id)
                if with_journey_id:
                    session_dir_path = os.path.join(datadir,
                        created_at_str,
                        journey_id,
                        session.session_id)

                if not os.path.isdir(session_dir_path):
                    os.makedirs(session_dir_path)

                if created_at_str in max_timestamp_per_day:
                    if created_at_timestamp > max_timestamp_per_day[created_at_str]:
                        max_timestamp_per_day[created_at_str] = created_at_timestamp
                        self._write_max_timestamp_file(datadir, created_at_str, created_at_timestamp)
                else:
                    max_timestamp_per_day[created_at_str] = created_at_timestamp
                    self._write_max_timestamp_file(datadir, created_at_str, created_at_timestamp)

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
