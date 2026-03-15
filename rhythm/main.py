import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from rhythm.db import RhythmDB   # new

class Song:
    def __init__(self, path, title=None, artist=None, album=None, genre=None, year=None):
        self.path = path
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year

    def update_metadata(self, title=None, album=None, genre=None, year=None):
            """Update MP3 tags and internal object"""
            audio = MP3(self.path, ID3=EasyID3)

            if title:
                audio['title'] = title
                self.title = title
            if album:
                audio['album'] = album
                self.album = album
            if genre:
                audio['genre'] = genre
                self.genre = genre
            if year:
                audio['date'] = str(year)
                self.year = year

            audio.save()

    def __repr__(self):
        return f"<Song: {self.title or 'Unknown'} - {self.artist or 'Unknown'}>"

class MusicCollection:
    def __init__(self, directory, db_path=None):

        if db_path is None:
            db_path = os.path.join(directory, "rhythm.db")

        self.db = RhythmDB(db_path)
        self.songs = []
        self.load_songs(directory)
        self.load_from_db()

    def load_songs(self, directory):

      for root, dirs, files in os.walk(directory):

        for file in files:

          if not file.lower().endswith(".mp3"):
            continue

          path = os.path.join(root, file)

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

          self.db.insert_song(song)
      
    def load_from_db(self):
        self.songs.clear()
        rows = self.db.fetch_all_songs()
        for r in rows:
            path, title, artists_str, album, genre, year = r
            song = Song(path=path, title=title, album=album, genre=genre, year=year)
            # attach artists as list
            song.artists = artists_str.split(", ") if artists_str else []
            self.songs.append(song)

    def filter(self, **kwargs):
        rows = self.db.filter_songs(**kwargs)
        return [Song(*r) for r in rows]

    def __repr__(self):
        return f"<MusicCollection: {len(self.songs)} songs>"

    def edit_song(self, song, title=None, album=None, genre=None, year=None):
        """Update song metadata (both file and DB)"""
        song.update_metadata(title=title, album=album, genre=genre, year=year)
        self.db.update_song(song)

def load_collection(directory=None):

  if directory is None:
    directory = os.getenv("RHYTHM_MUSIC_DIR", os.path.expanduser("~/Music"))

  return MusicCollection(directory)
