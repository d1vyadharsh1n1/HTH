#!/usr/bin/env python3
"""
burn_word_subs.py with lightweight NLP emotion coloring
Now also generates interactive_subs.json for web app
"""

import os
import sys
import time
import requests
import subprocess
import ffmpeg
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch

# ----------------- CONFIG -----------------
# Lightweight emotion model (only ~50MB)
EMOTION_MODEL = "bhadresh-savani/distilbert-base-uncased-emotion"
try:
    tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(EMOTION_MODEL)
    emotion_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
except Exception as e:
    print(f"Error loading emotion model: {e}")
    emotion_classifier = None

# Simplified emotion color mapping
EMOTION_COLORS = {
    'joy': 'ffff00',      # yellow
    'sadness': '0000ff',  # blue
    'anger': 'ff0000',    # red
    'fear': '800080',     # purple
    'surprise': 'ffa500', # orange
    'love': 'ff69b4',     # pink
    'neutral': 'ffffff'   # white
}

# Emotion emoji mapping
EMOTION_EMOJIS = {
    'joy': '😊',
    'sadness': '😔',
    'anger': '😡',
    'fear': '😨',
    'surprise': '😲',
    'love': '❤️',
    'neutral': '😐'
}

# Either set ASSEMBLYAI_API_KEY in the environment OR paste it here

API_KEY = os.environ.get("ASSEMBLYAI_API_KEY") or "2efd94d4c0594bcab804953a0e780ea8"
if not API_KEY:
    print("WARNING: No AssemblyAI API key provided. Set ASSEMBLYAI_API_KEY env var or paste key in script.")

# Base URL
BASE = "https://api.assemblyai.com/v2"

# Files
INPUT_VIDEO = "MonsterInc.mp4"
EXTRACTED_AUDIO = "MonsterInc.mp3"
SRT_FILE = "subtitles.srt"
OUTPUT_VIDEO = "MonsterDubs.mp4"
JSON_OUTPUT = "interactive_subs.json"  # NEW: JSON file for web app

# Controls for grouping words into readable subtitle lines
MAX_CHUNK_MS = 3200     # max duration per subtitle (ms)
MAX_CHARS = 45          # approx max characters per subtitle line
PAD_MS = 80             # pad end of subtitle so it doesn't cut exactly at word end

# Polling
POLL_INTERVAL = 3       # seconds between checking transcription status

# ----------------- HELPERS -----------------
def detect_emotion_lightweight(text):
    """
    Uses a lightweight DistilBERT model fine-tuned for emotion classification
    """
    if not emotion_classifier:
        return 'neutral'
    
    try:
        # Process text in chunks if too long
        if len(text) > 400:
            text = text[:400] + "..."
        
        result = emotion_classifier(text, truncation=True, max_length=512)
        if result:
            emotion = result[0]['label'].lower()
            return emotion
    except Exception as e:
        print(f"Emotion detection error: {str(e)[:100]}...")
    return 'neutral'

def get_word_definition(word):
    """Fetches a definition and example from a free dictionary API."""
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            meanings = data[0].get("meanings", [])
            for meaning in meanings:
                definitions = meaning.get("definitions", [])
                for definition in definitions:
                    if definition.get("example"):
                        return {
                            "definition": definition.get("definition"),
                            "example": definition.get("example")
                        }
            # Fallback to the first definition if no example is found
            if meanings and meanings[0].get("definitions"):
                return {
                    "definition": meanings[0]["definitions"][0].get("definition", "No definition found."),
                    "example": "No example available."
                }
    except Exception as e:
        print(f"Error fetching definition for '{word}': {e}")
    return {"definition": "Definition not found.", "example": "Example not found."}

def ensure_file_exists(path):
    if not os.path.exists(path):
        print(f"ERROR: Required file not found: {path}")
        sys.exit(1)

def extract_audio(video_path, audio_out):
    """Extract audio using ffmpeg-python wrapper (creates mp3 using libmp3lame)."""
    print(f"[1/6] Extracting audio from '{video_path}' -> '{audio_out}' ...")
    try:
        ffmpeg.input(video_path).output(audio_out, acodec='libmp3lame', vn=None).run(overwrite_output=True, quiet=False)
    except ffmpeg.Error as e:
        print("FFmpeg error during extraction:")
        try:
            print(e.stderr.decode())
        except Exception:
            print(e)
        sys.exit(1)
    if os.path.exists(audio_out):
        print("Audio extracted.")
    else:
        print("Audio extraction failed: output not found.")
        sys.exit(1)

def upload_audio_to_assemblyai(audio_path, api_key):
    """Upload binary file to AssemblyAI /upload endpoint and return upload_url."""
    print(f"[2/6] Uploading audio '{audio_path}' to AssemblyAI...")
    headers = {"authorization": api_key}
    try:
        with open(audio_path, "rb") as f:
            r = requests.post(f"{BASE}/upload", headers=headers, data=f)
        r.raise_for_status()
        upload_url = r.json().get("upload_url")
        if not upload_url:
            print("Upload response did not contain upload_url:", r.text)
            sys.exit(1)
        print("Upload successful. audio_url:", upload_url)
        return upload_url
    except FileNotFoundError:
        print("Audio file not found for upload.")
        sys.exit(1)
    except requests.RequestException as e:
        print("Error uploading audio:", e)
        if hasattr(e, "response") and e.response is not None:
            print("Response:", e.response.text)
        sys.exit(1)

def request_transcript(api_key, audio_url):
    """
    Request a transcription with word timestamps.
    """
    print("[3/6] Requesting transcription (with word timestamps)...")
    headers = {"authorization": api_key}
    payload = {
        "audio_url": audio_url,
        "speech_model": "universal",
        "format_text": True,
        "punctuate": True,
        "disfluencies": False
    }
    try:
        r = requests.post(f"{BASE}/transcript", json=payload, headers=headers)
        r.raise_for_status()
        tid = r.json().get("id")
        if not tid:
            print("Transcription request failed to return id:", r.text)
            sys.exit(1)
        print("Transcript requested. id:", tid)
        return tid
    except requests.RequestException as e:
        print("Error requesting transcription:", e)
        if hasattr(e, "response") and e.response is not None:
            print("Response:", e.response.text)
        sys.exit(1)

def poll_transcript(api_key, transcript_id, poll_interval=POLL_INTERVAL):
    """Polls until transcription status is 'completed' (returns JSON) or 'error' (raises)."""
    print("[4/6] Polling transcription status...")
    headers = {"authorization": api_key}
    url = f"{BASE}/transcript/{transcript_id}"
    while True:
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            j = r.json()
        except requests.RequestException as e:
            print("Error polling transcription:", e)
            sys.exit(1)

        status = j.get("status")
        if status == "completed":
            print("Transcription completed.")
            return j
        if status == "error":
            print("Transcription error:", j.get("error"))
            sys.exit(1)

        print(f"Status: {status}. Waiting {poll_interval}s...")
        time.sleep(poll_interval)

def extract_word_list_from_result(result_json):
    """
    Extract a flat list of words (dicts with text,start,end) from AssemblyAI result.
    """
    words = result_json.get("words") or []
    if words:
        return words
    # fallback: collect words from utterances if present
    utterances = result_json.get("utterances") or []
    if utterances:
        all_words = []
        for u in utterances:
            wlist = u.get("words") or []
            all_words.extend(wlist)
        if all_words:
            return all_words
    return []

def ms_to_srt_time(ms):
    """Convert milliseconds to SRT timestamp 'HH:MM:SS,mmm'"""
    ms = int(ms)
    hours = ms // 3600000
    rem = ms % 3600000
    minutes = rem // 60000
    rem = rem % 60000
    seconds = rem // 1000
    millis = rem % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def words_to_grouped_srt_and_json(words, srt_path, json_path, max_chunk_ms=MAX_CHUNK_MS, max_chars=MAX_CHARS, pad_ms=PAD_MS):
    """
    Modified to generate both SRT and JSON files with emotion detection
    """
    print(f"[5/6] Building emotion-color-coded SRT -> '{srt_path}' and JSON -> '{json_path}' ...")
    lines = []
    json_data = []
    cur_words = []
    cur_start = None
    cur_end = None
    cur_chars = 0

    for w in words:
        text = w.get("text") or ""
        try:
            start = int(float(w.get("start")))
            end = int(float(w.get("end")))
        except Exception:
            continue

        if cur_start is None:
            cur_start = start
            cur_end = end
            cur_words = [text]
            cur_chars = len(text)
            continue

        prospective_chars = cur_chars + 1 + len(text)
        prospective_dur = end - cur_start

        if (prospective_dur > max_chunk_ms) or (prospective_chars > max_chars):
            # Process current chunk
            full_text = " ".join(cur_words)
            emotion = detect_emotion_lightweight(full_text)
            color = EMOTION_COLORS.get(emotion, 'ffffff')
            emoji = EMOTION_EMOJIS.get(emotion, '')
            
            # Format with color and emoji for SRT
            colored_text = f'<font color="#{color}">{emoji} {full_text}</font>'
            lines.append((cur_start, cur_end + pad_ms, colored_text))
            
            # Add individual words to JSON with emotion and definitions
            for word_text in cur_words:
                clean_word = word_text.strip('.,?!').lower()
                definition_data = get_word_definition(clean_word)
                
                json_entry = {
                    "start": cur_start,
                    "end": cur_end + pad_ms,
                    "text": word_text,
                    "emotion": emotion,
                    "definition": definition_data["definition"],
                    "example": definition_data["example"]
                }
                json_data.append(json_entry)
            
            # Start new chunk
            cur_words = [text]
            cur_start = start
            cur_end = end
            cur_chars = len(text)
        else:
            cur_words.append(text)
            cur_end = end
            cur_chars = prospective_chars

    if cur_words:
        full_text = " ".join(cur_words)
        emotion = detect_emotion_lightweight(full_text)
        color = EMOTION_COLORS.get(emotion, 'ffffff')
        emoji = EMOTION_EMOJIS.get(emotion, '')
        colored_text = f'<font color="#{color}">{emoji} {full_text}</font>'
        lines.append((cur_start, cur_end + pad_ms, colored_text))
        
        # Add final words to JSON
        for word_text in cur_words:
            clean_word = word_text.strip('.,?!').lower()
            definition_data = get_word_definition(clean_word)
            
            json_entry = {
                "start": cur_start,
                "end": cur_end + pad_ms,
                "text": word_text,
                "emotion": emotion,
                "definition": definition_data["definition"],
                "example": definition_data["example"]
            }
            json_data.append(json_entry)

    # Write SRT file
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, (st, en, text) in enumerate(lines, start=1):
            if en <= st:
                en = st + 20
            f.write(f"{i}\n")
            f.write(f"{ms_to_srt_time(st)} --> {ms_to_srt_time(en)}\n")
            f.write(text.strip() + "\n\n")
    
    # Write JSON file for web app
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)
    
    print("Emotion-color-coded SRT file written:", srt_path)
    print("Interactive JSON file written:", json_path)
    return srt_path

def fallback_get_srt_from_assemblyai(api_key, transcript_id, srt_path):
    """
    If words are not present, attempt to download AssemblyAI's own SRT for the transcript.
    """
    print("[5/6 fallback] Attempting to download AssemblyAI-generated SRT...")
    headers = {"authorization": api_key}
    url = f"{BASE}/transcript/{transcript_id}/srt"
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        print("Downloaded AssemblyAI SRT to", srt_path)
        return srt_path
    except requests.RequestException as e:
        print("Failed to download AssemblyAI SRT:", e)
        return None

def burn_srt_into_video(input_video, srt_file, output_video):
    """Burn the subtitles into the video via ffmpeg subtitles filter."""
    print(f"[6/6] Burning '{srt_file}' into video -> '{output_video}' ...")
    ensure_file_exists(input_video)
    ensure_file_exists(srt_file)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vf", f"subtitles={srt_file}:force_style='Fontsize=24,PrimaryColour=&HFFFFFF&'",
        "-c:a", "copy",
        output_video
    ]
    try:
        subprocess.run(cmd, check=True)
        print("Output written to:", output_video)
    except subprocess.CalledProcessError as e:
        print("ffmpeg failed while burning subtitles. Command output:")
        print(e)
        sys.exit(1)

# ----------------- MAIN FLOW -----------------
def main():
    # basic checks
    ensure_file_exists(INPUT_VIDEO)
    if not API_KEY:
        print("ERROR: No AssemblyAI API key found. Set ASSEMBLYAI_API_KEY env var or update API_KEY in script.")
        sys.exit(1)

    # 1. Extract audio
    extract_audio(INPUT_VIDEO, EXTRACTED_AUDIO)

    # 2. Upload audio
    audio_url = upload_audio_to_assemblyai(EXTRACTED_AUDIO, API_KEY)

    # 3. Request transcription
    transcript_id = request_transcript(API_KEY, audio_url)

    # 4. Poll until transcription done
    result = poll_transcript(API_KEY, transcript_id)

    # 5. Try to extract words
    words = extract_word_list_from_result(result)
    if not words:
        print("No per-word timestamps found in transcription JSON.")
        # fallback: try download srt directly from assemblyai
        downloaded = fallback_get_srt_from_assemblyai(API_KEY, transcript_id, SRT_FILE)
        if not downloaded:
            print("No SRT available from AssemblyAI and no words present. Exiting.")
            sys.exit(1)
    else:
        # build grouped srt and json
        words_to_grouped_srt_and_json(words, SRT_FILE, JSON_OUTPUT)

    # 6. Burn SRT into video
    burn_srt_into_video(INPUT_VIDEO, SRT_FILE, OUTPUT_VIDEO)

    print("\nAll done! 🎉")
    print("Generated:", OUTPUT_VIDEO)
    print("Generated:", JSON_OUTPUT, "(for web app)")
    print("If subtitles look too fast/slow, adjust MAX_CHUNK_MS, MAX_CHARS, or PAD_MS near top of the script.")

if __name__ == "__main__":
    main() 