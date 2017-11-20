import requests
import json
import subprocess
import pyaudio
import wave
import os
import sys
import errno
import shutil

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

def stringifytime(seconds,milliseconds=0,ffmpeg=False):
    #print(seconds)
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    if(seconds==0):
        if(ffmpeg == False):
            return "00:00:00," + '{:<03d}'.format(milliseconds)
        else:
            return "00:00:00." + '{:<03d}'.format(milliseconds)
    else:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if(ffmpeg == False):
            return "%02d:%02d:%02d," % (h, m, s) + '{:<03d}'.format(milliseconds)
        else:
            return "%02d:%02d:%02d." % (h, m, s) + '{:<03d}'.format(milliseconds)

def subtitlify(text,count, starttime,endtime):
    if("error" in text):
        return str(int(count)) + "\n" + starttime + " --> " + endtime + "\n" + ""
    else:
        return str(int(count)) + "\n" + starttime + " --> " + endtime + "\n" + text["_text"] + "\n"

def main():
    with open('config.json', 'r') as f:
        ARR = json.load(f)
    path = os.path.abspath((ARR)['ffmpegpath'])
    API_ENDPOINT = str((ARR)['auth']['wit.ai']['endpoint'])
    wit_access_token = str((ARR)['auth']['wit.ai']['witaccesstoken'])
    splittime = input("Enter Speech Range JSON file path: ")
    with open(splittime, 'r') as f:
        splittime = json.load(f)
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
    idval = 0
    for item in splittime:
        start_time = stringifytime(str(item['speech_begin']).split(".")[0],str(item['speech_begin']).split(".")[1],True)
        end_time = stringifytime(str(item['speech_end']).split(".")[0],str(item['speech_end']).split(".")[1],True)
        print(start_time)
        print(end_time)
        print("next")
        command = path + " -i " + filepath + " -ss " + start_time  + " -to " + end_time + " -c copy temp\\out" + '{0:04d}'.format(idval) + ".mp3"
        subprocess.call(command, shell=True)
        idval += 1
    filecount = len(next(os.walk("temp"))[2])
    print(str(filecount) + " files generated")
    print("Beginning Subtitle Generation")
    for i in range(0,filecount + 1):
        text =  RecognizeSpeech(os.path.abspath("temp\\out" + '{0:04d}'.format(i) + ".mp3"),API_ENDPOINT,wit_access_token)
        progress(i,filecount," Transcribe Progress")
        f = open('transcript.srt','a+')
        #print(text)
        #print(i + 1, text["_text"], int(splittime))
        try:
            start_time = stringifytime(str(splittime[i]['speech_begin']).split(".")[0],str(splittime[i]['speech_begin']).split(".")[1],True)
            end_time = stringifytime(str(splittime[i]['speech_end']).split(".")[0],str(splittime[i]['speech_end']).split(".")[1],True)
            texttowrite = subtitlify(text, i + 1, start_time,end_time)
        except KeyError as exception:
            print(text)
            raise  
        if(i == 0):
            f.write(texttowrite)
        else:
            f.write('\n' + texttowrite)
        f.close()
    print("Cleaning up Temporary Folder")
    shutil.rmtree("temp", ignore_errors=False, onerror=None)
    print("Transcribed Successfully")

if __name__ == "__main__":
    print("Loading Configuration")
    main()