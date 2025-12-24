import sqlite3

class RhythmDB:
    def __init__(self, db_path="rhythm.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Artist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Album (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          year INTEGER NOT NULL,
          UNIQUE(name, year)
        );

        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Song (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            title TEXT,
            album_id INTEGER,
            genre TEXT,
            FOREIGN KEY(album_id) REFERENCES Album(id)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS SongArtist (
            song_id INTEGER,
            artist_id INTEGER,
            PRIMARY KEY (song_id, artist_id),
            FOREIGN KEY(song_id) REFERENCES Song(id),
            FOREIGN KEY(artist_id) REFERENCES Artist(id)
        )
        """)

        self.conn.commit()

    def insert_song(self, song):
        cur = self.conn.cursor()

        album_id = self.get_album_id(song.album, song.year)

        cur.execute("""
        INSERT OR IGNORE INTO Song(path, title, album_id, genre)
        VALUES (?, ?, ?, ?)
        """, (song.path, song.title, album_id, song.genre))

        cur.execute("SELECT id FROM Song WHERE path = ?", (song.path,))
        song_id = cur.fetchone()[0]

        if song.artist:
            artists = [a.strip() for a in song.artist.replace("&", ",").split(",")]
            for a in artists:
                artist_id = self.get_artist_id(a)
                cur.execute("""
                INSERT OR IGNORE INTO SongArtist(song_id, artist_id)
                VALUES (?, ?)
                """, (song_id, artist_id))

        self.conn.commit()

    def fetch_all_songs(self):
        cur = self.conn.cursor()
        cur.execute("""
        SELECT
            s.path,
            s.title,
            GROUP_CONCAT(ar.name, ', '),
            al.name,
            s.genre,
            al.year
        FROM Song s
        JOIN Album al ON s.album_id = al.id
        JOIN SongArtist sa ON s.id = sa.song_id
        JOIN Artist ar ON sa.artist_id = ar.id
        GROUP BY s.id
        """)
        return cur.fetchall()


    def filter_songs(self, artist=None, year=None, genre=None):
        query = """
        SELECT
          s.path,
          s.title,
          al.name,
          s.genre,
          al.year,
          GROUP_CONCAT(ar.name, ', ')
        FROM Song s
        JOIN Album al ON s.album_id = al.id
        JOIN SongArtist sa ON s.id = sa.song_id
        JOIN Artist ar ON sa.artist_id = ar.id
        """

        conditions = []
        params = []

        if artist:
            conditions.append("ar.name = ?")
            params.append(artist)

        if year:
            conditions.append("al.year = ?")
            params.append(year)

        if genre:
            conditions.append("s.genre = ?")
            params.append(genre)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY s.id"

        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

    def get_artist_id(self, name):
        cur = self.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO Artist(name) VALUES (?)", (name,))
        cur.execute("SELECT id FROM Artist WHERE name = ?", (name,))
        return cur.fetchone()[0]
        
    def get_album_id(self, name, year):
        name = name if name else "Unknown Album"
        year = year if year else -1
        cur = self.conn.cursor()
        cur.execute(
          "INSERT OR IGNORE INTO Album(name, year) VALUES (?, ?)",
          (name, year)
        )

        cur.execute(
          "SELECT id FROM Album WHERE name = ? AND year = ?",
          (name, year)
        )

        row = cur.fetchone()
        if row is None:
            raise RuntimeError(f"Album insert/select failed: {name}, {year}")

        return row[0]

    def update_song(self, song):
        """Update DB to match Song object's metadata"""
        cur = self.conn.cursor()
        
        # Update album table first (if album changed)
        cur.execute("INSERT OR IGNORE INTO Album(name, year) VALUES (?, ?)", (song.album, song.year))
        cur.execute("SELECT id FROM Album WHERE name = ? AND year = ?", (song.album, song.year))
        album_id = cur.fetchone()[0]

        # Update song table
        cur.execute("""
            UPDATE Song
            SET title = ?, album_id = ?, genre = ?
            WHERE path = ?
        """, (song.title, album_id, song.genre, song.path))

        self.conn.commit()
