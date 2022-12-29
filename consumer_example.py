"""
Copyright 2021 Moonsense, Inc.

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

"""
This example script shows how you can easily write a session data consumer
that will periodically pull for new session data chunks and process them.

On start, the scripts checks for active sessions that received new data in
the last 90 seconds and for each stars a thread to process chunks.

Each thread maintains a list of processed chunks and for every new chunk
it will call the process_bundles_chunk() method. That method gets access to all the
bundles in a chunk and can publish cards in the session that will be
visible in the Recorder app.
"""

import logging
import itertools
import time
import threading

from datetime import datetime, timedelta, timezone

from moonsense.models import Session, Chunk
from moonsense.client import Client

#
# Signals combine multiple features derived from source data into a single
# value that can be used to detect suspicious activity. A signal can either
# be based on rules or on a machine learning model.
#
def process_signals(client: Client, session: Session) -> None:
    try:
        signals = client.list_session_signals(session.session_id)
        logging.info(f"Session {session.session_id} signals: {signals}")
    except Exception as e:
        pass


#
# Features are derived from the raw data and can be used as input into
# custom roles or specialized risk scoring models.
#
def process_features(client: Client, session: Session) -> None:
    try:
        response = client.list_session_features(session.session_id)
        logging.info(f"Session {session.session_id} has {len(response.features)} features.")
    except Exception as e:
        pass


#
# Bundles are the smallest unit of data that can be processed. They are
# automatically assembled into chunks for efficient processing.
#
def process_bundles_chunk(client: Client, session: Session, chunk: Chunk) -> None:
    bundles = list(client.read_chunk(session.session_id, chunk.chunk_id))
    logging.info(f"Chunk {chunk.chunk_id} has {len(bundles)} bundles")


def main():
    client = Client()
    monitored = set()

    logging.info("Checking for recent sessions that are actively receiving data")

    while True:

        for session in itertools.islice(client.list_sessions(), 25):
            if session.session_id not in monitored and active(session):
                logging.info("Monitoring %s", session.session_id)
                monitored.add(session.session_id)
                threading.Thread(
                    target=worker,
                    args=(
                        client,
                        session,
                    ),
                ).start()
        time.sleep(2)


def worker(client: Client, session: Session) -> None:
    time.sleep(5)

    processed = set(c.chunk_id for c in client.list_chunks(session.session_id))

    process_signals(client, session)
    process_features(client, session)

    while active(session):
        for chunk in client.list_chunks(session.session_id):
            if chunk.chunk_id not in processed:
                logging.info(
                    "Processing bundles chunk %s for session %s",
                    chunk.chunk_id,
                    session.session_id,
                )
                process_bundles_chunk(client, session, chunk)
                processed.add(chunk.chunk_id)

        time.sleep(30)
        session = client.describe_session(session.session_id)

    logging.info("Session %s is inactive", session.session_id)


def active(session: Session) -> bool:
    newest_event = datetime.fromtimestamp(session.newest_event.seconds, timezone.utc)
    return newest_event > datetime.now(timezone.utc) - timedelta(seconds=90)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
