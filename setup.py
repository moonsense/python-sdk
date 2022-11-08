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

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="moonsense",
    version="0.9.1",
    packages=find_packages(exclude=["tests*"]),
    description="Moonsense Cloud API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': ['moonsense=moonsense.cli:main'],
    },
    install_requires=[
        "protobuf>=3,<4",
        "requests>=2.26,<3",
        "pandas>=1.3,<2",
        "click>=8.1,<9",
        "retry>=0.9,<1",
    ],
    url="https://github.com/moonsense/python-sdk.git",
    author="Moonsense Team",
    author_email="support@moonsense.io",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha"
    ],
)
