import requests
import json
import pyaudio
import wave


API_ENDPOINT = 'https://api.wit.ai/speech'

wit_access_token = 'S4OWJR36ESNBDLNEMPTUEORMEVZWRSX7'

def read_audio(WAVE_FILENAME):
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio

def RecognizeSpeech(AUDIO_FILENAME):
    
    # reading audio
	
    audio = read_audio(AUDIO_FILENAME)
    
    # defining headers for HTTP request
    headers = {'authorization': 'Bearer ' + wit_access_token,
               'Content-Type': 'audio/mpeg3'}

    # making an HTTP post request
    resp = requests.post(API_ENDPOINT, headers = headers,
                         data = audio)
    
    # converting response content to JSON format
    data = json.loads(resp.content)
    
    # get text from data
    text = data
    
    # return the text
    return text

if __name__ == "__main__":
    text =  RecognizeSpeech(input("Enter your file path: "))
    #text =  RecognizeSpeech("C:\\Users\\Nisch\\Desktop\\speech-recog\\bin\\out" + '{0:03d}'.format(i) + ".mp3")
    f = open('transcript.txt','a+')
    f.write('\n' + text["_text"])
    f.close()
    print("Done")