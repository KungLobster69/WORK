#include <iostream>
#include <locale>
#include <portaudio.h>
#include <sndfile.h>
#include <whisper.h>  // ไลบรารี Whisper C++

#define SAMPLE_RATE 48000
#define NUM_CHANNELS 1
#define DURATION 10
#define FRAMES_PER_BUFFER 1024

struct AudioData {
    float *recordedSamples;
    int maxFrameIndex;
    int frameIndex;
};

// Callback สำหรับบันทึกเสียง
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

// ฟังก์ชันถอดเสียงด้วย Whisper C++
void transcribe_with_whisper(const char* audio_file, const char* language) {
    whisper::Whisper whisperModel;
    if (!whisperModel.loadModel("path/to/whisper/model")) { // ระบุเส้นทางไปยังโมเดลของ Whisper
        std::cerr << "Error loading Whisper model." << std::endl;
        return;
    }

    whisper::AudioData audioData;
    if (!audioData.loadFromFile(audio_file)) { // โหลดไฟล์เสียงที่บันทึก
        std::cerr << "Error loading audio file." << std::endl;
        return;
    }

    // ตั้งค่าภาษาและเริ่มการถอดเสียง
    whisperModel.setLanguage(language);
    std::string transcription = whisperModel.transcribe(audioData);

    if (transcription.empty()) {
        std::cerr << "Error during transcription." << std::endl;
    } else {
        std::cout << "Whisper transcription completed: " << transcription << std::endl;
    }
}

int main() {
    std::locale::global(std::locale("")); // ตั้งค่าภาษาให้รองรับ UTF-8

    PaError err;
    AudioData data;
    const char* audio_file = "output.wav";
    const char* language = "th"; // เลือกภาษาไทย
    int totalFrames = DURATION * SAMPLE_RATE;
    data.maxFrameIndex = totalFrames;
    data.frameIndex = 0;
    data.recordedSamples = new float[totalFrames];
    if (data.recordedSamples == nullptr) {
        std::cerr << "Error allocating memory for recorded samples." << std::endl;
        return 1;
    }

    // เริ่มต้น PortAudio
    err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "Error initializing PortAudio: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    // เปิด stream สำหรับการบันทึกเสียง
    PaStream *stream;
    err = Pa_OpenDefaultStream(&stream, NUM_CHANNELS, 0, paFloat32, SAMPLE_RATE, FRAMES_PER_BUFFER, recordCallback, &data);
    if (err != paNoError) {
        std::cerr << "Error opening stream: " << Pa_GetErrorText(err) << std::endl;
        Pa_Terminate();
        delete[] data.recordedSamples;
        return 1;
    }

    // เริ่มการบันทึกเสียง
    std::cout << "Recording..." << std::endl;
    err = Pa_StartStream(stream);
    if (err != paNoError) {
        std::cerr << "Error starting stream: " << Pa_GetErrorText(err) << std::endl;
        Pa_CloseStream(stream);
        Pa_Terminate();
        delete[] data.recordedSamples;
        return 1;
    }

    // รอจนกว่าการบันทึกจะเสร็จ
    while ((err = Pa_IsStreamActive(stream)) == 1) {
        Pa_Sleep(100);
    }
    if (err < 0) {
        std::cerr << "Error during recording: " << Pa_GetErrorText(err) << std::endl;
    }

    // ปิด stream เมื่อการบันทึกเสร็จสิ้น
    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        std::cerr << "Error closing stream: " << Pa_GetErrorText(err) << std::endl;
    }
    Pa_Terminate();

    std::cout << "Recording complete." << std::endl;

    // บันทึกข้อมูลเสียงเป็นไฟล์ .wav
    SF_INFO sfinfo;
    sfinfo.channels = NUM_CHANNELS;
    sfinfo.samplerate = SAMPLE_RATE;
    sfinfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;
    SNDFILE *outfile = sf_open(audio_file, SFM_WRITE, &sfinfo);
    if (!outfile) {
        std::cerr << "Error opening output file: " << sf_strerror(NULL) << std::endl;
        delete[] data.recordedSamples;
        return 1;
    }
    sf_write_float(outfile, data.recordedSamples, totalFrames);
    sf_close(outfile);
    std::cout << "Audio saved to " << audio_file << std::endl;

    // เรียกใช้ฟังก์ชันถอดเสียง
    transcribe_with_whisper(audio_file, language);

    // ล้างหน่วยความจำที่จัดสรร
    delete[] data.recordedSamples;

    return 0;
}
