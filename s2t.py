import requests
import os

API_URL = "https://api.assemblyai.com/v2/"
API_TOKEN = "4ece715f10514fb89421a127b7d03f4c"

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data)

def upload(filename, auth_token):
    headers = {'authorization': auth_token}
    response = requests.post(
        API_URL + 'upload', 
        headers=headers,
        data=read_file(filename
    ))
    return response.json()

def transcribe():
    """

    """
    pass
