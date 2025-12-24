import rhythm
from tabulate import tabulate
import textwrap

coll = rhythm.load_collection()
coll = rhythm.load_collection()
print(coll.songs)

# Fixed column widths
col_widths = {
    "Title": 25,
    "Artist(s)": 25,
    "Album": 20,
    "Genre": 10,
    "Year": 6,
    "Path": 30
}

# Helper function to wrap text
def wrap_text(text, width):
    if not text:
        return ""
    return "\n".join(textwrap.wrap(str(text), width=width))

# Prepare table
table = []
for song in coll.songs:
    table.append([
        wrap_text(song.title, col_widths["Title"]),
        wrap_text(", ".join(song.artists), col_widths["Artist(s)"]),
        wrap_text(song.album, col_widths["Album"]),
        wrap_text(song.genre, col_widths["Genre"]),
        wrap_text(song.year, col_widths["Year"]),
        wrap_text(song.path, col_widths["Path"])
    ])

# Print nicely
headers = ["Title", "Artist(s)", "Album", "Genre", "Year", "Path"]
print(tabulate(table, headers=headers, tablefmt="grid"))

# DB-backed filtering
rahman = coll.filter(artist="A. R. Rahman")
print(rahman)

rock = coll.filter(genre="Rock")
print(rock)

songs_2015 = coll.filter(year="2015")
print(songs_2015)

rock_15 = coll.filter(genre="Hindi", year="2015")
print(rock_15)

coll.filter(artist="Some Unknown Artist")

