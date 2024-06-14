import socket
import re
import struct
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import keyboard
import threading

esp32_ip ='192.168.138.27'              #192.168.235.27  
esp32_port = 80

esp32_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
esp32_socket.connect((esp32_ip, esp32_port))

is_q_pressed = False

def extract_numbers(text):
    number_pattern = r'\d+'
    numbers = re.findall(number_pattern, text)
    return numbers

def speech_to_text(api_key, region):
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language = "en-IN"
    audio_config = speechsdk.audio.AudioConfig(device_name = '{0.0.1.00000000}.{74BCE343-438F-42AE-9591-13B2943607EA}') #leave blank for default settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "3000")
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "5")

    print("Speak Now.")
    while is_q_pressed:
        data = 0
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognised: {}" .format(speech_recognition_result.text))
            if "stop session" in speech_recognition_result.text.lower():
                print("Session ended.")
                break
            elif "turn right" in speech_recognition_result.text.lower() and "degrees" in speech_recognition_result.text.lower():
                numbers = extract_numbers(speech_recognition_result.text)
                print(numbers)
                data = struct.pack('2B', 1, int(numbers[0]))
                esp32_socket.sendall(data)
            elif "turn left" in speech_recognition_result.text.lower() and "degrees" in speech_recognition_result.text.lower():
                numbers = extract_numbers(speech_recognition_result.text)
                print(numbers)
                data = struct.pack('2B', 2, int(numbers[0]))
                esp32_socket.sendall(data)
            elif "go forward" in speech_recognition_result.text.lower():
                data = struct.pack('2B', 3, 0)
                esp32_socket.sendall(data)
            elif "stop" in speech_recognition_result.text.lower():
                data = struct.pack('2B', 4, 0)
                esp32_socket.sendall(data)
            elif "comeback" in speech_recognition_result.text.lower() or "come back" in speech_recognition_result.text.lower():
                data = struct.pack('2B', 5, 0)
                esp32_socket.sendall(data)



        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("Couldnt recognise speech")
        
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition cancelled: {}".format(cancellation_details.reason))
    

load_dotenv()

api_key = '<enter api key>' #os.getenv("api_key")
region = '<enter region>' #os.getenv("region")


def perform_task():
    global is_q_pressed
    while is_q_pressed:
        #print("Hello")
        speech_to_text(api_key, region)

def on_q_press_event(event):
    global is_q_pressed
    if event.name == 'q' and event.event_type == 'down':
        if not is_q_pressed:
            is_q_pressed = True
            threading.Thread(target=perform_task).start()
    elif event.name == 'q' and event.event_type == 'up':
        is_q_pressed = False

keyboard.hook(on_q_press_event)

print("Press 'q' to perform the task. Press 'esc' to exit.")
keyboard.wait('esc')



