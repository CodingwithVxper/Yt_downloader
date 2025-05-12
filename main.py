import argparse
import os
import re
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


def valid_youtube_url(url):
    """Simple check to validate if the input is a YouTube URL."""
    pattern = r'^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}$'
    return re.match(pattern, url) is not None


def get_default_resolution():
    """Return the default resolution."""
    return {
        "resolution": "720"
    }


def download(url, output_path, resolution):
    """Download YouTube video using yt-dlp"""
    def progress(d):
        if 'filename' in d and os.path.exists(d['filename']):
            print(" Already downloaded")
            return
        if not valid_youtube_url(url):
            print(" Download failed: Invalid YouTube URL")
            return
        if valid_youtube_url(url) and not 'filename' in d and os.path.exists(d['filename']):
            os.makedirs(output_path, exist_ok=True)
            print(
                f"Downloading video to: {os.path.abspath(output_path)} with a resolution of {resolution}p")

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': f'best[ext=mp4][height<={resolution}]',
        'progress_hooks': [progress],
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as e:
        print(f"Download failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download YouTube videos with progress bar")
    parser.add_argument("--url", type=str, required=True,
                        help="YouTube video URL")
    parser.add_argument("--resolution", default=get_default_resolution().get("resolution", "720"),
                        help="Resolution (e.g., 480, 720)")
    parser.add_argument("--output_path", type=str, default=".",
                        help="Output directory (default: current folder)")
    args = parser.parse_args()

    download(args.url, args.output_path, args.resolution)
