from mido import MidiFile
from mido import MetaMessage
from mido.midifiles import MidiTrack
import mido
import sys

def read_mid(fname):
    mid = MidiFile(fname)
    for i,track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message) 
        print mid.type

read_mid(sys.argv[1]) 
