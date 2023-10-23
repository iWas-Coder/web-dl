"""
Decryptor Module
~~~~~~~~~~~~~~~~

(...)
"""

import requests
import xml.etree.ElementTree as ET
from pprint import pprint
from pwn import *
from itertools import tee
import modules.assets as assets
import os


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def extract_keys(url: str):
    """
    (...)
    """

    assets.divider()
    
    # Parsing XML
    xml_file = requests.get(url).content
    xml_root = ET.fromstring(xml_file)
    
    # Periods handling
    periods = xml_root.findall("{urn:mpeg:dash:schema:mpd:2011}Period")

    # ISSUE #5: 'duration' KeyError. There is no argument in the period(s).
    # In this case, if len(periods) == 1, do not care at all about the duration of the period.
    # If there are multiple periods, then they should have a duration attribute; if not, pick the first one (and log it).
    if len(periods) == 1:
        selected_period_idx = 0
        info(f"Selected Period: {selected_period_idx}")
    else:
        durations = []
        for period in periods:
            if 'H' in period.attrib['duration']:
                duration_h = int(''.join(period.attrib['duration'].split('PT')[1].split('H')[0]))
                duration_m = int(''.join(period.attrib['duration'].split('H')[1].split('M')[0]))
                duration_s = int(float(''.join(period.attrib['duration'].split('M')[1].split('S')[0])))
            elif 'M' in period.attrib['duration']:
                duration_h = 0
                duration_m = int(''.join(period.attrib['duration'].split('PT')[1].split('M')[0]))
                duration_s = int(float(''.join(period.attrib['duration'].split('M')[1].split('S')[0])))
            elif 'S' in period.attrib['duration']:
                duration_h = 0
                duration_m = 0
                duration_s = int(float(''.join(period.attrib['duration'].split('PT')[1].split('S')[0])))
            else:
                duration_h = 0
                duration_m = 0
                duration_s = 0

                durations.append({
                    'H': duration_h,
                    'M': duration_m,
                    'S': duration_s
                })

        # Period selection
        for n, i in enumerate(durations):
            info(f"Period #{n}: ({i['H']}:{i['M']}:{i['S']})")
        if len(durations) > 1:
            biggest = None
            for i, j in pairwise(durations):
                if i['H'] > j['H']: biggest = i
                elif i['H'] < j['H']: biggest = j
                else:
                    if i['M'] > j['M']: biggest = i
                    elif i['M'] < j['M']: biggest = j
                    else:
                        if i['S'] > j['S']: biggest = i
                        elif i['S'] < j['S']: biggest = j
                        else:
                            raise Exception("Two periods with same duration! :O")
                        selected_period_idx = durations.index(biggest)
        else:
            selected_period_idx = 0
            info(f"Selected Period: {selected_period_idx}")

    assets.divider()
    
    # AdaptationSets handling
    adaptationsets = periods[selected_period_idx].findall("{urn:mpeg:dash:schema:mpd:2011}AdaptationSet")
    adaptationsets_video = []
    adaptationsets_audio = []
    for n, adaptationset in enumerate(adaptationsets):
        if all(key in adaptationset.attrib for key in ["maxWidth", "maxHeight"]):
            info(f"AdaptationSet #{n}: (video, {adaptationset.attrib['maxWidth']}x{adaptationset.attrib['maxHeight']})")
            adaptationsets_video.append((n, adaptationset))
        elif all(key in adaptationset.attrib for key in ["maxWidth", "maxHeight", "maxFrameRate"]):
            info(f"AdaptationSet #{n}: (video, {adaptationset.attrib['maxWidth']}x{adaptationset.attrib['maxHeight']}@{adaptationset.attrib['maxFrameRate']})")
            adaptationsets_video.append((n, adaptationset))
        elif all(key in adaptationset.attrib for key in ["lang", "maxBandwidth", "minBandwidth"]):
            info(f"AdaptationSet #{n}: (audio, {adaptationset.attrib['lang']} @ [{adaptationset.attrib['minBandwidth']}, {adaptationset.attrib['maxBandwidth']}])")
            adaptationsets_audio.append((n, adaptationset))
        elif "lang" in adaptationset.attrib:
            info(f"AdaptationSet #{n}: (audio, {adaptationset.attrib['lang']})")
            adaptationsets_audio.append((n, adaptationset))
        else:
            info(f"AdaptationSet #{n}: (?)")

    # AdaptationSet selection
    if len(adaptationsets_video) > 1:
        selected_adaptationset_video_idx = adaptationsets_video[0][0]
        # TODO: Smart video selection
        pass
    else:
        selected_adaptationset_video_idx = adaptationsets_video[0][0]
        info(f"Selected AdaptationSet (video): {selected_adaptationset_video_idx}")
    if len(adaptationsets_audio) > 1:
        selected_adaptationset_audio_idx = adaptationsets_audio[0][0]
        # TODO: Smart audio selection
        pass
    else:
        selected_adaptationset_audio_idx = adaptationsets_audio[0][0]
        info(f"Selected AdaptationSet (audio): {selected_adaptationset_audio_idx}")

    assets.divider()

    # KID, PR_PSSH, WV_PSSH extraction (video)
    video_keys = {}
    video_contentprotections = adaptationsets[selected_adaptationset_video_idx].findall("{urn:mpeg:dash:schema:mpd:2011}ContentProtection")
    
    # ISSUE #5: It does not pickup the 'ContentProtection' objects, because they are not directly under the 'AdaptationSet' object,
    # they are however under a 'Representation' object, inside the 'AdaptationSet'.
    if not video_contentprotections:
        representations = adaptationsets[selected_adaptationset_video_idx].findall("{urn:mpeg:dash:schema:mpd:2011}Representation")
        video_contentprotections = representations[0].findall("{urn:mpeg:dash:schema:mpd:2011}ContentProtection")
    
    for video_contentprotection in video_contentprotections:
        if "{urn:mpeg:cenc:2013}default_KID" in video_contentprotection.attrib:
            video_keys["KID"] = video_contentprotection.attrib["{urn:mpeg:cenc:2013}default_KID"].replace('-', '').lower()
            info(f"KID (video): {video_keys['KID']}")
            # ISSUE #5: The PSSH value happens to be inside the object with the KID attribute.
            for child in video_contentprotection:
                if child.tag == "{urn:mpeg:cenc:2013}pssh":
                    video_keys["PSSH"] = child.text
                    info(f"PSSH (video): {video_keys['PSSH']}")
        elif "value" in video_contentprotection.attrib and video_contentprotection.attrib["value"] == "MSPR 2.0":
            for child in video_contentprotection:
                if child.tag == "{urn:mpeg:cenc:2013}pssh":
                    video_keys["PR_PSSH"] = child.text
                    info(f"PR_PSSH (video): {video_keys['PR_PSSH']}")
        else:
            for child in video_contentprotection:
                if child.tag == "{urn:mpeg:cenc:2013}pssh":
                    video_keys["WV_PSSH"] = child.text
                    info(f"WV_PSSH (video): {video_keys['WV_PSSH']}")

    # KID, PR_PSSH, WV_PSSH extraction (audio)
    audio_keys = {}
    audio_contentprotections = adaptationsets[selected_adaptationset_audio_idx].findall("{urn:mpeg:dash:schema:mpd:2011}ContentProtection")

    # ISSUE #5: It does not pickup the 'ContentProtection' objects, because they are not directly under the 'AdaptationSet' object,
    # they are however under a 'Representation' object, inside the 'AdaptationSet'.
    if not audio_contentprotections:
        representations = adaptationsets[selected_adaptationset_audio_idx].findall("{urn:mpeg:dash:schema:mpd:2011}Representation")
        audio_contentprotections = representations[0].findall("{urn:mpeg:dash:schema:mpd:2011}ContentProtection")
    
    for audio_contentprotection in audio_contentprotections:
        if "{urn:mpeg:cenc:2013}default_KID" in audio_contentprotection.attrib:
            audio_keys["KID"] = audio_contentprotection.attrib["{urn:mpeg:cenc:2013}default_KID"].replace('-', '').lower()
            info(f"KID (audio): {audio_keys['KID']}")
            # ISSUE #5: The PSSH value happens to be inside the object with the KID attribute.
            for child in audio_contentprotection:
                if child.tag == "{urn:mpeg:cenc:2013}pssh":
                    audio_keys["PSSH"] = child.text
                    info(f"PSSH (audio): {audio_keys['PSSH']}")
        elif "value" in audio_contentprotection.attrib and audio_contentprotection.attrib["value"] == "MSPR 2.0":
            for child in audio_contentprotection:
                if child.tag == "{urn:mpeg:cenc:2013}pssh":
                    audio_keys["PR_PSSH"] = child.text
                    info(f"PR_PSSH (audio): {audio_keys['PR_PSSH']}")
        else:
            for child in audio_contentprotection:
                if child.tag == "{urn:mpeg:cenc:2013}pssh":
                    audio_keys["WV_PSSH"] = child.text
                    info(f"WV_PSSH (audio): {audio_keys['WV_PSSH']}")

    assets.divider()
    return video_keys, audio_keys


def decrypt(video_keys: dict, audio_keys: dict):
    # os.system("mv ./cache/video.enc.mp4 ./cache/video.mp4")
    # os.system("mv ./cache/audio.enc.m4a ./cache/audio.m4a")
    pass
