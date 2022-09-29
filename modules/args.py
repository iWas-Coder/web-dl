"""
Arguments Module
~~~~~~~~~~~~~~~~

Adding and parsing all arguments, making them accessible.
"""

import argparse


parser = argparse.ArgumentParser(description = "Downloader & Decryptor for MPD Streams through CDNs")

args = {}
url = lambda: args["url"]
output = lambda: args["output"]

def init_args() -> None:
    """
    Initializes all defined arguments.
    """
    
    # === Adding arguments === #
    parser.add_argument("-u", "--url", help = "MPD file URL", required = True)
    parser.add_argument("-o", "--output", help = "Output file", required = True)
    
    # === Parsing arguments === #
    parsed_args = parser.parse_args()
    
    # === Making arguments accessible through constants === #
    args["url"] = parsed_args.url
    args["output"] = parsed_args.output
