import requests
import base64
import subprocess

"""
soxi: https://linux.die.net/man/1/soxi
- Used to check .wav header information bits 

ffmpeg CLI options:
-i : input file
-t : time (seconds)
-ar : sampling rate (Hz)
-ac : number of audio channels
-b:a : audio bit rate (num/sec)
"""
# Use this Terminal cmd to record from native audio channel
ffmpeg_cmd = 'ffmpeg -f avfoundation -i ":0" -t 5 -ar 8000 -ac 1 -b:a 128k output.wav'

def check_wav_specs(filepath):
    correct_specs = {
        "Sample Encoding" : "16-bit Signed Integer PCM",
        "Sample Rate" : '8000',
        "Bit Rate" : "128k",
        "Precision" : "16-bit",
        "Channels" : '1',
        "Duration" : 15
    }
    p = subprocess.Popen(['soxi', f"{filepath}"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode('latin1').split('\n')

    for i in range(len(out)):
        out[i] = out[i].split(':')
        for j in range(len(out[i])):
            out[i][j] = out[i][j].strip(' ')

    statement = ''
    for item in out:
        if item[0] == 'Duration':
            item[1] = float(item[3][:5])
        if item == ['']:
            pass
        elif item[0] not in correct_specs:
            pass
        elif correct_specs[item[0]] == item[1] and item[0] != 'Duration':
            pass
        elif item[0] == 'Duration': 
            if item[1] <= correct_specs['Duration']:
                pass
            else:
                statement += 'Duration too long.\n'
        else:
            statement += f'Have not met requirement: {item[0]}\n'

    return statement


def send_request(filepath, auth_token):
    """
    Returns a json response from AssemblyAI API, 
    including transcribed text from a .wav file.

    Parameters: filepath (str), auth_token (alphanumeric str)
    Returns: response (json)
    """
    headers = {'authorization' : auth_token}

    with open(filepath, 'rb') as f:
        # strip off wav headers
        data = f.read()[44:]

    # encode as base64 bytes, then decode to latin1
    # so that the data is JSON-serialisable
    data = base64.b64encode(data).decode('latin1')
    json_data = {'audio_data': data}

    response = requests.post(
        API_URL+'stream', 
        json = json_data, 
        headers = headers
    )
    return response.json()



if __name__ == "__main__":

    API_URL = "https://api.assemblyai.com/v2/"
    with open('./auth_key.txt','r') as f:
        AUTH_TOKEN = f.readline().rstrip('\n')

    filepath = './output.wav'
    
    # Check file meets requirements:
    check = check_wav_specs(filepath)
    if check != '':
        print(check)
        
    r = send_request(filepath, AUTH_TOKEN)
    # Synchronous transcription is a paid feature...

  
