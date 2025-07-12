from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "✅ API server is live on Render -TLX!"

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    video_id = str(uuid.uuid4())[:8]
    output_path = f"{DOWNLOAD_DIR}/{video_id}.mp4"

    try:
        subprocess.run(["yt-dlp", "-f", "best", "-o", output_path, url], check=True)
        return jsonify({"status": "success", "file": output_path})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": e.stderr}), 500
