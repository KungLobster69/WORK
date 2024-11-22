import sounddevice as sd
import os
import numpy as np
from scipy.io.wavfile import write
import whisper
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def text_to_speech(message):
    try:
        # ใช้คำสั่ง echo และ pipe ไปยัง festival
        os.system(f'echo "{message}" | festival --tts')
    except Exception as e:
        print(f"Error in Text-to-Speech using Festival: {e}")

def save_microphone_names_to_txt(names, filename="microphone_names.txt"):
    try:
        with open(filename, 'w') as file:
            for name in names:
                file.write(f"{name}\n")
        print(f"Microphone names saved to {filename}.")
    except Exception as e:
        print(f"Error saving microphone names: {e}")

def load_microphone_names_from_txt(filename="microphone_names.txt"):
    if not os.path.exists(filename):
        print(f"No microphone names file found. Creating {filename} with default names.")
        save_microphone_names_to_txt([], filename)
        return []  # Return empty list if file doesn't exist

    try:
        with open(filename, 'r') as file:
            names = [line.strip() for line in file.readlines()]
            if not names:  # If file exists but is empty
                print("Microphone list is empty. Resetting to default names.")
                save_microphone_names_to_txt([], filename)
                return []
            return names
    except Exception as e:
        print(f"Error loading microphone names: {e}")
        return []

def find_or_select_microphone():
    try:
        # Get available audio input devices
        devices = sd.query_devices()
        input_devices = [dev for dev in devices if dev['max_input_channels'] > 0]

        if not input_devices:
            print("No available input devices found.")
            return None

        # List available input devices
        print("Available Input Devices:")
        for idx, device in enumerate(input_devices):
            print(f"{idx + 1}. {device['name']}")

        # Prompt user to select a device
        while True:
            try:
                choice = int(input("Select a microphone by number: ")) - 1
                if 0 <= choice < len(input_devices):
                    selected_device = input_devices[choice]
                    print(f"Selected microphone: {selected_device['name']}")
                    return selected_device
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    except Exception as e:
        print(f"Error finding/selecting microphone: {e}")
        return None

def check_microphone_status(input_device_index=None, threshold=100, duration=1, samplerate=44100):
    try:
        # Capture audio from the specified microphone
        audio_data = sd.rec(int(samplerate * duration), 
                            samplerate=samplerate, 
                            channels=1, 
                            dtype='int16', 
                            device=input_device_index)
        sd.wait()  # Wait for the recording to finish
        audio_data = audio_data.flatten()  # Flatten to 1D array

        # Check if the maximum amplitude exceeds the threshold
        if np.max(np.abs(audio_data)) > threshold:
            return True
        return False
    except Exception as e:
        print(f"Error checking microphone status: {e}")
        return False
    
def check_speech_presence(input_device_index=None, threshold=2000, chunk=1024, duration=1, samplerate=44100):
    try:
        print(f"Checking for speech presence (threshold={threshold})...")
        
        # Record audio for the specified duration
        audio_data = sd.rec(int(samplerate * duration), 
                            samplerate=samplerate, 
                            channels=1, 
                            dtype='int16', 
                            device=input_device_index)
        sd.wait()  # Wait for the recording to complete
        
        # Flatten audio data and check for speech
        audio_data = audio_data.flatten()
        if np.max(np.abs(audio_data)) > threshold:
            print("Speech detected.")
            return True
        print("No speech detected.")
        return False
    except Exception as e:
        print(f"Error checking speech presence: {e}")
        return False

def record_audio(filename="temp_audio.wav", duration=5, samplerate=44100, input_device_index=None):
    try:
        print(f"Recording audio for {duration} seconds...")
        # Record audio
        audio_data = sd.rec(int(samplerate * duration), 
                            samplerate=samplerate, 
                            channels=1, 
                            dtype='int16', 
                            device=input_device_index)
        sd.wait()  # Wait for the recording to finish
        
        # Save the recorded audio as a WAV file
        write(filename, samplerate, audio_data)
        print(f"Audio saved to {filename}")
    except Exception as e:
        print(f"Error recording audio: {e}")

def transcribe_audio(filename, model):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return ""

    try:
        print(f"Transcribing audio from '{filename}'...")
        result = model.transcribe(filename, language="en")
        text = result.get("text", "").strip()
        print(f"Transcribed Text: {text}")
        return text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

def save_command_to_file(command, output_file):
    try:
        with open(output_file, 'a') as f:  # Open in append mode
            f.write(f"{command}\n")
        print(f"Command '{command}' saved to '{output_file}'.")
    except Exception as e:
        print(f"Error saving command to file: {e}")

def listen_for_commands(wake_word, model, output_file="command_output.txt", input_device_index=None, duration=2, command_timeout=30):
    last_microphone_status = True
    command_start_time = None

    while True:
        # Check for microphone status
        if not check_microphone_status(input_device_index=input_device_index):
            if last_microphone_status:
                print("Microphone is not ready or no sound detected. Please check your microphone.")
                text_to_speech("Microphone is not ready or no sound detected. Please check your microphone.")
            last_microphone_status = False
            continue
        else:
            if not last_microphone_status:
                print("Microphone is now ready.")
                text_to_speech("Microphone is now ready.")
            last_microphone_status = True

        # Check for speech presence
        if not check_speech_presence(input_device_index=input_device_index, duration=1):
            continue

        # Record audio and transcribe for wake word detection
        print("Listening for wake word...")
        record_audio(filename="temp_audio.wav", duration=duration, input_device_index=input_device_index)
        audio_text = transcribe_audio("temp_audio.wav", model)

        if wake_word in audio_text.lower():
            print("Wake word detected.")
            text_to_speech(f"Yes sir! I'm ready for your command.")
            command_start_time = time.time()

            while True:
                elapsed_time = time.time() - command_start_time
                if elapsed_time > command_timeout:
                    print("Timeout. No command received.")
                    text_to_speech("Timeout. No command received.")
                    break

                if not check_speech_presence(input_device_index=input_device_index, duration=1):
                    continue

                # Record command audio
                print("Listening for command...")
                record_audio(filename="temp_audio.wav", duration=duration, input_device_index=input_device_index)
                command_text = transcribe_audio("temp_audio.wav", model)

                # Check for specific commands
                if "start" in command_text:
                    print("Command: Start")
                    text_to_speech("Starting the system.")
                    save_command_to_file("Start", output_file)
                    break

                elif "stop" in command_text:
                    print("Command: Stop")
                    text_to_speech("Stopping the system.")
                    save_command_to_file("Stop", output_file)
                    break

                elif "hold on" in command_text:
                    print("Command: Hold on")
                    text_to_speech("Holding the system.")
                    save_command_to_file("Hold", output_file)
                    break

                else:
                    print("Unrecognized command. Please try again.")
                    text_to_speech("Unrecognized command. Please try again.")
        else:
            print("Wake word not detected. Listening again.")
            text_to_speech("Sorry! Please say it again.")

def main():
    try:
        # Load Whisper model
        print("Loading Whisper model...")
        whisper_model = whisper.load_model("tiny")
        print("Whisper model loaded successfully.")

        # Select a microphone
        print("Finding available microphones...")
        mic_info = find_or_select_microphone()
        if not mic_info:
            text_to_speech("No suitable microphone found. Please check your device.")
            print("No microphone found. Exiting program.")
            return

        # Start listening for commands
        print("Starting voice command system...")
        listen_for_commands(wake_word="computer",
                            model=whisper_model,
                            input_device_index=mic_info['index'],
                            output_file="command_output.txt",
                            duration=2,
                            command_timeout=30)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()