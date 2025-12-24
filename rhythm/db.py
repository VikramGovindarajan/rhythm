import sqlite3

class RhythmDB:
    def __init__(self, db_path="rhythm.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Song (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            title TEXT,
            artist TEXT,
            album TEXT,
            genre TEXT,
            year TEXT
        )
        """)
        self.conn.commit()

    def insert_song(self, song):
        cur = self.conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO Song
        (path, title, artist, album, genre, year)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            song.path,
            song.title,
            song.artist,
            song.album,
            song.genre,
            song.year
        ))
        self.conn.commit()

    def fetch_all_songs(self):
        cur = self.conn.cursor()
        cur.execute("SELECT path, title, artist, album, genre, year FROM Song")
        return cur.fetchall()

    def filter_songs(self, *, artist=None, year=None, genre=None):
        query = "SELECT path, title, artist, album, genre, year FROM Song WHERE 1=1"
        params = []

        if artist:
            query += " AND artist LIKE ?"
            params.append(f"%{artist}%")
        if year:
            query += " AND year = ?"
            params.append(year)
        if genre:
            query += " AND genre = ?"
            params.append(genre)

        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
