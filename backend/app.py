from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os, time, ffmpeg, requests, subprocess, sys, uuid, shutil

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from React

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBTITLES_DIR = os.path.join(BASE_DIR, 'subtitles')
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
GENERATED_DIR = os.path.join(BASE_DIR, 'generated')

# Ensure folders exist
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

# Config
app.config['UPLOAD_FOLDER'] = UPLOADS_DIR

ASSEMBLYAI_API_KEY = "2efd94d4c0594bcab804953a0e780ea8"
ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com"

def extract_audio(video_path, audio_path):
    # Use system ffmpeg via ffmpeg-python
    (
        ffmpeg
        .input(video_path)
        .output(audio_path, acodec='libmp3lame')
        .run(overwrite_output=True, quiet=True)
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

# Dynamic emotion subtitles generation for any uploaded video
@app.route("/process-subtitles", methods=["POST"])
def process_subtitles():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    # Create a unique job folder
    job_id = uuid.uuid4().hex
    job_dir = os.path.join(GENERATED_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    # Save original upload
    video_file = request.files["video"]
    original_name = secure_filename(video_file.filename or f"upload_{job_id}.mp4")
    original_path = os.path.join(job_dir, original_name)
    video_file.save(original_path)

    # The subtitles script expects a file named 'MonsterInc.mp4' in its CWD
    # Copy the uploaded file to that expected name inside the job folder
    script_input_path = os.path.join(job_dir, "MonsterInc.mp4")
    try:
        shutil.copyfile(original_path, script_input_path)
    except Exception:
        # Fallback to move if copying across devices fails
        shutil.copy(original_path, script_input_path)

    # Run the subtitles generator script in the job directory
    script_path = os.path.join(SUBTITLES_DIR, 'burn_word_subs.py')
    try:
        subprocess.run([sys.executable, script_path], cwd=job_dir, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Subtitle generation failed: {str(e)}"}), 500

    # Expected outputs
    output_video = os.path.join(job_dir, "MonsterDubs.mp4")
    output_json = os.path.join(job_dir, "interactive_subs.json")

    if not os.path.exists(output_video) or not os.path.exists(output_json):
        return jsonify({"status": "error", "message": "Generation did not produce expected outputs."}), 500

    # Build URLs for the generated assets and the interactive page
    host = request.host_url.rstrip('/')
    video_url = f"/generated/{job_id}/MonsterDubs.mp4"
    json_url = f"/generated/{job_id}/interactive_subs.json"
    page_url = f"/subtitles/?video={video_url}&json={json_url}"

    return jsonify({
        "status": "success",
        "job_id": job_id,
        "video_url": video_url,
        "json_url": json_url,
        "page_url": page_url,
        "absolute_page_url": f"{host}{page_url.lstrip('/')}"
    })

@app.route("/generated/<job_id>/<path:filename>")
def serve_generated(job_id, filename):
    job_dir = os.path.join(GENERATED_DIR, secure_filename(job_id))
    return send_from_directory(job_dir, filename)

@app.route("/generate_subtitles")
def get_dubbed_video():
    # Legacy endpoint serving a static demo file
    video_folder = os.path.join(BASE_DIR, "subtitles")
    video_filename = "MonsterDubs.mp4"
    return send_from_directory(video_folder, video_filename)

@app.route("/subtitles/")
@app.route("/subtitles/<path:filename>")
def serve_subtitles(filename=None):
    """Serve files from the subtitles folder"""
    if filename is None:
        # Serve index.html for the root subtitles path
        return send_from_directory(SUBTITLES_DIR, "index.html")
    else:
        # Serve specific files from subtitles folder
        return send_from_directory(SUBTITLES_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
