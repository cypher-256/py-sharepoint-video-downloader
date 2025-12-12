#!/usr/bin/env python3
#./download.py
import argparse
from pathlib import Path
from urllib.parse import urlparse
import yt_dlp

def shorten_url(url: str) -> str:
    key = 'index&format=dash'
    idx = url.find(key)
    if idx == -1:
        raise ValueError("No se encontró 'index&format=dash' en la URL.")
    return url[:idx + len(key)]

def build_downloader_opts(fast: bool):
    opts = {
        'format': 'vcopy+audcopy/best',
        'merge_output_format': 'mp4',
        'ignoreerrors': False,

        'retries': 20,
        'fragment_retries': 20,
        'retry_sleep_functions': {'fragment': lambda n: min(2**n, 10)},

        'nopart': True,

        # timeouts para evitar colgados por fragmento
        'socket_timeout': 30,
    }

    if not fast:
        return opts
    
    
    opts['concurrent_fragments'] = 4
    opts['prefer_insecure'] = False
    opts['enable_file_urls'] = False
    opts['http_client'] = 'curl_cffi'
    opts['verbose'] = True

    return opts

def download_with_yt_dlp(url: str, output: str, opts: dict):
    opts = opts | {'outtmpl': output}
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

def main():
    p = argparse.ArgumentParser(description="Descarga grabaciones Teams/Stream")
    p.add_argument("manifest_file")
    p.add_argument("-o", "--output", default="output.mp4")
    p.add_argument("--no-fast", action="store_true")
    args = p.parse_args()

    raw_url = Path(args.manifest_file).read_text().strip()
    short_url = shorten_url(raw_url)

    # Solo aplicamos modo rápido si el host es *.svc.ms
    host = urlparse(short_url).hostname or ''
    fast_mode = (not args.no_fast) and host.endswith('svc.ms')

    print(f"Descargando desde: {short_url}")
    opts = build_downloader_opts(fast_mode)
    download_with_yt_dlp(short_url, args.output, opts)
    print(f"Descarga completada: {args.output}")

if __name__ == "__main__":
    main()
