#!/usr/bin/env python3

import modules.args as args
import modules.assets as assets
import modules.downloader as downloader
import modules.decryptor as decryptor


# === Ctrl+C === #
assets.ctrl_c()

# === MAIN === #
def main():
    """
    Main program flow.
    """
    
    # Banner
    assets.banner(); assets.divider()
    # Arguments
    args.init_args()
    # Hide cursor
    assets.cursor_hide()
    
    # Download content
    downloader.get_content(args.url())
    # Extract KID, PR_PSSH, WV_PSSH, KEY
    decryptor.extract_keys()
    # Decrypt content
    decryptor.decrypt()
    # Merge video & audio files
    downloader.merge()
    # Delete cache files
    downloader.delete_cache()
    
    # Show cursor
    assets.cursor_show()
    

if __name__ == "__main__":
    main()
