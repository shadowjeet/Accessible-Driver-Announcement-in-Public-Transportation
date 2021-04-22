from __future__ import division

import sys
from google.oauth2 import service_account

RATE = 16000
CHUNK = int(RATE/10)
#D:/Hioa/Y2 S3/Master Thesis Phase II Codes and Softwares/MTCode_V31/api_key/MasterT-a0d3d0a08dc2.json
#credentials = service_account.Credentials.from_service_account_file('D:/Hioa/Y2 S3/Master Thesis Phase II Codes and Softwares/MTCode_V31/api_key/MasterT-a0d3d0a08dc2.json')

def print_speech_loop(responses):
    num_chars = 0
    for response in responses:

        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        overwrite_chars = '' * (num_chars - len(transcript))

        for word_info in result.alternatives[0].words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time



        if not result.is_final:
            #sys.stdout.write(transcript + overwrite_chars + '\r')
            #sys.stdout.flush()
            num_chars = len(transcript)

        else:
            transcription = transcript + overwrite_chars
            return transcription


