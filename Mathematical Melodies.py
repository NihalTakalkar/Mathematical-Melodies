import math
from mido import Message, Midifile, Miditrack

mid = Midfile()
track = Miditrack()
mid.tracks.append(track)

track.append(Message('note_on', note=60, velocity=64, time=0))
track.append(Message('note_off', note=60, velocity=64, time=480))
track.append(Message('note_on', note=64, velocity=64, time=0))
track.append(Message('note_off', note=64, velocity=64, time=480))
track.append(Message('note_on', note=67, velocity=64, time=0))
track.append(Message('note_off', note=67, velocity=64, time=480))

mid.save('simple_song.mid')
