"""
Downloader Module
~~~~~~~~~~~~~~~~

(...)
"""

import os
import time
from pwn import *
import modules.assets as assets


def get_content(url: str):
    """
    (...)
    """
    
    pv = log.progress("Download Video")
    pa = log.progress("Download Audio")
    
    pv.status("Downloading encrypted video files...")
    time.sleep(2)
    os.system("yt-dlp " +
              "--external-downloader aria2c " +
              "--no-warnings " +
              "--allow-unplayable-formats " +
              "--no-check-certificate " +
             f"-f {assets.VIDEO_ID} \"{url}\" " +
             f"-o \"{assets.CACHE_DIR}/encrypted_video.%(ext)s\" " +
              ">/dev/null 2>&1 &")
    
    pa.status("Downloading encrypted audio files...")
    time.sleep(2)
    os.system("yt-dlp " +
              "--external-downloader aria2c " +
              "--no-warnings " +
              "--allow-unplayable-formats " +
              "--no-check-certificate " +
             f"-f {assets.AUDIO_ID} \"{url}\" " +
             f"-o \"{assets.CACHE_DIR}/encrypted_audio.%(ext)s\" " +
              ">/dev/null 2>&1 &")
    
    video_path = f"{assets.CACHE_DIR}/encrypted_video.mp4"
    video_has_downloaded = os.path.isfile(video_path)
    audio_path = f"{assets.CACHE_DIR}/encrypted_audio.m4a"
    audio_has_downloaded = os.path.isfile(audio_path)
    
    if video_has_downloaded:
        pv.success(f"Content downloaded! ({video_path})")
        if audio_has_downloaded:
            pa.success(f"Content downloaded! ({audio_path})")
        else:
            pa.failure("Content not downloaded due to errors!")
            sys.exit(1)
    else:
        pv.failure("Content not downloaded due to errors!")
        if audio_has_downloaded:
            pa.success(f"Content downloaded! ({audio_path})")
        else:
            pa.failure("Content not downloaded due to errors!")
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