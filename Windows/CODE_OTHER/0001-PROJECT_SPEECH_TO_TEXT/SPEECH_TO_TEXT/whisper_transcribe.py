import whisper  # นำเข้าไลบรารี whisper
import warnings

# ปิดการแจ้งเตือนที่ไม่ต้องการ
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def transcribe_audio(file_path, language="en"):
    model = whisper.load_model("large")
    transcription = model.transcribe(file_path, language=language)
    return transcription["text"]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        language = sys.argv[2] if len(sys.argv) > 2 else "en"
        result = transcribe_audio(file_path, language)
        print("Transcription:", result)  # แสดงผลการถอดเสียง
    else:
        print("Please provide an audio file path.")
