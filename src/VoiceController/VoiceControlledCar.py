import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

#{0.0.1.00000000}.{74BCE343-438F-42AE-9591-13B2943607EA}

def speech_to_text(api_key, region):
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language = "en-IN"
    audio_config = speechsdk.audio.AudioConfig(device_name = '{0.0.1.00000000}.{74BCE343-438F-42AE-9591-13B2943607EA}') #leave blank for default 
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "3000")
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "50")


    print("Speak Now.")
    while True:
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognised: {}" .format(speech_recognition_result.text))
            if "stop session" in speech_recognition_result.text.lower():
                print("Session ended.")
                break

        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("Couldnt recognise speech")
        
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition cancelled: {}".format(cancellation_details.reason))

load_dotenv()

api_key = 'Enter api key' #os.getenv("api_key")
region = 'Enter  Region' #os.getenv("region")

speech_to_text(api_key, region)