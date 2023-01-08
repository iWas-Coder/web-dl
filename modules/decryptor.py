"""
Decryptor Module
~~~~~~~~~~~~~~~~

(...)
"""

import urllib.request
import xmltodict
from pprint import pprint
from pwn import *


def extract_keys(url: str):
    """
    (...)
    """
    
    # Parsing XML to JSON Object
    mpd_obj = xmltodict.parse(urllib.request.urlopen(url).read())['MPD']['Period'][1]['AdaptationSet']
    video_keys = {}
    audio_keys = {}
    
    # Extracting KID, PR_PSSH and WV_PSSH
    video_keys["KID"] = mpd_obj[0]['ContentProtection'][0]['@cenc:default_KID'].replace('-', '').lower()
    video_keys["PR_PSSH"] = mpd_obj[0]['ContentProtection'][1]['cenc:pssh']
    video_keys["WV_PSSH"] = mpd_obj[0]['ContentProtection'][2]['cenc:pssh']
    audio_keys["KID"] = mpd_obj[1]['ContentProtection'][0]['@cenc:default_KID'].replace('-', '').lower()
    audio_keys["PR_PSSH"] = mpd_obj[1]['ContentProtection'][1]['cenc:pssh']
    audio_keys["WV_PSSH"] = mpd_obj[1]['ContentProtection'][2]['cenc:pssh']
    
    # Logging extracted info
    info("\033[1m" + "\033[4m" + "(video) KID:" + "\033[0m " + video_keys['KID'])
    info("\033[1m" + "\033[4m" + "(video) Microsoft PlayReady PSSH:" + "\033[0m " + video_keys['PR_PSSH'])
    info("\033[1m" + "\033[4m" + "(video) Google Widevine PSSH:" + "\033[0m " + video_keys['WV_PSSH'])
    info("\033[1m" + "\033[4m" + "(audio) KID:" + "\033[0m " + audio_keys['KID'])
    info("\033[1m" + "\033[4m" + "(audio) Microsoft PlayReady PSSH:" + "\033[0m " + audio_keys['PR_PSSH'])
    info("\033[1m" + "\033[4m" + "(audio) Google Widevine PSSH:" + "\033[0m " + audio_keys['WV_PSSH'])
    
    return video_keys, audio_keys


def decrypt():
    pass
