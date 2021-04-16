import pytest

from moonsense import client

def test_fahrToKelv():
    '''
    make sure freezing is calculated correctly
    '''
    
    assert client.fahrToKelv(32) == 273.15, 'incorrect freezing point!'
