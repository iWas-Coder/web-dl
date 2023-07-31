"""
Downloader Module
~~~~~~~~~~~~~~~~

(...)
"""

import os
import sys
import time
import glob
import modules.assets as assets
from pwn import *


def is_encrypted(url: str) -> bool:
    """
    (...)
    """
    
    p_check = log.progress("DRM Check")
    p_check.status("Checking if content is protected (DRM)...")
    time.sleep(2)
    
    status = os.system(f"curl -s '{url}' | grep 'ContentProtection' &>/dev/null")
    # Check status code of previous system-level command
    if status == 0:
        p_check.failure("The content is DRM protected :(")
        time.sleep(2)
        return True
    else:
        p_check.success("The content is not protected :D")
        time.sleep(2)
        return False


def get_enc_content(url: str) -> None:
    """
    (...)
    """
    
    p_video = log.progress("Video")
    p_audio = log.progress("Audio")
    
    p_video.status("Downloading encrypted video files from CDN...")
    os.system(f"yt-dlp --no-warnings --allow-unplayable-formats -f bv '{url}' -o \"{assets.CACHE_DIR}/video.enc.%(ext)s\"")
    p_audio.status("Downloading encrypted audio files from CDN...")
    os.system(f"yt-dlp --no-warnings --allow-unplayable-formats -f ba '{url}' -o \"{assets.CACHE_DIR}/audio.enc.%(ext)s\"")
    
    failed = 0

    if glob.glob(f"{assets.CACHE_DIR}/video.enc.*"):
        p_video.success("Done!")
    else:
        p_video.failure("Video download failed :(")
        failed += 1
    
    if glob.glob(f"{assets.CACHE_DIR}/audio.enc.*"):
        p_audio.success("Done!")
    else:
        p_audio.failure("Audio download failed :(")
        failed += 1

    if failed > 0:
        delete_cache()
        sys.exit(1)


def get_content(url: str) -> None:
    """
    (...)
    """
    
    p_video = log.progress("Video")
    p_audio = log.progress("Audio")
    
    p_video.status("Downloading video files from CDN...")
    os.system(f"yt-dlp --no-warnings -f bv '{url}' -o \"{assets.CACHE_DIR}/video.%(ext)s\"")
    p_audio.status("Downloading audio files from CDN...")
    os.system(f"yt-dlp --no-warnings -f ba '{url}' -o \"{assets.CACHE_DIR}/audio.%(ext)s\"")
    
    failed = 0

    if glob.glob(f"{assets.CACHE_DIR}/video.*"):
        p_video.success("Download successfully :)")
    else:
        p_video.failure("Download failed :(")
        failed += 1
    
    if glob.glob(f"{assets.CACHE_DIR}/audio.*"):
        p_audio.success("Download successfully :)")
    else:
        p_audio.failure("Download failed :(")
        failed += 1

    if failed > 0:
        delete_cache()
        sys.exit(1)


def merge(output: str) -> bool:
    """
    (...)
    """
    
    p_merge = log.progress("Merge")
    p_merge.status("Merging video and audio files...")
    time.sleep(2)
    
    status = os.system(f"ffmpeg -loglevel quiet -i \"{assets.CACHE_DIR}/video.mp4\" -i \"{assets.CACHE_DIR}/audio.m4a\" -c:v copy -c:a copy \"{output}\"")
    if status == 0:
        p_merge.success("Content merged correctly!")
        log.info(f"Result: {output}")
        return True
    else:
        p_merge.failure("Content cannot be merged due to errors :(")
        log.warning("Cache files (downloaded content) has not been removed and, thus, can be found under 'cache/' directory.")
        return False


def delete_cache() -> None:
    """
    (...)
    """
    
    os.system("rm -rf ./cache/")
