import sounddevice as sd
import os
import numpy as np
from scipy.io.wavfile import write
import whisper
import warnings
import time

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def text_to_speech_pico(message, output_file="pico_output.wav"):
    try:
        # สร้างไฟล์เสียงจากข้อความ
        command = f'pico2wave -w={output_file} "{message}"'
        os.system(command)

        # เล่นไฟล์เสียงที่สร้าง
        os.system(f'aplay {output_file} > /dev/null 2>&1')
    except Exception as e:
        print(f"Error using Pico TTS: {e}")

def save_microphone_names_to_txt(names, filename="microphone_names.txt"):
    try:
        with open(filename, 'w') as file:
            for name in names:
                file.write(f"{name}\n")
    except Exception as e:
        print(f"Error saving microphone names: {e}")

def load_microphone_names_from_txt(filename="microphone_names.txt"):
    if not os.path.exists(filename):
        save_microphone_names_to_txt([], filename)
        return []  # Return empty list if file doesn't exist

    try:
        with open(filename, 'r') as file:
            names = [line.strip() for line in file.readlines()]
            return names if names else []
    except Exception as e:
        print(f"Error loading microphone names: {e}")
        return []

def find_or_select_microphone():
    try:
        saved_mic_names = load_microphone_names_from_txt()
        devices = sd.query_devices()
        input_devices = [
            {"index": idx, "name": dev["name"], "rate": dev["default_samplerate"], "channels": dev["max_input_channels"]}
            for idx, dev in enumerate(devices)
            if dev["max_input_channels"] > 0
        ]

        if not input_devices:
            text_to_speech_pico("No available input devices found. Please check your microphone.")
            return None

        for saved_name in saved_mic_names:
            for device in input_devices:
                if device["name"] == saved_name:
                    text_to_speech_pico(f"Microphone {device['name']} is connected and ready.")
                    return device

        print("Please select a microphone:")
        for idx, device in enumerate(input_devices):
            print(f"{idx + 1}. {device['name']}")

        while True:
            try:
                choice = int(input("Select a microphone by number: ")) - 1
                if 0 <= choice < len(input_devices):
                    selected_device = input_devices[choice]
                    save_microphone_names_to_txt([selected_device["name"]])
                    text_to_speech_pico(f"Microphone {selected_device['name']} is connected and ready.")
                    return selected_device
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except Exception as e:
        text_to_speech_pico(f"Error finding or selecting microphone. {e}")
        return None

def check_microphone_status(mic_info, threshold=100, duration=1):
    try:
        samplerate = int(mic_info['rate'])
        channels = mic_info['channels']
        device_index = mic_info['index']

        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16', device=device_index)
        sd.wait()
        audio_data = audio_data.flatten()

        return np.max(np.abs(audio_data)) > threshold
    except Exception as e:
        return False

def check_speech_presence(mic_info, threshold=2000, duration=1):
    try:
        samplerate = int(mic_info['rate'])
        channels = mic_info['channels']
        device_index = mic_info['index']

        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16', device=device_index)
        sd.wait()
        audio_data = audio_data.flatten()

        return np.max(np.abs(audio_data)) > threshold
    except Exception as e:
        return False

def transcribe_audio(filename, model):
    if not os.path.exists(filename):
        print("Error: Audio file not found.")
        return ""
    try:
        print("Transcribing audio...")
        result = model.transcribe(filename, language="en")
        text = result.get("text", "").strip().lower()  
        print(f"Transcription result: {text}") 
        return text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

def record_audio(filename="temp_audio.wav", duration=2, mic_info=None):
    try:
        if not mic_info:
            return
        samplerate = int(mic_info['rate'])
        channels = mic_info['channels']
        device_index = mic_info['index']

        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16', device=device_index)
        sd.wait()
        write(filename, samplerate, audio_data)
    except Exception as e:
        pass

def save_command_to_file(command, output_file):
    try:
        with open(output_file, 'a') as f:
            f.write(f"{command}\n")
    except Exception as e:
        pass

def listen_for_commands(wake_word, model, mic_info, output_file="command_output.txt", duration=2, command_timeout=60):
    last_microphone_status = True
    command_start_time = None

    print("Listening for wake word...")  # แจ้งสถานะเริ่มต้น
    while True:
        # Check for microphone status
        if not check_microphone_status(mic_info=mic_info): 
            if last_microphone_status:
                text_to_speech_pico("Microphone is not ready or no sound detected. Please check your microphone.")
            last_microphone_status = False
            continue
        else:
            if not last_microphone_status:
                text_to_speech_pico("Microphone is now ready.")
            last_microphone_status = True

        # Check for speech presence
        if not check_speech_presence(mic_info=mic_info):  
            continue

        # Record audio and transcribe for wake word detection
        print("Recording audio for wake word...")
        record_audio(filename="temp_audio.wav", duration=duration, mic_info=mic_info)

        # แปลงเสียงเป็นข้อความ
        audio_text = transcribe_audio("temp_audio.wav", model)

        if wake_word in audio_text.lower():
            print(f"Wake word detected: {audio_text}")
            text_to_speech_pico("Yes sir! I'm ready for your command.")
            command_start_time = time.time()

            print("Listening for commands...")
            while True:
                if time.time() - command_start_time > command_timeout:
                    text_to_speech_pico("Timeout. No command received.")
                    break

                if not check_speech_presence(mic_info=mic_info):
                    continue

                print("Recording audio for command...")
                record_audio(filename="temp_audio.wav", duration=duration, mic_info=mic_info)
                command_text = transcribe_audio("temp_audio.wav", model)

                if "start" in command_text:
                    print("Command received: Start")
                    text_to_speech_pico("Starting the system.")
                    save_command_to_file("Start", output_file)
                    break

                elif "stop" in command_text:
                    print("Command received: Stop")
                    text_to_speech_pico("Stopping the system.")
                    save_command_to_file("Stop", output_file)
                    break

                elif "hold on" in command_text:
                    print("Command received: Hold on")
                    text_to_speech_pico("Holding the system.")
                    save_command_to_file("Hold", output_file)
                    break

                else:
                    print(f"Unrecognized command: {command_text}")
                    text_to_speech_pico("Unrecognized command. Please try again.")

def main():
    try:
        # Load Whisper model
        print("Loading Whisper model...")
        whisper_model = whisper.load_model("tiny")
        print("Whisper model loaded successfully.")

        # Select a microphone
        selected_mic = find_or_select_microphone()
        if not selected_mic:
            text_to_speech_pico("No suitable microphone found. Please check your device.")
            return
        
        # Start listening for commands
        listen_for_commands(wake_word="computer", model=whisper_model, mic_info=selected_mic)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass

if __name__ == "__main__":
    main()