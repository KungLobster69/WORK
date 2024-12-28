#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <whisper.h> // ไลบรารี Whisper (สมมติว่าติดตั้งแล้ว)
#include "ViewController.h"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <audio_file_path>" << std::endl;
        return 1;
    }

    // รับไฟล์เสียงจากอาร์กิวเมนต์
    std::string audioFilePath = argv[1];
    std::cout << "Processing audio file: " << audioFilePath << std::endl;

    // โหลด Whisper Model
    std::string modelPath = "path_to_whisper_model.bin";
    whisper_context* ctx = whisper_init_from_file(modelPath.c_str());
    if (!ctx) {
        std::cerr << "Failed to load Whisper model: " << modelPath << std::endl;
        return 1;
    }

    // โหลดไฟล์เสียง
    std::vector<float> audioData;
    if (!whisper_load_audio(audioFilePath, audioData)) {
        std::cerr << "Failed to load audio file: " << audioFilePath << std::endl;
        whisper_free(ctx);
        return 1;
    }

    // กำหนดพารามิเตอร์
    whisper_full_params params = whisper_full_default_params();
    params.language = "en"; // กำหนดภาษา
    params.n_threads = 4;   // จำนวน Thread

    // ประมวลผลไฟล์เสียง
    if (whisper_full(ctx, params, audioData.data(), audioData.size()) != 0) {
        std::cerr << "Failed to process audio file." << std::endl;
        whisper_free(ctx);
        return 1;
    }

    // แสดงผลลัพธ์
    int n_segments = whisper_full_n_segments(ctx);
    for (int i = 0; i < n_segments; ++i) {
        const char* text = whisper_full_get_segment_text(ctx, i);
        std::cout << "Segment " << i + 1 << ": " << text << std::endl;
    }

    // ล้างหน่วยความจำ
    whisper_free(ctx);
    return 0;
}
