import os
import pytest

from moonsense import client

PROTOCOL = "https"
ROOT_DOMAIN = "moonsense.dev"
DEFAULT_REGION = "us-central1.gcp"

# PROTOCOL = "http"
# ROOT_DOMAIN = "localhost:8081"
# DEFAULT_REGION = ""


def new_client():
    return client.Client(
        os.environ["SECRET_TOKEN"], ROOT_DOMAIN, PROTOCOL, DEFAULT_REGION
    )


def test_regions():
    c = new_client()
    assert "europe-west1.gcp" in [r["name"] for r in c.regions()]


def test_whoami():
    c = new_client()
    assert c.whoami()["app_id"] != ""


def test_sessions():
    c = new_client()
    result = list(c.sessions())
    assert len(result) > 0
    assert result[0].app_id != ""


def test_chunks():
    session_id = "TPhqRmrgHeSRigJxbavQhh"
    pass
