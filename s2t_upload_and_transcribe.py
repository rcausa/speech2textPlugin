import requests
import os
import time

def read_file(filename, chunk_size=5242880):
    """
    Reads an existing audio file in chunks.

    Parameters: filename (str), chunk_size (int)
    Yields:  data (binary)
    """
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

def upload(filename, auth_token):
    """
    Uploads chunked audio file to AssemblyAI API.
    
    Parameters: filename (str), auth_token (str)
    Returns: json API response
    """
    headers = {'authorization': auth_token}
    response = requests.post(
        API_URL+'upload', 
        headers=headers,
        data=read_file(filename
    ))
    return response.json()

def transcribe(upload_response):
    """
    Returns the transcription repsonse which includes
    transcribed words.
    Response'status' which can be 'queued', 'processing', 'completed'

    Parameters: json API response from upload.
    Returns: json API response from transcription.
    """
    headers = {
        "authorization": AUTH_TOKEN,
        "content-type": "application/json"
    }
    response = requests.post(
        API_URL+'transcript',
        json = upload_response,
        headers = headers
    )
    transcribe_response =  response.json()
    transcribe_id = transcribe_response["id"]

    completed_transcription_URL = API_URL+'transcript/'+transcribe_id
    
    waiting = True
    while waiting:
        completion_response = requests.get(
            completed_transcription_URL, 
            headers = {
                "authorization" : AUTH_TOKEN
            }
        )

        completion_response_json = completion_response.json()
        if completion_response_json["status"] == 'completed':
            return completion_response_json
            waiting = False
            
        time.sleep(0.0001)


if __name__ == "__main__":
    API_URL = "https://api.assemblyai.com/v2/"

    with open('./auth_key.txt','r') as f:
        AUTH_TOKEN = f.readline().rstrip('\n')

    filename = "./output.mp4"
    upload_response = upload(filename, AUTH_TOKEN)
    
    transcribe_json = {
        "audio_url" : upload_response["upload_url"]
    }
    transcribe_response = transcribe(transcribe_json)
    
    
    sentence = ""
    for word_dict in transcribe_response['words']:
        sentence += word_dict["text"] + ' '

    print(f"Transcription:\n >> {sentence}")