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

from typing import Any

import os
import tempfile
import uuid
import io
import tarfile
import gzip

import json
import responses
from responses import matchers
import datetime

import shortuuid

from moonsense import client

PROTOCOL = "https"
ROOT_DOMAIN = "moonsense.dev"
DEFAULT_REGION = "us-central1.gcp"

SESSION_ID = "zKDPvZfVLMc6jjUHNpmXHk"
SESSION_BUNDLES_COUNT = 2

MOCK_SECRET_TOKEN = "test.secret.token"

def new_client():
    return client.Client(MOCK_SECRET_TOKEN, ROOT_DOMAIN, PROTOCOL, DEFAULT_REGION)


def generate_test_session(session_id=shortuuid.uuid(),
    app_id=shortuuid.uuid(),
    created_at=datetime.datetime.now(),
    labels=[],
    region_id=DEFAULT_REGION):

    return {
        "session_id": session_id,
        "app_id": app_id,
        "created_at": created_at.isoformat() + "Z",
        "metadata":{
            "platform":"iOS"
        },
        "labels": labels,
        "region_id": region_id
    }


def generate_test_sessions_list(count, current_page, total_pages, total_count):
    sessions = []
    for i in range(count):
        sessions.append(generate_test_session())
    return {
        "sessions": sessions,
        "pagination":{
            "current_page": current_page,
            "per_page":50,
            "total_pages": total_pages,
            "total_count": total_count
        }}


def generate_downloadable_payload(data: str) -> bytes:
    data_buffer = io.BytesIO()
    data_buffer.write(data.encode())
    data_buffer.seek(0)

    # create tar gz file.
    ioBuffer = io.BytesIO()
    with tarfile.open(fileobj=ioBuffer, mode="w:gz") as tar:
        info = tarfile.TarInfo("test-session_id1.json")
        info.size = len(data)
        tar.addfile(info, data_buffer)
    
    return ioBuffer.getvalue()


# The chunk payload is a format of a JSON per line, gzipped.
def generate_chunk_payload(data: list[dict[str, Any]]) -> bytes:
    data_buffer = io.BytesIO()
    gzip_handler = gzip.GzipFile(fileobj=data_buffer, mode='w')
    for item in data:
        json_line = json.dumps(item) + "\n"
        gzip_handler.write(json_line.encode('utf8'))
    gzip_handler.close()
    
    return data_buffer.getvalue()


def generate_bundle(session_id, bundle_index=1):
    return {
        "bundle": {
            "index": bundle_index,
        },
        "session_id": session_id
    }

def test_regions():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://api.moonsense.dev/v2/regions",
            body=json.dumps({
                "regions":[
                    {"name":"us-central1.gcp", "url":"https://us-central1.gcp.data-api.moonsense.dev",
                     "default_primary":True, "status":"ok"},
                    {"name":"europe-west1.gcp", "url":"https://europe-west1.gcp.data-api.moonsense.dev", 
                     "default_backup":True, "status":"ok"}
                ]
            }),
            status=200,
            content_type="application/json",
        )

        c = new_client()
        assert "europe-west1.gcp" in [r.name for r in c.list_regions().regions]


def test_whoami():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/tokens/self",
            body=json.dumps({
                "app_id":"test_app_id",
                "project_id":"test_project_id",
                "scopes":"cqt"}),
            status=200,
            content_type="application/json",
        )
        c = new_client()
        response = c.whoami()
        assert response.app_id == "test_app_id"
        assert response.project_id == "test_project_id"


def test_list_sessions():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions?per_page=50&page=1",
            body=json.dumps({
                "sessions":[
                    generate_test_session("test_session_id1", "test_app_id"),
                    generate_test_session("test_session_id2", "test_app_id")
                ],
                "pagination":{
                    "current_page":1,
                    "per_page":50,
                    "total_pages":1,
                    "total_count":2
                }}),
            status=200,
            content_type="application/json",
        )

        c = new_client()
        result = list(c.list_sessions())
        assert len(result) == 2
        assert result[0].app_id == "test_app_id"
        assert result[0].session_id == "test_session_id1"

        assert result[1].app_id == "test_app_id"
        assert result[1].session_id == "test_session_id2"


def test_list_sessions_with_pagination():
    session_page1 = generate_test_sessions_list(count=2, current_page=1, total_pages=2, total_count=4)
    session_page2 = generate_test_sessions_list(count=2, current_page=2, total_pages=2, total_count=4)

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions?per_page=50&page=1",
            body=json.dumps(session_page1),
            status=200,
            content_type="application/json",
        )

        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions?per_page=50&page=2",
            body=json.dumps(session_page2),
            status=200,
            content_type="application/json",
        )

        c = new_client()
        result = list(c.list_sessions())
        assert len(result) == 4
        assert result[0].session_id == session_page1["sessions"][0]["session_id"]
        assert result[0].app_id == session_page1["sessions"][0]["app_id"]
        

def test_list_and_read_chunks():
    test_session = generate_test_session("test_session_id1", "test_app_id")
    created_at = datetime.datetime.now()

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1?view=minimal",
            body=json.dumps(test_session),
            status=200,
            content_type="application/json",
        )

        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1/chunks?per_page=50&page=1",
            body=json.dumps({
                "session_id": "test_session_id1",
                "chunks": [{"chunk_id": "chunk_id1", "md5": "abcd", "created_at": created_at.isoformat() + "Z"}],
                "pagination":{"current_page":1,"total_pages":1}
            }),
            status=200,
            content_type="application/json",
        )

        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1/chunks/chunk_id1",
            body=generate_chunk_payload([
                generate_bundle("test_session_id1", 1),
                generate_bundle("test_session_id1", 2)
            ]),
            headers={'Content-Encoding': 'gzip'},
            status=200,
            content_type="application/json",
        )

        c = new_client()
        chunks = list(c.list_chunks("test_session_id1"))
        assert len(chunks) == 1
        assert chunks[0].md5 == "abcd"

        bundles = c.read_chunk("test_session_id1", chunks[0].chunk_id)
        count = 0
        for envelope in bundles:
            assert envelope.bundle is not None
            count += 1
        
        assert count == 2


def test_download_session():
    test_session = generate_test_session("test_session_id1", "test_app_id")
    created_at = datetime.datetime.now()
    payload = json.dumps({"hello": "world"})

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1?view=minimal",
            body=json.dumps(test_session),
            status=200,
            content_type="application/json")
        
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1/bundles",
            body=generate_downloadable_payload(payload),
            status=200,
            content_type="application/json")

        c = new_client()
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_file = os.path.join(tmpdirname, "test_session_id1.json")
            c.download_session("test_session_id1", output_file)
            assert os.path.getsize(output_file) == len(payload)


def test_download_packets():
    test_session = generate_test_session("test_session_id1", "test_app_id")
    created_at = datetime.datetime.now()
    payload = json.dumps({"hello": "world"})

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1?view=minimal",
            body=json.dumps(test_session),
            status=200,
            content_type="application/json")
        
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1/network-telemetry/packets",
            body=generate_downloadable_payload(payload),
            status=200,
            content_type="application/json")

        c = new_client()
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_file = os.path.join(tmpdirname, "test_session_id1.json")
            c.download_pcap_data("test_session_id1", output_file)
            assert os.path.getsize(output_file) == len(payload)


def test_read_session():
    test_session_id = "test_session_id1"
    test_session = generate_test_session(test_session_id, "test_app_id")
    created_at = datetime.datetime.now()
    payload = json.dumps(generate_bundle(test_session_id, 1)) + \
        "\n" + json.dumps(generate_bundle(test_session_id, 2)) + \
        "\n" + json.dumps(generate_bundle(test_session_id, 3))

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1?view=minimal",
            body=json.dumps(test_session),
            status=200,
            content_type="application/json")
        
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1/bundles",
            body=generate_downloadable_payload(payload),
            status=200,
            content_type="application/json")

        c = new_client()
        bundles = c.read_session("test_session_id1")
    
        count = 0
        for envelope in bundles:
            assert envelope.bundle is not None
            count += 1
        assert count == 3


def test_set_and_retrieve_labels():
    test_session_id = "test_session_id1"
    test_session = generate_test_session(test_session_id, "test_app_id", labels=[
        {"name":"label1"},
        {"name":"label2"}
    ])

    updated_session = generate_test_session(test_session_id, "test_app_id", labels=[
        {"name":"label1"},
        {"name":"updated_label1"},
        {"name":"updated_label2"},
    ])

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1?view=minimal",
            body=json.dumps(test_session),
            status=200,
            content_type="application/json",
        )

        rsps.add(
            responses.POST,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1/labels",
            body="",
            match=[
                matchers.json_params_matcher({"labels": [
                    {"name": "label1"},
                    {"name": "updated_label1"},
                    {"name": "updated_label2"}
                ]})
            ],
            status=200,
            content_type="application/json",
        )

        rsps.add(
            responses.GET,
            "https://us-central1.gcp.data-api.moonsense.dev/v2/sessions/test_session_id1?view=minimal",
            body=json.dumps(updated_session),
            status=200,
            content_type="application/json",
        )

        c = new_client()
        session = c.describe_session(test_session_id)
        
        labels = []
        for label in session.labels:
            labels.append(label.name)
        assert sorted(labels) == ['label1', 'label2']

        c.update_session_labels(test_session_id, ["label1", "updated_label1", "updated_label2"])

        session = c.describe_session(test_session_id)

        labels = []
        for label in session.labels:
            labels.append(label.name)

        sorted_labels = sorted(labels)
        assert sorted_labels == ["label1", "updated_label1", "updated_label2"]
