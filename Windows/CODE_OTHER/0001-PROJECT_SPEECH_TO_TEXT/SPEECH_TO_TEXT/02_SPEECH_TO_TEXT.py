import warnings
import pyaudio
import wave
import os
import pyttsx3
import whisper
import numpy as np

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Text-to-speech function
def text_to_speech(message, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(message)
    engine.runAndWait()

# Find specific microphone
def find_microphone():
    microphone_names = ["Microphone (BY Y02)", "USB Audio Device", "Built-in Microphone"]
    audio = pyaudio.PyAudio()
    device_info = None

    try:
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            for mic_name in microphone_names:
                if mic_name.lower() in info.get('name', '').lower():
                    device_info = info
                    break
            if device_info:
                break

        if device_info:
            text_to_speech("Microphone connected. The system is ready to use.") 
            return device_info
        else:
            message = "No predefined microphone found. Please check your device."
            text_to_speech(message)
            return None
    finally:
        audio.terminate()

# Check microphone status
def check_microphone_status(input_device_index=None, threshold=100):
    audio = pyaudio.PyAudio()
    try:
        rate = int(audio.get_device_info_by_index(input_device_index)["defaultSampleRate"])
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=rate,
                            input=True,
                            input_device_index=input_device_index,
                            frames_per_buffer=1024)
        
        data = stream.read(1024, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)

        if np.max(np.abs(audio_data)) > threshold:
            status = True
        else:
            status = False
        
        stream.close()
        return status
    except Exception as e:
        return False
    finally:
        audio.terminate()

# check_speech_presence
def check_speech_presence(input_device_index=None, threshold=400, chunk=1024, duration=None):
    audio = pyaudio.PyAudio()
    try:
        rate = int(audio.get_device_info_by_index(input_device_index)["defaultSampleRate"])
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=rate,
                            input=True,
                            input_device_index=input_device_index,
                            frames_per_buffer=chunk)

        for _ in range(0, int(44100 / chunk * duration)):
            data = stream.read(chunk, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            if np.max(np.abs(audio_data)) > threshold:
                return True  
        return False 
    except Exception as e:
        return False
    finally:
        stream.close()
        audio.terminate()

# Audio recording function
def record_audio(filename="temp_audio.wav", duration=None, chunk=1024, input_device_index=None):
    audio = pyaudio.PyAudio()
    if input_device_index is None:
        input_device_index = audio.get_default_input_device_info()["index"]

    rate = int(audio.get_device_info_by_index(input_device_index)["defaultSampleRate"])
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        input_device_index=input_device_index,
                        frames_per_buffer=chunk)

    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

# Transcribe audio using Whisper
def transcribe_audio(filename, model):
    result = model.transcribe(filename, language="en")
    text = result.get("text", "").strip().lower()
    print(f"Transcribed Text: {text}")  
    os.remove(filename)
    return text

# Save command to .txt file
def save_command_to_file(command, output_file):
    with open(output_file, 'w') as f: 
        f.write(f"{command}\n")

def listen_for_commands(wake_word, model, output_file="command_output.txt", input_device_index=None, duration=2):

    last_microphone_status = True  
    
    while True:
        current_status = check_microphone_status(input_device_index=input_device_index)
        
        if not current_status:
            if last_microphone_status:
                text_to_speech("Microphone is not ready or no sound detected. Please check your microphone.")
            last_microphone_status = False
            continue 
        else:
            if not last_microphone_status:
                text_to_speech("Microphone is now ready.")
            last_microphone_status = True

        if not check_speech_presence(input_device_index=input_device_index, duration=1):
            continue  

        # Record short audio clip for the specified duration
        record_audio(duration=duration, input_device_index=input_device_index)
        audio_text = transcribe_audio("temp_audio.wav", model)

        # Check for wake word
        if wake_word in audio_text:
            response = f"Yse sir!. I'm ready for your command."
            text_to_speech(response)

            while True:
                # Listen for command
                record_audio(duration=duration, input_device_index=input_device_index)
                command_text = transcribe_audio("temp_audio.wav", model)

                # Check for specific commands
                if "turn on" in command_text:
                    response = "Turning on the system."
                    text_to_speech(response)
                    save_command_to_file("turn on", output_file)
                    break  

                elif "turn off" in command_text:
                    response = "Turning off the system."
                    text_to_speech(response)
                    save_command_to_file("turn off", output_file)
                    break  

                else:
                    response = "Sorry! Command not recognized. Please try again."
                    text_to_speech(response)
        else:
            response = "Sorry!. Please say it again."
            text_to_speech(response)

# Load Whisper model
whisper_model = whisper.load_model("small")

# Find microphone
mic_info = find_microphone()
if mic_info:
    listen_for_commands(wake_word="computer", model=whisper_model, input_device_index=mic_info["index"])
else:
    text_to_speech("No suitable microphone found. Please check your device settings.")
    print("No microphone found. Exiting program.")