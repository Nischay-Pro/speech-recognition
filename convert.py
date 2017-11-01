import subprocess
import os
import json


def main():
    try:
        with open('config.json', 'r') as f:
            ARR = json.load(f)
        # lossy = (ARR)['lossy']
        path = os.path.abspath((ARR)['ffmpegpath'])
        filename = os.path.abspath(input("Enter File Path: "))
        if((ARR)['lossy']==True):
            targetformat = "mp3"
        else:
            targetformat = "flac"
        bitrate = str((ARR)['parameter'][targetformat]['bitrate'])
        channels = str((ARR)['parameter'][targetformat]['numchannels'])
        samplerate = str((ARR)['parameter'][targetformat]['samplerate'])
        dumppath = str((ARR)['dumppath'])
        loglevel = " -loglevel " + str((ARR)['loglevel']) + " -stats"
        command = path + " -i " + filename + loglevel + " -ab " + bitrate + " -ac " + channels + " -ar " + samplerate + " -vn " + dumppath + "\output." + targetformat
        #command = path + "\\bin\\ffmpeg.exe -i dump\\012.mp4 -r 60 -s 1920x1080 -f image2 images\\foo-%03d.png"
        #command = path + "\\bin\\ffmpeg.exe -f image2 -framerate 60 -i images\\foo-%03d.png -s 1920x1080 foo.avi"
        #print(filename)
        #command = path + " -i dump\\sa.mp3 -f segment -segment_time 5 -c copy out%03d.mp3"
        subprocess.call(command, shell=True)
    except KeyError:
        print("Configuration JSON file error")

if __name__ == "__main__":
    main()