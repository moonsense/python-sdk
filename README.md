# Moonsense Cloud API Client

Simple client library for the Moonsense Cloud API.

# Installation

Install the module from PyPI: 

```shell
pip install moonsense 
```

Or from source like this:

```shell
python setup.py install 
```

# Getting Started

Start by getting an API secret key by navigating to App in Console and creating a token. You will need to save the generated secret key to a secure place.

https://console.moonsense.cloud/dashboard

We recommend exporting the API secret key as an environment variable:

    export MOONSENSE_SECRET_TOKEN=...

You can then very easily list sessions and access the granular data:

```python
from moonsense.client import Client

client = Client()
for session in client.list_sessions():
    print(session)

    for bundle in client.read_session(session.session_id):
        # Each bundle is a SealedBundle. See schema below.

```

**Recommended:** For a more realistic example see [consumer_example.py](https://github.com/moonsense/python-sdk/blob/main/consumer_example.py). It shows how you can write a consumer that will process session data using an incremental approach.

# Webhooks

See [webhook_example.py](https://github.com/moonsense/python-sdk/blob/main/webhook_example.py) for an example on how to create a very simple handler that the consumer webhooks.

The request payload use the following schema:

```protobuf
 message WebhookPayload {
    string project_id = 1; // checked in the handler since not all event types can provide a projectId.
    string app_id = 2;
    string session_id = 3;
    WebhookEventTypes event_type = 4;
    v2.bundle.SealedBundle bundle = 5; // payload is optional and only a small number of events require a bundle.
    string client_session_group_id = 6;
    repeated string session_labels = 7;
}
```

The following webhook types are supported:

```protobuf
enum WebhookEventTypes {
    UNKNOWN = 0;
    SESSION_CREATED = 1;
    BUNDLE_RECEIVED = 2;
    CHUNK_PERSISTED = 3;
    SESSION_INACTIVE = 4;
}
```

# Tests

Simply run: `pytest`

# Release

```bash
rm -rf build/ dist/
python setup.py sdist bdist_wheel
twine upload dist/*
```

Dont' forget to bump main branch to the next version.

# Code coverge

Generate coverage report with: `py.test --cov=moonsense tests/`
