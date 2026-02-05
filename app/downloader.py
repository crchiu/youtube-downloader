import subprocess
import os
import uuid

DOWNLOAD_DIR = "/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube(url: str, fmt: str, task_id: str) -> str:
    output_template = f"{DOWNLOAD_DIR}/{task_id}.%(ext)s"

    if fmt == "mp4":
        cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "-o", output_template,
            url
        ]
    elif fmt == "mp3":
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_template,
            url
        ]
    else:
        raise ValueError("Unsupported format")

    subprocess.run(cmd, check=True)
    return f"{task_id}.{fmt}"
