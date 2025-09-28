#!/usr/bin/env python3

import subprocess
import json
import sys
from pathlib import Path

CHANNELS_FILE = Path("channels.json")


def load_channels():
    if CHANNELS_FILE.exists():
        with open(CHANNELS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_channels(channels):
    with open(CHANNELS_FILE, "w") as f:
        json.dump(channels, f, indent=2)


def choose_from_fzf(options: list, prompt="Choose:"):
    if not options:
        return None
    try:
        fzf = subprocess.run(["fzf", "--prompt", prompt],
                             input="\n".join(options),
                             text=True, capture_output=True)
        return fzf.stdout.strip()
    except FileNotFoundError:
        print("⚠️ fzf not found, using fallback.")
        for i, option in enumerate(options):
            print(f"{i + 1}: {option}")
        choice = input("Enter number: ")
        try:
            return options[int(choice) - 1]
        except:
            return None


def search_youtube_channels(query: str, max_results=5):
    print(f"🔎 Searching YouTube for channels matching: {query}")
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--print", "%(uploader)s | %(channel_url)s",
        "--skip-download"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    channels = {}

    for line in result.stdout.strip().splitlines():
        if "|" in line:
            name, url = [s.strip() for s in line.split("|", 1)]
            channels[name] = url

    return channels


def list_channel_videos(channel_url, max_videos=10):
    # Force the "videos" tab of the channel
    if not channel_url.endswith("/videos"):
        channel_url = channel_url.rstrip("/") + "/videos"

    print(f"📺 Fetching last {max_videos} videos from {channel_url}")
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--playlist-end", str(max_videos),
        channel_url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    videos = []
    for line in result.stdout.strip().splitlines():
        try:
            entry = json.loads(line)
            videos.append({
                "title": entry.get("title"),
                "id": entry.get("id"),
                "url": entry.get("webpage_url")
            })
        except json.JSONDecodeError:
            continue

    return videos


def play_with_mpv(video_url):
    print(f"🎬 Streaming {video_url} with mpv...")
    subprocess.run(["mpv", video_url])


def main():
    while True:
        channels = load_channels()

        # Always offer the "search" option
        saved_channel_names = list(channels.keys())
        choices = saved_channel_names + ["➕ Search for a new channel", "🚪 Exit"]

        selected = choose_from_fzf(choices, prompt="Channel> ")
        if not selected or selected == "🚪 Exit":
            print("👋 Exiting.")
            return

        if selected == "➕ Search for a new channel":
            query = input("Enter channel name to search: ")
            search_results = search_youtube_channels(query)

            if not search_results:
                print("❌ No channels found.")
                continue

            new_channel = choose_from_fzf(list(search_results.keys()), prompt="Add which channel> ")
            if not new_channel:
                print("❌ No channel selected.")
                continue

            url = search_results[new_channel]
            print(f"✅ Added: {new_channel} -> {url}")
            channels[new_channel] = url
            save_channels(channels)
            selected_channel_url = url
        else:
            selected_channel_url = channels[selected]

        # 🔁 Only fetch videos once per channel
        videos = list_channel_videos(selected_channel_url)
        if not videos:
            print("❌ No videos found.")
            continue

        while True:
            video_choices = [f"{v['title']} | {v['url']}" for v in videos]
            video_choices.append("⬅️ Back to channels")
            selected_video = choose_from_fzf(video_choices, prompt="Video> ")
            if not selected_video or selected_video == "⬅️ Back to channels":
                break

            video_url = selected_video.split("|")[-1].strip()
            play_with_mpv(video_url)


if __name__ == "__main__":
    main()
