import urllib.request

import pandas as pd


TRAIN_URL = "https://storage.googleapis.com/maps-premium/dataset/yes_complete/train.txt"
SONG_HASH_URL = "https://storage.googleapis.com/maps-premium/dataset/yes_complete/song_hash.txt"


def download_text(url: str) -> str:
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def load_playlists(text: str):
    lines = text.split("\n")[2:]
    playlists = [line.rstrip().split() for line in lines if line.strip()]
    return [playlist for playlist in playlists if len(playlist) > 1]


def load_song_metadata(text: str) -> pd.DataFrame:
    rows = [
        [field.strip() for field in line.split("\t")]
        for line in text.split("\n")
        if line.strip()
    ]
    songs = pd.DataFrame(rows, columns=["id", "title", "artist"])
    return songs.set_index("id")


if __name__ == "__main__":
    print("Downloading playlists...")
    playlists = load_playlists(download_text(TRAIN_URL))
    print(f"Loaded {len(playlists)} playlists with more than one song")

    print("Downloading song metadata...")
    songs = load_song_metadata(download_text(SONG_HASH_URL))
    print(f"Loaded metadata for {len(songs)} songs")

    print(songs.head())
    print(playlists[0][:10])
