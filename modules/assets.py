import os
import sys
import signal


BANNER = """
 _       ____________        ____  __ 
| |     / / ____/ __ )      / __ \/ /     Downloader & Decryptor for MPD Streams
| | /| / / __/ / __  |_____/ / / / /      through CDN's
| |/ |/ / /___/ /_/ /_____/ /_/ / /___
|__/|__/_____/_____/     /_____/_____/                  (by iWas <3)
"""

CWD = os.getcwd()
CACHE_DIR = CWD + "/cache"
OUT_DIR = CWD + "/out"

VIDEO_ID = "bv"
AUDIO_ID = "ba"

# === Lambda/Arrow function definitions === #
cursor_hide = lambda: print('\033[? 25l', end="")
cursor_show = lambda: print('\033[? 25h', end="")
banner = lambda: print(BANNER)
divider = lambda: print('\u2500' * 10)
err = lambda txt: print(f"[-] {txt}")
log = lambda txt: print(f"[+] {txt}")
done = lambda txt: print(f"[*] {txt}")

# === Function definitions === #
def ctrl_c():
    """
    Catching and handling any KeyboardInterrupt ('SIGINT' code) sent by the user
    when a Ctrl+C is performed at any time during the execution of the script.
    """
    
    def def_handler(sig, frame):
        err("Process cancelled by user\n")
        cursor_show()
        sys.exit(1)
    
    signal.signal(signal.SIGINT, def_handler)
