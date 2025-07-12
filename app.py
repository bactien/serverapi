from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "✅ Server is running!"

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    video_id = str(uuid.uuid4())[:8]
    output_path = f"{DOWNLOAD_DIR}/{video_id}.mp4"

    try:
        cmd = ["yt-dlp", "-f", "best", "-o", output_path, url]
        subprocess.run(cmd, check=True)
        return jsonify({"status": "success", "file": output_path})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "error": str(e)}), 500
