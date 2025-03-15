YouTube Audio Downloader
===================
Overview
---
YouTube Audio Downloader is a Python-based command-line tool that allows users to download audio from YouTube videos in various formats, including MP3, WAV, and FLAC. It features an interactive menu with arrow key navigation for selecting the preferred language and audio format. The tool is built as an extension over yt-dlp, a powerful command-line utility for downloading media from various websites.

Features
---
- Interactive UI – Navigate menus using arrow keys to select language and format.
- Multiple Audio Formats – Supports MP3, WAV, and FLAC.
- Fully Local Dependencies – No need for global installations; everything runs within the project folder.
- Cross-Platform – Works on Windows, macOS, and Linux.
- Built on yt-dlp – Leverages yt-dlp for fast and reliable YouTube downloads.

Installation
---
**1. Clone the Repository**
```bash
git clone https://github.com/ZoomCH02/youtube-to-audio.git
cd youtube-to-audio
```

**2. Set Up a Virtual Environment**
```bash
python -m venv venv
```
**3. Activate the Virtual Environment**
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

**4. Install Dependencies**
```bash
pip install -r requirements.txt
```

**5. Download yt-dlp Locally**
- Windows:
```bash
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -o yt-dlp.exe
```
- macOS/Linux:
```bash
wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O yt-dlp
chmod +x yt-dlp
```

**6. Download FFmpeg**
FFmpeg is needed for processing audio and video. 
### Windows
1. [Download FFmpeg](https://ffmpeg.org/download.html)
2. Add to `PATH`
### Linux (Ubuntu/Debian)
```sh
sudo apt install ffmpeg
```

Usage
---
Running the Program

```bash
python main.py
```

Steps:

- Select a language (ru or en) using arrow keys and press Enter.
- Enter the URL of the YouTube video.
- Choose the desired audio format (mp3, wav, flac).
- The tool will download and convert the audio file automatically.

Dependencies
---

- Python 3.8+
- yt-dlp (locally downloaded)
- readchar (for keyboard input handling)

Notes
---

- This tool does not bypass YouTube restrictions.
- The project is an extension over yt-dlp and does not modify its core functionality.
- If encountering issues, ensure yt-dlp is up to date by manually re-downloading it.

License
---
This project is licensed under the MIT License.

Contributing
---
Feel free to submit issues or pull requests to improve the project.

Acknowledgments
---
Special thanks to the yt-dlp team for their amazing work in developing a robust media downloader.



