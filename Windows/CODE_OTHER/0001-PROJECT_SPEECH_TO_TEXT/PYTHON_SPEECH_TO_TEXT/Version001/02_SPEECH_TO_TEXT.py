import warnings
import pyaudio
import wave
import os
import pyttsx3
import whisper
import numpy as np
import time

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Text-to-speech function
def text_to_speech(message, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(message)
    engine.runAndWait()

# Save microphone names to a .txt file
def save_microphone_names_to_txt(names, filename="microphone_names.txt"):
    with open(filename, 'w') as file:
        for name in names:
            file.write(f"{name}\n")

# Load microphone names from a .txt file or reset to default
def load_microphone_names_from_txt(filename="microphone_names.txt"):
    default_microphone_names = []
    try:
        with open(filename, 'r') as file:
            # Read lines and strip newline characters
            names = [line.strip() for line in file.readlines()]
            if not names:  # If file exists but is empty
                print("Microphone list is empty. Resetting to default names.")
                save_microphone_names_to_txt(default_microphone_names, filename)
                return default_microphone_names
            return names
    except FileNotFoundError:
        # If file doesn't exist, create it with default names
        print(f"No microphone names file found. Creating {filename} with default names.")
        save_microphone_names_to_txt(default_microphone_names, filename)
        return default_microphone_names

def find_or_select_microphone():
    global microphone_names
    microphone_names = load_microphone_names_from_txt()  # Load names from .txt
    audio = pyaudio.PyAudio()
    device_info = None

    try:
        # Check if predefined microphones exist
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            for mic_name in microphone_names:
                if mic_name.lower() in info.get('name', '').lower():
                    device_info = info
                    break
            if device_info:
                break

        if not device_info:  # If no predefined microphone is found
            print("No predefined microphone found. Searching for available microphones...")
            text_to_speech("No predefined microphone found. Please select a microphone.")

            available_microphones = []
            for i in range(audio.get_device_count()):
                info = audio.get_device_info_by_index(i)
                if info.get('maxInputChannels', 0) > 0:
                    available_microphones.append((i, info.get('name', 'Unknown')))

            if not available_microphones:
                text_to_speech("No microphones available. Please check your device.")
                return None

            # List available microphones
            print("Available Microphones:")
            for index, (i, name) in enumerate(available_microphones):
                print(f"{index + 1}. {name}")

            # User selects a microphone
            while True:
                try:
                    choice = int(input("Select a microphone by number: ")) - 1
                    if 0 <= choice < len(available_microphones):
                        selected_index, selected_name = available_microphones[choice]
                        text_to_speech(f"You selected {selected_name}. Saving this microphone.")
                        if selected_name not in microphone_names:
                            microphone_names.append(selected_name)  # Add name to the list
                            save_microphone_names_to_txt(microphone_names)  # Save updated names to .txt
                        device_info = audio.get_device_info_by_index(selected_index)
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

        if device_info:
            text_to_speech("Microphone connected. The system is ready to use.")
            return device_info
        else:
            text_to_speech("No suitable microphone found.")
            return None
    finally:
        audio.terminate()

# Check microphone status with separate audio file saving
def check_microphone_status(input_device_index=None, threshold=10, filename="mic_status.wav"):
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
        
        # Save audio to file
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(data)
        
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

# Check speech presence with separate audio file saving
def check_speech_presence(input_device_index=None, threshold=2000, chunk=1024, duration=None, filename="speech_presence.wav"):
    audio = pyaudio.PyAudio()
    try:
        rate = int(audio.get_device_info_by_index(input_device_index)["defaultSampleRate"])
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=rate,
                            input=True,
                            input_device_index=input_device_index,
                            frames_per_buffer=chunk)
        
        frames = []
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.int16)
            if np.max(np.abs(audio_data)) > threshold:
                speech_detected = True
                break
        else:
            speech_detected = False
        
        # Save audio to file
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        
        stream.close()
        return speech_detected
    except Exception as e:
        return False
    finally:
        stream.close()
        audio.terminate()

# Audio recording function with dynamic filename
def record_audio(filename="recorded_audio.wav", duration=None, chunk=1024, input_device_index=None):
    print(f"Record audio")
    filename = os.path.abspath(filename)  

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

    # บันทึกไฟล์เสียง
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def transcribe_audio(filename, model):
    filename = os.path.abspath(filename)  
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Audio file not found: {filename}") 
    result = model.transcribe(filename, language="en")
    text = result.get("text", "").strip().lower()
    print(f"Transcribed Text: {text}")  
    return text

# Save command to .txt file
def save_command_to_file(command, output_file):
    with open(output_file, 'w') as f: 
        f.write(f"{command}\n")

def listen_for_commands(wake_word, model, output_file="command_output.txt", input_device_index=None, duration=2, command_timeout=30):
    last_microphone_status = True  
    command_start_time = None 

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
        audio_text = transcribe_audio("recorded_audio.wav", model)

        # Check for wake word
        if wake_word in audio_text:
            response = f"Yes sir!."
            text_to_speech(response)

            command_start_time = time.time() 

            while True:
                elapsed_time = time.time() - command_start_time
                if elapsed_time > command_timeout:
                    text_to_speech("Timeout. No command received.")
                    break 

                if not check_speech_presence(input_device_index=input_device_index, duration=1):
                    continue  
                
                # Listen for command
                record_audio(duration=duration, input_device_index=input_device_index)
                command_text = transcribe_audio("recorded_audio.wav", model)

                # Check for specific commands
                if "turn on" in command_text:
                    response = "turn on the system."
                    text_to_speech(response)
                    save_command_to_file("turn on", output_file)
                    break  

                elif "turn off" in command_text:
                    response = "turn off the system."
                    text_to_speech(response)
                    save_command_to_file("turn off", output_file)
                    break  

                elif "hold on" in command_text:
                    response = "Hold on the system."
                    text_to_speech(response)
                    save_command_to_file("Hold", output_file)
                    break  

                else:
                    response = "Sorry! Please try again."
                    text_to_speech(response)
        else:
            response = "Sorry! Please say it again."
            text_to_speech(response)

# Load Whisper model
whisper_model = whisper.load_model("medium.en")

# Find microphone
mic_info = find_or_select_microphone()
if mic_info:
    listen_for_commands(wake_word="computer", model=whisper_model, input_device_index=mic_info["index"])
else:
    text_to_speech("No suitable microphone found. Please check your device settings.")
    print("No microphone found. Exiting program.")