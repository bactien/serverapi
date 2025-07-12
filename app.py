from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"

# Tạo thư mục nếu chưa tồn tại
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "✅ Server is running. Use POST /download to get started!"

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json(force=True)
        url = data.get("url")

        if not url:
            return jsonify({"status": "error", "message": "Thiếu URL video."}), 400

        # Tạo tên file ngẫu nhiên để tránh trùng
        output_name = os.path.join(DOWNLOAD_DIR, str(uuid.uuid4()))

        # Lệnh yt-dlp tải video MP4 tốt nhất
        command = [
            "yt-dlp",
            "-f", "best[ext=mp4]/best",
            "-o", f"{output_name}.%(ext)s",
            url
        ]

        # Thực thi
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Tải video thất bại.",
                "error_detail": result.stderr
            }), 500

        # Tìm file đã tải
        downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(os.path.basename(output_name))]
        if not downloaded_files:
            return jsonify({"status": "error", "message": "Không tìm thấy file đã tải."}), 500

        return jsonify({
            "status": "success",
            "message": "Tải video thành công!",
            "filename": downloaded_files[0]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

