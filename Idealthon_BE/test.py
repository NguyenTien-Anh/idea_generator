import os
import re
import time
import tempfile
from pydub import AudioSegment, silence
from dotenv import load_dotenv
from google import genai
from google.genai import types
from transcript import vie_prompt

load_dotenv()


CHUNK_OVERLAP_MS = 1000              # 1s overlap
MIN_SILENCE_LEN_MS = 700
SILENCE_THRESH_DB = -40
MAX_CHUNK_DURATION_MS = 10 * 60 * 1000  # 10 phút
OUTPUT_TRANSCRIPT = "full_transcript.txt"

# === SETUP GEMINI ===
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# === STEP 1: Chia audio theo điểm im lặng, return [(chunk, offset)] ===
def split_audio_by_silence(audio_path):
    audio = AudioSegment.from_file(audio_path)
    silent_ranges = silence.detect_silence(audio,
                                           min_silence_len=MIN_SILENCE_LEN_MS,
                                           silence_thresh=SILENCE_THRESH_DB)
    silent_ranges = [(start, stop) for start, stop in silent_ranges if stop - start > 300]

    chunks = []
    last_cut = 0

    for start, stop in silent_ranges:
        if stop - last_cut > MAX_CHUNK_DURATION_MS:
            cut_point = stop
            chunk = audio[max(0, last_cut - CHUNK_OVERLAP_MS):cut_point + CHUNK_OVERLAP_MS]
            chunks.append((chunk, max(0, last_cut - CHUNK_OVERLAP_MS)))
            last_cut = cut_point

    # Add final chunk
    if last_cut < len(audio):
        chunk = audio[max(0, last_cut - CHUNK_OVERLAP_MS):]
        chunks.append((chunk, max(0, last_cut - CHUNK_OVERLAP_MS)))

    return chunks


# === STEP 2: Chuyển audio segment thành bytes ===
def audio_segment_to_bytes(segment):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        segment.export(temp_file.name, format="mp3")
        with open(temp_file.name, "rb") as f:
            data = f.read()
        os.unlink(temp_file.name)
    return data


# === STEP 3: Gửi 1 chunk lên Gemini ===
def transcribe_chunk(chunk_bytes):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=[
                vie_prompt,
                types.Part.from_bytes(
                    data=chunk_bytes,
                    mime_type='audio/mp3',
                )
            ]
        )
        return response.text
    except Exception as e:
        print(f"[ERROR] Gemini failed: {e}")
        return ""


# === STEP 4: Cộng offset vào các timestamp ===
def adjust_timestamps(text, offset_ms):
    def time_to_sec(t):
        m, s = map(float, t.split(":"))
        return m * 60 + s

    def sec_to_time(sec):
        m = int(sec // 60)
        s = int(sec % 60)
        return f"{m}:{s:02}"

    def replace_fn(match):
        start, end = match.group(1), match.group(2)
        start_sec = time_to_sec(start) + offset_ms / 1000
        end_sec = time_to_sec(end) + offset_ms / 1000
        return f"<time>{sec_to_time(start_sec)} - {sec_to_time(end_sec)}</time>"

    return re.sub(r"<time>(\d+:\d+) - (\d+:\d+)</time>", replace_fn, text)


# === STEP 5: Ghép transcript & loại trùng lặp ===
def merge_transcripts(transcripts):
    seen_lines = set()
    final_transcript = []

    for text in transcripts:
        for line in text.splitlines():
            if re.match(r"<time>\d+:\d+ - \d+:\d+</time>", line.strip()):
                content = line.strip()
                if content not in seen_lines:
                    final_transcript.append(content)
                    seen_lines.add(content)

    return "\n".join(final_transcript)


# === MAIN ===
def transcribe_audio_file(input_audio_path):
    print("[+] Splitting audio by silence...")
    chunks = split_audio_by_silence(input_audio_path)
    print(f"[+] Total chunks: {len(chunks)}")

    transcripts = []
    for i, (chunk, offset) in enumerate(chunks):
        print(f"[+] Transcribing chunk {i+1}/{len(chunks)} (offset: {offset/1000:.2f}s)...")
        audio_bytes = audio_segment_to_bytes(chunk)
        raw_text = transcribe_chunk(audio_bytes)
        adjusted = adjust_timestamps(raw_text, offset)
        transcripts.append(adjusted)
        time.sleep(1)

    final = merge_transcripts(transcripts)

    with open(OUTPUT_TRANSCRIPT, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"[✓] Done! Saved to {OUTPUT_TRANSCRIPT}")


# === RUN ===
if __name__ == "__main__":
    input_file = "/home/rb071/Downloads/Vie.mp3"  # ← Đặt file đầu vào ở đây
    transcribe_audio_file(input_file)
