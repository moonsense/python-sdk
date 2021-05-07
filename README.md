# moonsense

Simple client library for the Moonsense Cloud API.

# Installation

Install the module

```shell
python setup.py install 
```

# Getting Started

Query for previously recorded sessions:

```python
from moonsense.client import Client

YOUR_SECRET_KEY_HERE = ''
client = Client(secret_token=YOUR_SECRET_KEY_HERE)
for session in client.list_sessions():
    print(session)
```

Note that explicitly writing your Moonsense secret key is discharged for security reasons. You may set `MOONSENSE_SECRET_KEY` as an
environment variable, and instnatiate your client without specifying na input secret token.

## Tests

Simply run: `pytest`

## Code coverge

Generate coverage report with: `py.test --cov=moonsense tests/`
