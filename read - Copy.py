import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()
file_name = os.path.abspath(input("Enter File Path you want to transcribe: "))
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US')
response = client.recognize(config, audio)
alternatives = response.results[0].alternatives
for alternative in alternatives:
    print('Transcript: {}'.format(alternative.transcript))