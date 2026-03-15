-- Rhythm Database Schema
-- Recreates the database structure used by RhythmDB

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Artist (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Album (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
year INTEGER NOT NULL,
UNIQUE(name, year)
);

CREATE TABLE IF NOT EXISTS Song (
id INTEGER PRIMARY KEY AUTOINCREMENT,
path TEXT UNIQUE,
title TEXT,
album_id INTEGER,
genre TEXT,
FOREIGN KEY(album_id) REFERENCES Album(id)
);

CREATE TABLE IF NOT EXISTS SongArtist (
song_id INTEGER,
artist_id INTEGER,
PRIMARY KEY (song_id, artist_id),
FOREIGN KEY(song_id) REFERENCES Song(id),
FOREIGN KEY(artist_id) REFERENCES Artist(id)
);
