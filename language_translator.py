from google.oauth2 import service_account
from google.cloud import translate
import sys
# client = speech.SpeechClient(credentials=credentials)

credentials = service_account.Credentials.from_service_account_file('D:/MTCode_V31/api_key/translatorApi.json')

translate_client = translate.Client(credentials=credentials)

# Example Scenario
# text = "This metro and the station are now being evacuated please leave the metro now and follow staffs instruction to exit the stations"
# target = 'no' - Translating to norwegian language 

def translator(text, target):

    translation = translate_client.translate(
        text,
        target_language=target
        )
    data = translation['translatedText']
    return data

def universal(text):
    spDict = {'å': "&aring;", 'ø': "&oslash;", 'æ': "&aelig;"}
    for char in spDict:
        replaced = text.replace(char, spDict[char])
        text = replaced
    return text




