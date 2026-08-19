from gensim.models import Word2Vec

from playlist_dataset import (
    SONG_HASH_URL,
    TRAIN_URL,
    download_text,
    load_playlists,
    load_song_metadata,
)


def train_word2vec(playlists, vector_size=32, window=20, min_count=1, sg=1):
    return Word2Vec(
        sentences=playlists,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        sg=sg,
    )


def most_similar(model, songs, song_id, exclude_artist, topn=5):
    results = []
    for similar_id, score in model.wv.most_similar(song_id, topn=50):
        similar_song = songs.loc[similar_id]
        if similar_song["artist"] == exclude_artist:
            continue
        results.append((similar_song, score))
        if len(results) == topn:
            break
    return results


if __name__ == "__main__":
    print("Downloading playlists...")
    playlists = load_playlists(download_text(TRAIN_URL))

    print("Downloading song metadata...")
    songs = load_song_metadata(download_text(SONG_HASH_URL))

    print(f"Training Word2Vec on {len(playlists)} playlists...")
    model = train_word2vec(playlists)

    song_id = "2172"
    song = songs.loc[song_id]
    print(f"\nMost similar songs to '{song['title']}' by {song['artist']} (excluding {song['artist']}):")

    for similar_song, score in most_similar(model, songs, song_id, exclude_artist=song["artist"], topn=5):
        print(f"{similar_song['title']} - {similar_song['artist']}: {score:.4f}")
