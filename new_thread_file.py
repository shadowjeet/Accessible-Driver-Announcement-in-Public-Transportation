from __future__ import division
import sys
import strem_recognition_module
import language_translator as lt
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from google.cloud import speech_v1 as speech
# from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types
from google.oauth2 import service_account

from stream_recognition_class import StreamRecognition
import time

start = time.time()
lan_code = sys.argv[1]
translator_code = sys.argv[2]
RATE = 16000
CHUNK = int(RATE/10)



credentials = service_account.Credentials.from_service_account_file('Location of API Key File')

data = []
client = speech.SpeechClient(credentials=credentials)
config = types.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE, language_code=lan_code)
streaming_config = types.StreamingRecognitionConfig(
    config=config, interim_results=True)

with StreamRecognition(RATE, CHUNK) as stream:
    audio_generator = stream.speech_generator()
    requests = (types.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator)

    responses = client.streaming_recognize(streaming_config, requests)

    end = (time.time() - start) - 10
    formatted_time = "{:.2f}".format(end)
    while True:
        fetched_text = strem_recognition_module.print_speech_loop(responses)#does not append text on screen
        data.append(fetched_text)
        recognized_text = ''.join(data)#does append text on screen
        finaldata = lt.translator(recognized_text, translator_code)

        universal_data = lt.universal(recognized_text+"++ "+finaldata)


        if re.search(r'\b(terminate|over)\b', fetched_text, re.I):
            break
        print(universal_data)
        #print(recognized_text)
        sys.stdout.flush()
