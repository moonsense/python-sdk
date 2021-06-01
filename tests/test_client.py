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
from moonsense import client
import dotenv

dotenv.load_dotenv()

PROTOCOL = "https"
ROOT_DOMAIN = "moonsense.dev"
DEFAULT_REGION = "us-central1.gcp"
SESSION_ID = "qCyM5JXCzPgniCnZjVdjqD"

# PROTOCOL = "http"
# ROOT_DOMAIN = "localhost:8081"
# DEFAULT_REGION = ""


def new_client():
    return client.Client(
        os.environ["SECRET_TOKEN"], ROOT_DOMAIN, PROTOCOL, DEFAULT_REGION
    )


def test_env_variable_client():
    c = client.Client(None, ROOT_DOMAIN, PROTOCOL, DEFAULT_REGION)
    assert isinstance(c, client.Client)


def test_regions():
    c = new_client()
    assert "europe-west1.gcp" in [r["name"] for r in c.list_regions()]


def test_whoami():
    c = new_client()
    assert c.whoami()["app_id"] != ""


def test_list_sessions():
    c = new_client()

    result = list(c.list_sessions())
    assert len(result) > 0
    assert result[0].app_id != ""

    session = c.describe_session(result[0].session_id)
    assert session.created_at == result[0].created_at


def test_list_chunks():
    c = new_client()
    chunks = list(c.list_chunks(SESSION_ID))
    assert len(chunks) > 0
    assert chunks[0].md5 != ""


def test_download_session():
    c = new_client()
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_file = os.path.join(tmpdirname, SESSION_ID + ".json")
        c.download_session(SESSION_ID, output_file)
        assert os.path.getsize(output_file) > 1024