import requests
import os

API_URL = "https://api.assemblyai.com/v2/"

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
    
