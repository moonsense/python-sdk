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

import logging
import itertools
import time
import threading

from datetime import datetime, timedelta, timezone

from moonsense.models import Session, Chunk
from moonsense.client import Client

# Override the process_chunk method to do useful things with the session data

def process_chunk(client: Client, session: Session, chunk: Chunk) -> None:
    bundles = list(client.read_chunk(chunk))

    client.create_card(
        session.session_id,
        "Python Consumer Example",
        f"Chunk {chunk.chunk_id} has {len(bundles)} bundles",
    )


def main():
    client = Client()
    monitored = set()
    while True:
        logging.info("Checking for recent sessions that are actively receiving data")

        for session in itertools.islice(client.list_sessions(), 25):
            if session.session_id not in monitored and active(session):
                logging.info("Starting to monitor %s", session.session_id)
                monitored.add(session.session_id)
                threading.Thread(
                    target=worker,
                    args=(
                        client,
                        session,
                    ),
                ).start()

        logging.info("Waiting for 10 seconds until the next check")
        time.sleep(10)


def worker(client: Client, session: Session) -> None:
    logging.info(
        "Fetching the initial list of session data chunks for session %s",
        session.session_id,
    )
    processed = set(c.chunk_id for c in client.list_chunks(session.session_id))
    while active(session):
        for chunk in client.list_chunks(session.session_id):
            if chunk.chunk_id not in processed:
                logging.info(
                    "Processing chunk %s for session %s",
                    chunk.chunk_id,
                    session.session_id,
                )
                process_chunk(client, session, chunk)
                processed.add(chunk.chunk_id)

        logging.info("Waiting for 30 seconds to check for new session data chunks")
        time.sleep(30)
        session = client.describe_session(session.session_id)

    logging.info("Done monitoring session %s", session.session_id)


def active(session: Session) -> bool:
    return (datetime.now(timezone.utc) - session.newest_event) < timedelta(seconds=90)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()