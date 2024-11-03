#include <stdio.h>
#include <stdlib.h>
#include <locale.h> // สำหรับตั้งค่าการเข้ารหัส
#include <wchar.h>  // สำหรับใช้ wprintf
#include <portaudio.h>
#include <sndfile.h>

#define SAMPLE_RATE 48000
#define NUM_CHANNELS 1
#define DURATION 10
#define FRAMES_PER_BUFFER 1024

typedef struct {
    float *recordedSamples;
    int maxFrameIndex;
    int frameIndex;
} AudioData;

static int recordCallback(const void *inputBuffer, void *outputBuffer,
                          unsigned long framesPerBuffer,
                          const PaStreamCallbackTimeInfo* timeInfo,
                          PaStreamCallbackFlags statusFlags,
                          void *userData) {
    AudioData *data = (AudioData*) userData;
    const float *rptr = (const float*) inputBuffer;
    float *wptr = &data->recordedSamples[data->frameIndex * NUM_CHANNELS];
    int framesToCalc = (data->maxFrameIndex - data->frameIndex) < framesPerBuffer ?
                        (data->maxFrameIndex - data->frameIndex) : framesPerBuffer;
    if (inputBuffer == NULL) {
        for (int i = 0; i < framesToCalc * NUM_CHANNELS; i++) {
            *wptr++ = 0;
        }
    } else {
        for (int i = 0; i < framesToCalc * NUM_CHANNELS; i++) {
            *wptr++ = *rptr++;
        }
    }
    data->frameIndex += framesToCalc;
    return (data->frameIndex >= data->maxFrameIndex) ? paComplete : paContinue;
}

void transcribe_with_whisper(const char* audio_file, const char* language) {
    char command[256];
    snprintf(command, sizeof(command), "python whisper_transcribe.py %s %s", audio_file, language);
    printf("Starting Whisper transcription...\n");
    int result = system(command); // Run the Python script for transcription
    if (result == -1) {
        fprintf(stderr, "Error executing Whisper transcription.\n");
    } else {
        printf("Whisper transcription completed.\n");
    }
}

int main() {
    setlocale(LC_ALL, ""); // Set encoding according to the system to support UTF-8

    PaError err;
    AudioData data;
    const char* audio_file = "output.wav";
    const char* language = "en";
    int totalFrames = DURATION * SAMPLE_RATE;
    data.maxFrameIndex = totalFrames;
    data.frameIndex = 0;
    data.recordedSamples = (float *) malloc(totalFrames * sizeof(float));
    if (data.recordedSamples == NULL) {
        fprintf(stderr, "Error allocating memory for recorded samples.\n");
        return 1;
    }

    // Initialize PortAudio
    err = Pa_Initialize();
    if (err != paNoError) {
        fprintf(stderr, "Error initializing PortAudio: %s\n", Pa_GetErrorText(err));
        return 1;
    }

    // Open stream for recording
    PaStream *stream;
    err = Pa_OpenDefaultStream(&stream, NUM_CHANNELS, 0, paFloat32, SAMPLE_RATE, FRAMES_PER_BUFFER, recordCallback, &data);
    if (err != paNoError) {
        fprintf(stderr, "Error opening stream: %s\n", Pa_GetErrorText(err));
        Pa_Terminate();
        free(data.recordedSamples);
        return 1;
    }

    // Start recording
    printf("Recording...\n");
    err = Pa_StartStream(stream);
    if (err != paNoError) {
        fprintf(stderr, "Error starting stream: %s\n", Pa_GetErrorText(err));
        Pa_CloseStream(stream);
        Pa_Terminate();
        free(data.recordedSamples);
        return 1;
    }

    // Wait for the recording to complete
    while ((err = Pa_IsStreamActive(stream)) == 1) {
        Pa_Sleep(100);
    }
    if (err < 0) {
        fprintf(stderr, "Error during recording: %s\n", Pa_GetErrorText(err));
    }

    // Close stream after recording completes
    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        fprintf(stderr, "Error closing stream: %s\n", Pa_GetErrorText(err));
    }
    Pa_Terminate();

    printf("Recording complete.\n");

    // Save audio data to .wav file
    SF_INFO sfinfo;
    sfinfo.channels = NUM_CHANNELS;
    sfinfo.samplerate = SAMPLE_RATE;
    sfinfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;
    SNDFILE *outfile = sf_open(audio_file, SFM_WRITE, &sfinfo);
    if (!outfile) {
        fprintf(stderr, "Error opening output file: %s\n", sf_strerror(NULL));
        free(data.recordedSamples);
        return 1;
    }
    sf_write_float(outfile, data.recordedSamples, totalFrames);
    sf_close(outfile);
    printf("Audio saved to %s\n", audio_file);

    // Transcribe audio with Whisper
    transcribe_with_whisper(audio_file, language);

    // Free allocated memory
    free(data.recordedSamples);

    return 0;
}
