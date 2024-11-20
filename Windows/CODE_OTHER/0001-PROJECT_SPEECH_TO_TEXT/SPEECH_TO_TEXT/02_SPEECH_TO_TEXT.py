import pyaudio
import wave
import whisper
import numpy as np
import warnings
import time
from gtts import gTTS
from playsound import playsound
import os

# ปิดคำเตือน FutureWarning และ UserWarning
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def get_microphone_info(target_name="Microphone (BY Y02)"):
    """ค้นหาและแสดงรายละเอียดของไมโครโฟนที่ระบุ"""
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if target_name.lower() in device_info['name'].lower():
            print(f"พบอุปกรณ์: {device_info['name']} (ID: {i})")
            p.terminate()
            return i, device_info
    print(f"ไม่พบอุปกรณ์ '{target_name}'")
    p.terminate()
    return None, None

def is_microphone_active(device_id, sample_duration=1):
    """
    ตรวจสอบว่าไมโครโฟนยังส่งข้อมูลเสียงอยู่หรือไม่
    :param device_id: int, ID ของไมโครโฟน
    :param sample_duration: int, ระยะเวลาการสุ่มตัวอย่างเสียง (วินาที)
    :return: bool, True หากไมโครโฟนมีเสียงใช้งาน
    """
    p = pyaudio.PyAudio()
    chunk = 1024
    rate = 44100
    channels = 1

    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        input_device_index=device_id,
                        frames_per_buffer=chunk)
        frames = []

        for _ in range(0, int(rate / chunk * sample_duration)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(np.frombuffer(data, dtype=np.int16))

        # คำนวณพลังงานเฉลี่ยของสัญญาณ
        audio_signal = np.concatenate(frames)
        signal_power = np.mean(audio_signal ** 2)
        stream.stop_stream()
        stream.close()
        p.terminate()

        return signal_power > 500  # เกณฑ์พลังงานต่ำสุด
    except:
        p.terminate()
        return False

def save_audio_to_wav(frames, channels, rate, output_file):
    """
    บันทึกข้อมูลเสียงลงในไฟล์ .wav
    :param frames: list, ข้อมูลเสียง
    :param channels: int, จำนวนช่องเสียง
    :param rate: int, Sample Rate
    :param output_file: str, ชื่อไฟล์ .wav
    """
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    print(f"บันทึกไฟล์เสียงเรียบร้อย: {output_file}")

def play_audio_response(text):
    """
    สร้างเสียงตอบกลับจากข้อความและเล่นเสียง
    :param text: str, ข้อความที่ต้องการแปลงเป็นเสียง
    """
    tts = gTTS(text=text, lang='en')
    response_file = "response.mp3"
    tts.save(response_file)
    print(f"ตอบกลับ: {text}")
    playsound(response_file)
    os.remove(response_file)  # ลบไฟล์หลังเล่นเสียงเสร็จ

def listen_and_detect(device_info, duration=2, keyword="computer"):
    """
    ฟังเสียงแบบเรียลไทม์ บันทึกเสียงเป็นไฟล์ .wav และตรวจจับคำที่กำหนด
    :param device_info: dict, ข้อมูลอุปกรณ์จาก PyAudio
    :param duration: int, ระยะเวลาของแต่ละช่วง (วินาที)
    :param keyword: str, คำที่ต้องการตรวจหาในเสียง
    """
    device_id = device_info['index']
    channels = int(device_info['maxInputChannels'])
    rate = int(device_info['defaultSampleRate'])
    chunk = 1024  # ขนาดของ buffer
    model = whisper.load_model("small")
    p = pyaudio.PyAudio()

    print(f"กำลังตรวจจับคำว่า '{keyword}' จาก '{device_info['name']}'")

    try:
        while True:
            # ตรวจสอบสถานะไมโครโฟนก่อนเริ่มฟังเสียง
            if not is_microphone_active(device_id):
                print("ไมโครโฟนถูกปิดหรือไม่พร้อมใช้งาน กำลังรอ...")
                time.sleep(1)
                continue

            print("ไมโครโฟนพร้อม เริ่มฟังเสียง...")
            frames = []

            # บันทึกเสียงเป็นข้อมูลในหน่วยความจำ
            stream = p.open(format=pyaudio.paInt16,
                            channels=channels,
                            rate=rate,
                            input=True,
                            input_device_index=device_id,
                            frames_per_buffer=chunk)
            for _ in range(0, int(rate / chunk * duration)):
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
            stream.stop_stream()
            stream.close()

            # บันทึกเสียงเป็นไฟล์ .wav
            temp_audio_file = "temp_audio.wav"
            save_audio_to_wav(frames, channels, rate, temp_audio_file)

            # ถอดเสียงและตรวจจับคำ
            print("กำลังถอดเสียง...")
            result = model.transcribe(temp_audio_file, fp16=False, language="en")
            text = result.get("text", "").lower()
            print(f"ข้อความที่ถอดเสียงได้: {text}")

            if keyword.lower() in text:
                print(f"ตรวจพบคำว่า '{keyword}'!")
                play_audio_response("Keyword detected. How can I assist you?")
            else:
                print("ไม่พบคำที่กำหนด")

    except KeyboardInterrupt:
        print("\nหยุดการตรวจจับคำ")
    finally:
        p.terminate()

# เริ่มต้นใช้งาน
if __name__ == "__main__":
    mic_index, mic_info = get_microphone_info("Microphone (BY Y02)")
    if mic_index is not None:
        listen_and_detect(mic_info, duration=2, keyword="computer")
    else:
        print("โปรดตรวจสอบการเชื่อมต่อไมโครโฟน")