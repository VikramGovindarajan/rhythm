# Python3 program to illustrate
# accessing of audio metadata
# using tinytag library
  
# Import Tinytag method from
# tinytag library
from tinytag import TinyTag
  
# Pass the filename into the
# Tinytag.get() method and store
# the result in audio variable
audio = TinyTag.get("SarangaDariya.mp3")
  
# Use the attributes
# and Display
print("Title:" + audio.title)
print("Artist: " + audio.artist)
print("Genre:" + audio.genre)
print("Year Released: " + audio.year)
print("Bitrate:" + str(audio.bitrate) + " kBits/s")
print("Composer: " + audio.composer)
print("Filesize: " + str(audio.filesize) + " bytes")
print("AlbumArtist: " + audio.albumartist)
print("Duration: " + str(audio.duration) + " seconds")
print("TrackTotal: " + str(audio.track_total))