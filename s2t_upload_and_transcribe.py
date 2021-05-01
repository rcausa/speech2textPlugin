import requests
import os
import time
import glob
import json
from word2number.w2n import word_to_num

"""
Uses the Aseembly API - https://docs.assemblyai.com/overview/getting-started
"""


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
    Returns the transcription repsonse which includes transcribed words.
    The response 'status' can be 'queued', 'processing', 'completed'

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
            waiting = False
            return completion_response_json
            
        time.sleep(0.0001)
    

def parse_input(string):
    """
    Turns voice commands into Linux Terminal commands.
    Each option must be specified separately, e.g. 
    you cannot have 'ls -ltr', only 'ls -l -t -r'.

    Parameters: speech2text string (str)
    Returns: Linux Terminal command (str) to be executed.
    """
    with open('./keywords.json','r') as json_f:
        cmd_dict = json.load(json_f)

    cmd_string = ''
    all_words = string.split(' ')
    i = 0
    capital_count = 0
    while i < len(all_words):
        time.sleep(0.4)
        try:
            # print(f'Word {i}: {all_words[i]}')
            if all_words[i] == 'dash':
                cmd_string += cmd_dict['dash'] # no space after '-'
                i += 1
            elif all_words[i] == 'capital':
                capital_count = 1
                i += 1
                
                if all_words[i] == 'twenty':
                    double_digit = 'twenty ' + all_words[i+1]
                    if isinstance(word_to_num(double_digit), int):
                        cmd_string += cmd_dict['capital ' + double_digit] + ' '
                        i += 2 
                    else:
                        cmd_string += cmd_dict['capital ' + 'twenty'] + ' '
                        i += 1

                    
                elif isinstance(word_to_num(all_words[i]), int):
                    cmd_string += cmd_dict[all_words[i]] + ' '
                    i += 1
                else:
                    print('Digit not recognised.')
                    i += 1
                
                
            elif all_words[i] == 'twenty':
                double_digit = 'twenty ' + all_words[i+1]
                if isinstance(word_to_num(double_digit), int):
                    cmd_string += cmd_dict[double_digit] + ' '
                    i += 2 
                else:
                    cmd_string += cmd_dict['twenty'] + ' '
                    i += 1
            # numbers below twenty handled with the last 'else'
                    
            elif all_words[i] == 'left':
                next_word = all_words[i+1]
                if next_word == 'square':
                    cmd_string += cmd_dict['left square']
                    i += 2
                elif next_word == 'curly':
                    cmd_string += cmd_dict['left curly']
                    i += 2
                elif next_word == 'angle':
                    cmd_string += cmd_dict['left angle']
                    i += 2
                elif next_word == 'parenthesis':
                    cmd_string += cmd_dict['left parenthesis']
                    i += 2
                else: 
                    print('Bracket not recognised.')
                    i += 1

            elif all_words[i] == 'right':
                next_word = all_words[i+1]
                if next_word == 'square':
                    cmd_string += cmd_dict['right square']
                    i += 2
                elif next_word == 'curly':
                    cmd_string += cmd_dict['right curly']
                    i += 2
                elif next_word == 'angle':
                    cmd_string += cmd_dict['right angle']
                    i += 2
                elif next_word == 'parenthesis':
                    cmd_string += cmd_dict['right parenthesis']
                    i += 2
                else: 
                    print('Bracket not recognised.')
                    i += 1
                
            else:
                cmd_string += cmd_dict[all_words[i]] + ' '
                i += 1
            capital_count = 0

        except: # handle spaces, punctuation, empty strings, chars not in dict.
            print(f'Word not present in dict: {all_words[i]}')
            i += 1
    return cmd_string


if __name__ == "__main__":
    API_URL = "https://api.assemblyai.com/v2/"

    with open('./auth_key.txt','r') as f:
        AUTH_TOKEN = f.readline().rstrip('\n')

    filename = "./recordings/output4.wav"
    upload_response = upload(filename, AUTH_TOKEN)
    
    transcribe_json = {
        "audio_url" : upload_response["upload_url"],
        "punctuate": False,
        "format_text": False
    }
    transcribe_response = transcribe(transcribe_json)
    
    sentence = ""
    print('Number of transcribed words: ',len(transcribe_response['words']))
    for word_dict in transcribe_response['words']:
        sentence += word_dict["text"] + ' '

    print(f"Transcription:\n >> {sentence}")

    # sentence = 'list dash capital twenty four left curly dollar zero right curly'
    print(parse_input(sentence))
