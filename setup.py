from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='moonsense',
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    description='Moonsense Cloud API client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    url='https://github.com/moonsense/python-sdk.git',
    author='Moonsense Team',
    author_email='support@moonsense.io',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
