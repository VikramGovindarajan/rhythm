Rhythm Music Player
===================

To install,
python3 -m pip install -e .

To use, go to songs directory, type:

import rhythm

coll = rhythm.load_collection()
print(coll.songs)

# DB-backed filtering
rahman = coll.filter(artist="A. R. Rahman")
print(rahman)

rock_90s = coll.filter(genre="Rock", year="1998")

