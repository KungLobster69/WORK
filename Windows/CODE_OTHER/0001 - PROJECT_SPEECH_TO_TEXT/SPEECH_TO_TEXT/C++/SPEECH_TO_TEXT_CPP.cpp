#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include "whisper.h" 
#include <portaudio.h>
#include <sndfile.h>

// Function to execute shell commands
void executeCommand(const std::string &command) {
    system(command.c_str());
}

// Function to convert text to speech using pico2wave
void textToSpeechPico(const std::string &message, const std::string &outputFile = "pico_output.wav") {
    try {
        std::string command = "pico2wave -w=" + outputFile + " \"" + message + "\"";
        executeCommand(command);
        executeCommand("aplay " + outputFile + " > /dev/null 2>&1");
    } catch (const std::exception &e) {
        std::cerr << "Error using Pico TTS: " << e.what() << std::endl;
    }
}

// Function to save microphone names to a file
void saveMicrophoneNamesToTxt(const std::vector<std::string> &names, const std::string &filename = "microphone_names.txt") {
    try {
        std::ofstream file(filename);
        if (file.is_open()) {
            for (const auto &name : names) {
                file << name << std::endl;
            }
        }
    } catch (const std::exception &e) {
        std::cerr << "Error saving microphone names: " << e.what() << std::endl;
    }
}

// Function to load microphone names from a file
std::vector<std::string> loadMicrophoneNamesFromTxt(const std::string &filename = "microphone_names.txt") {
    std::vector<std::string> names;
    try {
        std::ifstream file(filename);
        if (file.is_open()) {
            std::string line;
            while (std::getline(file, line)) {
                names.push_back(line);
            }
        }
    } catch (const std::exception &e) {
        std::cerr << "Error loading microphone names: " << e.what() << std::endl;
    }
    return names;
}

// Function to initialize PortAudio and find/select a microphone
PaDeviceIndex findOrSelectMicrophone() {
    Pa_Initialize();
    int numDevices = Pa_GetDeviceCount();
    if (numDevices < 0) {
        std::cerr << "No audio devices found." << std::endl;
        return paNoDevice;
    }

    std::vector<std::string> savedMicNames = loadMicrophoneNamesFromTxt();
    std::vector<std::pair<PaDeviceIndex, const PaDeviceInfo *>> inputDevices;

    for (PaDeviceIndex i = 0; i < numDevices; ++i) {
        const PaDeviceInfo *deviceInfo = Pa_GetDeviceInfo(i);
        if (deviceInfo->maxInputChannels > 0) {
            inputDevices.emplace_back(i, deviceInfo);
        }
    }

    if (inputDevices.empty()) {
        textToSpeechPico("No available input devices found. Please check your microphone.");
        return paNoDevice;
    }

    for (const auto &savedName : savedMicNames) {
        for (const auto &[index, device] : inputDevices) {
            if (savedName == device->name) {
                textToSpeechPico("Microphone " + std::string(device->name) + " is connected and ready.");
                return index;
            }
        }
    }

    std::cout << "Please select a microphone:" << std::endl;
    for (size_t i = 0; i < inputDevices.size(); ++i) {
        std::cout << i + 1 << ". " << inputDevices[i].second->name << std::endl;
    }

    int choice;
    while (true) {
        std::cin >> choice;
        if (choice > 0 && choice <= static_cast<int>(inputDevices.size())) {
            const auto &[index, device] = inputDevices[choice - 1];
            saveMicrophoneNamesToTxt({device->name});
            textToSpeechPico("Microphone " + std::string(device->name) + " is connected and ready.");
            return index;
        } else {
            std::cerr << "Invalid input. Please enter a valid number." << std::endl;
        }
    }
}

// Function to record audio using PortAudio
bool recordAudio(const std::string &filename, int duration, PaDeviceIndex deviceIndex, int sampleRate = 44100, int channels = 1) {
    try {
        PaStream *stream;
        Pa_OpenDefaultStream(&stream, channels, 0, paInt16, sampleRate, 256, nullptr, nullptr);
        Pa_StartStream(stream);

        std::vector<int16_t> audioData(sampleRate * duration * channels);
        Pa_ReadStream(stream, audioData.data(), audioData.size());
        Pa_StopStream(stream);
        Pa_CloseStream(stream);

        SF_INFO sfInfo;
        sfInfo.channels = channels;
        sfInfo.samplerate = sampleRate;
        sfInfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;

        SNDFILE *file = sf_open(filename.c_str(), SFM_WRITE, &sfInfo);
        if (file) {
            sf_writef_short(file, audioData.data(), audioData.size() / channels);
            sf_close(file);
            return true;
        } else {
            std::cerr << "Error writing audio file." << std::endl;
        }
    } catch (const std::exception &e) {
        std::cerr << "Error recording audio: " << e.what() << std::endl;
    }
    return false;
}

// Function to transcribe audio using Whisper
std::string transcribeAudio(const std::string &filename, whisper_context *ctx) {
    if (!ctx || filename.empty()) {
        std::cerr << "Invalid parameters for transcription." << std::endl;
        return "";
    }
    try {
        // Implement Whisper transcription logic here
        return "Transcribed text";  // Placeholder
    } catch (const std::exception &e) {
        std::cerr << "Error during transcription: " << e.what() << std::endl;
    }
    return "";
}

int main() {
    try {
        std::cout << "Loading Whisper model..." << std::endl;
        whisper_context *whisperCtx = whisper_init("tiny.bin");  // Adjust model path
        if (!whisperCtx) {
            std::cerr << "Failed to load Whisper model." << std::endl;
            return -1;
        }

        PaDeviceIndex micIndex = findOrSelectMicrophone();
        if (micIndex == paNoDevice) {
            textToSpeechPico("No suitable microphone found. Please check your device.");
            return -1;
        }

        std::cout << "Listening for commands..." << std::endl;
        // Add command listening loop here

        whisper_free(whisperCtx);
        Pa_Terminate();
    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    return 0;
}