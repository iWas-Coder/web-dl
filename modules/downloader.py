"""
Downloader Module
~~~~~~~~~~~~~~~~

(...)
"""

import os
import time
from pwn import *
from .import assets


def get_content(url: str):
    """
    (...)
    """
    
    p = log.progress("CDN")
    
    p.status("Downloading encrypted video files...")
    time.sleep(2)
    os.system("yt-dlp " +
              "--external-downloader aria2c " +
              "--no-warnings " +
              "--allow-unplayable-formats " +
              "--no-check-certificate " +
             f"-f {assets.VIDEO_ID} \"{url}\" " +
             f"-o \"{assets.CACHE_DIR}/encrypted_video.%(ext)s\" " +
              ">/dev/null 2>&1")
    
    p.status("Downloading encrypted audio files...")
    time.sleep(2)
    os.system("yt-dlp " +
              "--external-downloader aria2c " +
              "--no-warnings " +
              "--allow-unplayable-formats " +
              "--no-check-certificate " +
             f"-f {assets.AUDIO_ID} \"{url}\" " +
             f"-o \"{assets.CACHE_DIR}/encrypted_audio.%(ext)s\" " +
              ">/dev/null 2>&1")
    
    video_has_downloaded = os.path.isfile(f"{assets.CACHE_DIR}/encrypted_video.*")
    audio_has_downloaded = os.path.isfile(f"{assets.CACHE_DIR}/encrypted_audio.*")
    if video_has_downloaded and audio_has_downloaded:
        p.success("Content downloaded successfully")
    else:
        p.failure("Content not downloaded due to errors")
        sys.exit(1)


def merge():
    """
    (...)
    """
    
    pass


def delete_cache():
    """
    (...)
    """
    
    pass