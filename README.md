
# moonsense

Simple client library for the Moonsense Cloud API.

## Tests

Simply run: `pytest`


## Code coverge

Generate coverage report with: `py.test --cov=moonsense tests/`

####  script:
####    - pip install --user --upgrade setuptools wheel twine numpy
####    - python3 setup.py sdist bdist_wheel
####    - python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
####  before_script:
####    - bumpversion minor setup.py