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

import os
import tempfile
import uuid
import vcr

from moonsense import client

PROTOCOL = "https"
ROOT_DOMAIN = "moonsense.dev"
DEFAULT_REGION = "us-central1.gcp"

SESSION_ID = "zKDPvZfVLMc6jjUHNpmXHk"
SESSION_BUNDLES_COUNT = 2

# PROTOCOL = "http"
# ROOT_DOMAIN = "localhost:8081"
# DEFAULT_REGION = ""


def new_client():
    return client.Client(
        os.environ["SECRET_TOKEN"], ROOT_DOMAIN, PROTOCOL, DEFAULT_REGION
    )

def test_regions():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_regions.yaml', filter_headers=['authorization']):
        c = new_client()
        assert "europe-west1.gcp" in [r.name for r in c.list_regions().regions]


def test_whoami():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_whoami.yaml', filter_headers=['authorization']):
        c = new_client()
        assert c.whoami().app_id != ""


def test_list_sessions():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_list_sessions.yaml', filter_headers=['authorization']):
        c = new_client()
        result = list(c.list_sessions())
        assert len(result) > 0
        assert result[0].app_id != ""

        session = c.describe_session(result[0].session_id)
        assert session.created_at == result[0].created_at


def test_list_and_read_chunks():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_list_and_read_chunks.yaml', filter_headers=['authorization']):
        c = new_client()
        chunks = list(c.list_chunks(SESSION_ID))
        print(chunks)
        assert len(chunks) > 0
        assert chunks[0].md5 != ""

        bundles = c.read_chunk(SESSION_ID, chunks[0].chunk_id)
        count = 0
        for envelope in bundles:
            print("!!")
            assert envelope.bundle is not None
            count += 1
        assert count > 0


def test_download_session():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_download_session.yaml', filter_headers=['authorization']):
        c = new_client()
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_file = os.path.join(tmpdirname, SESSION_ID + ".json")
            c.download_session(SESSION_ID, output_file)
            assert os.path.getsize(output_file) > 1024


def test_read_session():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_read_session.yaml', filter_headers=['authorization']):
        c = new_client()
        bundles = c.read_session(SESSION_ID)
        count = 0
        for envelope in bundles:
            assert envelope.bundle is not None
            count += 1
        assert count == 7


def test_create_and_list_cards():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_create_and_list_cards.yaml', filter_headers=['authorization']):
        c = new_client()
        expected_title = "random-expected-title"
        c.create_card(SESSION_ID, expected_title, "test description")
        result =  c.list_cards(SESSION_ID)
        assert result[0].title == expected_title

def test_set_and_retrieve_labels():
    with vcr.use_cassette('fixtures/vcr_cassettes/test_set_and_retrieve_labels.yaml', filter_headers=['authorization']):
        c = new_client()
        c.update_session_labels(SESSION_ID, ["stopped-for-visibility-change", "test", "hello"])

        session = c.describe_session(SESSION_ID)

        labels = []
        for label in session.labels:
            labels.append(label.name)

        sorted_labels = sorted(labels)
        assert sorted_labels == ['hello', 'stopped-for-visibility-change', 'test']