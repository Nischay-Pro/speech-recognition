import requests
import json
import subprocess
import pyaudio
import wave
import os
import sys
import errno

def read_audio(WAVE_FILENAME):
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio

def RecognizeSpeech(AUDIO_FILENAME, API_ENDPOINT, wit_access_token):

    audio = read_audio(AUDIO_FILENAME)
    headers = {'authorization': 'Bearer ' + wit_access_token,
               'Content-Type': 'audio/mpeg3'}
    resp = requests.post(API_ENDPOINT, headers = headers,
                         data = audio)
    data = json.loads(resp.content)
    text = data
    return text
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total))
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

def main():
    with open('config.json', 'r') as f:
        ARR = json.load(f)
    path = os.path.abspath((ARR)['ffmpegpath'])
    API_ENDPOINT = str((ARR)['auth']['wit.ai']['endpoint'])
    wit_access_token = str((ARR)['auth']['wit.ai']['witaccesstoken'])
    splittime = str((ARR)['split-time'])
    #print(API_ENDPOINT)
    #print(wit_access_token)
    print("Configuration Loaded")
    print("Creating Temporary Directory")
    try:
        os.makedirs("temp")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    print("Created Temporary Directory")
    filepath = os.path.abspath(input("Enter your file path: "))
    print("Generating mp3 audio subparts")
    command = path + " -i " + filepath + " -f segment -segment_time " + splittime + " -c copy temp\\out%04d.mp3"
    subprocess.call(command, shell=True)
    filecount = len(next(os.walk("temp"))[2])
    print(str(filecount) + " files generated")
    print("Beginning Subtitle Generation")
    for i in range(0,filecount + 1):
        text =  RecognizeSpeech(os.path.abspath("temp\\out" + '{0:04d}'.format(i) + ".mp3"),API_ENDPOINT,wit_access_token)
        progress(i,filecount," Transcribe Progress")
        f = open('transcript.txt','a+')
        f.write('\n' + text["_text"])
        f.close()
    progress("Transcribed Successfully")
if __name__ == "__main__":
    print("Loading Configuration")
    main()