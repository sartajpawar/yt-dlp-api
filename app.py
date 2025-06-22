from flask import Flask, request, jsonify
import yt_dlp
import uuid
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get("video_url")

    if not url:
        return jsonify({"error": "Missing video_url"}), 400

    video_id = str(uuid.uuid4())
    filename = f"{video_id}.mp4"

    ydl_opts = {
        'outtmpl': filename,
        'format': 'best[ext=mp4]'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({
            "id": video_id,
            "file_path": filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
