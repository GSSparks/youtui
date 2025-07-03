
```
__     ______  _    _ _____ _    _ _____ 
\ \   / / __ \| |  | |_   _| |  | |_   _|
 \ \_/ / |  | | |  | | | | | |  | | | |  
  \   /| |  | | |  | | | | | |  | | | |  
   | | | |__| | |__| | | | | |__| |_| |_ 
   |_|  \____/ \____/  |_| |_____/|_____| Terminal YouTube Player
```
# YouTUI 🎥📺
**YouTUI** is a terminal-based YouTube browser and player. Save your favorite channels, browse recent videos, and stream them seamlessly with `mpv` — all from the comfort of your terminal.

---

## ✨ Features

- 🔍 Search YouTube channels by name
- 💾 Save favorite channels for future use
- 📺 Browse the latest 10 videos per channel
- 🎬 Stream videos directly using `mpv`
- ⚡ Fast fuzzy selection with `fzf`
- 🧠 Remembers your choices using `channels.json`

---

## 📦 Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [mpv](https://mpv.io)
- [fzf](https://github.com/junegunn/fzf)

## Install dependencies:

```bash
sudo apt install mpv fzf
pip install yt-dlp
```

🚀 Usage
```bash
python youtui.py
```

## Keyboard Controls
- Use fzf to navigate channel and video lists
- Enter to select
- q in mpv to quit video and return to menu

## 📁 channels.json
Your saved channels are stored in a simple JSON file like:

```json
{
  "DistroTube": "https://www.youtube.com/c/DistroTube",
  "NPR Music": "https://www.youtube.com/c/nprmusic"
}
```

## 🧱 Roadmap Ideas
- Add video duration & upload date to menu
- Support autoplay playlists
- Add channel thumbnails (using ueberzugpp)
- Export/import saved channels
- Optional video download

## 💡 License
MIT — free to use, improve, and share.

Built by a Linux terminal enjoyer 😎
