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
    
    p = log.progress("Download")
    
    p.status("Downloading and merging encrypted files...")
    time.sleep(2)
    os.system("ffmpeg -v quiet -stats" +
             f"-i \"{url}\" " +
              "-c copy " +
             f"{assets.CACHE_DIR}/video.enc.mkv")
    
    video_path = f"{assets.CACHE_DIR}/encrypted_video.mp4"
    audio_path = f"{assets.CACHE_DIR}/encrypted_audio.m4a"
    
    p.success("Done!")


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