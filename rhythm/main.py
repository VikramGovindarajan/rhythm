import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class Song:
    def __init__(self, path, title=None, artist=None, album=None, genre=None, year=None):
        self.path = path
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year

    def __repr__(self):
        return f"<Song: {self.title or 'Unknown'} - {self.artist or 'Unknown'}>"

class MusicCollection:
    def __init__(self, directory):
        self.songs = []
        self.load_songs(directory)

    def load_songs(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                path = os.path.join(directory, file)
                try:
                    audio = MP3(path, ID3=EasyID3)
                    song = Song(
                        path=path,
                        title=audio.get("title", [None])[0],
                        artist=audio.get("artist", [None])[0],
                        album=audio.get("album", [None])[0],
                        genre=audio.get("genre", [None])[0],
                        year=audio.get("date", [None])[0],
                    )
                except Exception as e:
                    print(f"Error reading {file}: {e}")
                    song = Song(path=path)
                self.songs.append(song)

    def __repr__(self):
        return f"<MusicCollection: {len(self.songs)} songs>"

# Entry point for the module
def load_collection(directory="."):
    return MusicCollection(directory)
