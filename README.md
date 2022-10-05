# WEB-DL - Downloader & Decryptor for MPD Streams through CDN's

### Dependencies
It is required to have both `ffmpeg` and `mp4decrypt` installed and fully accessible in the system.

Also, ensure that all needed python3 requirements are met doing:
```console
pip3 install -r requirements.txt
```

### Documentation
Visit the project's [wiki](https://github.com/iWas-Coder/web-dl/wiki) to see how things work in a much deeper explanation.

### Usage
- `-u` / `--url`: Input the URL or PATH to the MPD manifest of the desired stream.
- `-o` / `--output`: Input the final name that we want the target file to have; it is recommended to include a file extension (e.g. `test.mkv`).
