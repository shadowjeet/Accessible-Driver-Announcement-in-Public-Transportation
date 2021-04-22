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

#D:\Hioa\Y2 S3\Master Thesis Phase II Codes and Softwares\MTCode_V31\api_key\MasterT-a0d3d0a08dc2.json

credentials = service_account.Credentials.from_service_account_file('D:/MTCode_V31/api_key/MasterT-a0d3d0a08dc2.json')
#def generateSpeechToText():
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






"""
class ThreadClass(QtCore.QThread):
    tick = QtCore.pyqtSignal(str)
    #time = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)
        self.lan_code = ""

    def run(self):
        data = []
        client = speech.SpeechClient(credentials=credentials)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE, language_code=self.lan_code)
        streaming_config = types.StreamingRecognitionConfig(
            config=config, interim_results=True)

        with StreamRecognition(RATE, CHUNK) as stream:
            audio_generator = stream.speech_generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)
            while True:
                fetched_text = strem_recognition_module.print_speech_loop(responses)#does not append text on screen
                data.append(fetched_text)
                finaldata = '.'.join(data)#does append text on screen
                self.tick.emit(fetched_text)
                if re.search(r'\b(terminate|over)\b', fetched_text, re.I):
                    print("Exiting..")
                    break
num_chars = 0

for response in responses:

    if not response.results:
        continue

    result = response.results[0]
    if not result.alternatives:
        continue
    transcript = result.alternatives[0].transcript
    overwrite_chars = '' * (num_chars - len(transcript))

    if not result.is_final:
        sys.stdout.write(transcript + overwrite_chars + '\r')
        sys.stdout.flush()

        num_chars = len(transcript)

    else:
        transcription = transcript + overwrite_chars
        print(transcription)
        self.tick.emit(transcription)"""
