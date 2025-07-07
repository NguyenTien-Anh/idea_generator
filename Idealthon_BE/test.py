import os
from pydub import AudioSegment

# Gán thủ công nếu cần
AudioSegment.converter = r"D:\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe   = r"D:\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe"

os.environ["PATH"] += os.pathsep + r"D:\ffmpeg-7.1.1-essentials_build\bin"

sound = AudioSegment.from_mp3("C:/Users/LS/Downloads/Vie.mp3")
print("Load thành công")