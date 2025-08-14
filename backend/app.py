from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os, time, ffmpeg, requests, subprocess, sys

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from React
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ASSEMBLYAI_API_KEY = "2efd94d4c0594bcab804953a0e780ea8"
ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com"

def extract_audio(video_path, audio_path):
    ffmpeg_path = r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"  # <-- put your actual path here
    (
        ffmpeg
        .input(video_path)
        .output(audio_path, acodec='libmp3lame')
        .run(cmd=ffmpeg_path, overwrite_output=True, quiet=True)
    )

def transcribe(audio_path):
    # Upload audio
    with open(audio_path, "rb") as f:
        r = requests.post(
            f"{ASSEMBLYAI_BASE_URL}/v2/upload",
            headers={"authorization": ASSEMBLYAI_API_KEY},
            data=f
        )
    audio_url = r.json()['upload_url']

    # Start transcription
    r2 = requests.post(
        f"{ASSEMBLYAI_BASE_URL}/v2/transcript",
        headers={"authorization": ASSEMBLYAI_API_KEY},
        json={"audio_url": audio_url, "speech_model": "universal"}
    )
    transcript_id = r2.json()['id']

    # Poll for completion
    polling_endpoint = f"{ASSEMBLYAI_BASE_URL}/v2/transcript/{transcript_id}"
    while True:
        result = requests.get(polling_endpoint, headers={"authorization": ASSEMBLYAI_API_KEY}).json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'error':
            return f"Error: {result['error']}"
        time.sleep(2)

@app.route("/upload-video", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)

    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit(".",1)[0]+".mp3")
    extract_audio(video_path, audio_path)
    transcript_text = transcribe(audio_path)

    return jsonify({"transcript": transcript_text})

'''@app.route("/generate_subtitles", methods=["GET"])
def generate_subtitles():
    try:
        script_path = os.path.join("subtitles", "burn_word_subs.py")
        subprocess.run([sys.executable, script_path], check=True)
        return jsonify({"status": "success", "message": "Emotion subtitles generated successfully"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Script failed: {str(e)}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})'''

@app.route("/generate_subtitles")
def get_dubbed_video():
    video_folder = os.path.join("backend", "subtitles")
    video_filename = "MonsterDubs.mp4"  # change to your actual file name
    return send_from_directory(video_folder, video_filename)

@app.route("/subtitles/")
@app.route("/subtitles/<path:filename>")
def serve_subtitles(filename=None):
    """Serve files from the subtitles folder"""
    if filename is None:
        # Serve index.html for the root subtitles path
        return send_from_directory("subtitles", "index.html")
    else:
        # Serve specific files from subtitles folder
        return send_from_directory("subtitles", filename)

if __name__ == "__main__":
    app.run(debug=True)
