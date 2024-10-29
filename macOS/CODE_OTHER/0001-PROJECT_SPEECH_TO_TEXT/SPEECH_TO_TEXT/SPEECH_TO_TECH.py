import sounddevice as sd
from scipy.io.wavfile import write
import whisper  # นำเข้าโมดูล whisper

# กำหนดพารามิเตอร์การบันทึก
duration = 10  # ระยะเวลาในการบันทึก (วินาที)
sample_rate = 48000  # Sample rate 48 kHz
output_file = 'output.wav'  # ชื่อไฟล์ที่ต้องการบันทึก

print("เริ่มบันทึกเสียง...")

# บันทึกเสียงโดยใช้ฟอร์แมต float32
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')

# รอให้การบันทึกเสร็จสิ้น
sd.wait()
print("บันทึกเสียงเสร็จสิ้น")

# บันทึกเสียงเป็นไฟล์ .wav
write(output_file, sample_rate, audio_data)
print(f"ไฟล์เสียงถูกบันทึกเป็น '{output_file}'")

# โหลดโมเดล Whisper (ขนาดใหญ่)
model = whisper.load_model("turbo")

# ถอดเสียงจากไฟล์ที่บันทึก
print("เริ่มถอดเสียง...")
transcription = model.transcribe(output_file, language="en")

# แสดงผลลัพธ์การถอดเสียง
print("ข้อความที่ถอดเสียงได้:")
print(transcription["text"])