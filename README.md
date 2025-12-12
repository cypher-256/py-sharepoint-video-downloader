# py-sharepoint-video-downloader

Python helper to download Microsoft Teams / SharePoint recordings using DASH
`videomanifest` URLs exposed in the browser.

This tool relies on `yt-dlp` and `ffmpeg`.  
It does **not** bypass authentication, DRM, or access controls.

---

## What this does

This script downloads Microsoft Teams / SharePoint recordings by directly
consuming the DASH `videomanifest` URL that the web player uses internally.

It works only for videos that:
- You are already authorized to view in your browser
- Are delivered as DASH streams (`videomanifest`)

The script simply automates what the browser already does.

---

## Requirements

- Python **3.9+**
- `yt-dlp`
- `ffmpeg` available in `PATH`

Example setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install yt-dlp
````
Example setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install yt-dlp
````
## How to obtain the videomanifest URL

1. Open the video in **SharePoint or Microsoft Teams (web)**.
2. Open **Chrome DevTools**.
3. Go to the **Network** tab.
4. Filter requests by `videomanifest`.
5. Copy the request URL.
6. **Truncate the URL** so it ends exactly at:

```
part=index&format=dash
```

> Important:
> These URLs are **time-limited**. If the download fails with 403/404 errors,
> reload the page and copy a fresh URL.

---

## Usage

Save the `videomanifest` URL into a text file (for example `videomanifest.txt`).

Then run:

```bash
python download.py videomanifest.txt -o output.mp4
```

* `videomanifest.txt` must contain **only the URL**
* The default output container is **MP4**

---

## Performance limitations (important)

Microsoft applies **aggressive server-side throttling**, especially on
**audio DASH streams**.

Observed behavior:

* Video usually downloads at ~0.8–1.2 MB/s
* Audio can be throttled to **<100 KB/s**
* Increasing fragment concurrency often results in:

  * HTTP 503 errors
  * Read timeouts
  * Worse overall performance

This is a **Microsoft CDN limitation**, not a bug in the script.

---

## Notes on parallelism

The script enables DASH fragment parallelism when supported by the server.
However, Microsoft’s CDN often collapses parallel requests into a single
effective connection for audio streams.

Do not expect linear speedups by increasing concurrency.

---

## License

MIT License
