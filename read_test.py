from mido import MidiFile
from mido import MetaMessage
from mido.midifiles import MidiTrack
import mido
import random

def reverse_mid(fname,result_name):

    mid = MidiFile(fname)

    """
    for i,track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            if not isinstance(message, MetaMessage):
                print(message)  
    """
    messages = []
    for message in mid.tracks[1]:
        if not isinstance(message, MetaMessage):
            messages.append(message)

    with MidiFile() as new_mid:
        track = MidiTrack()
        new_mid.tracks.append(mid.tracks[0]) #append first track with all meta data
        new_mid.tracks.append(track)
        reversed_msg = []
        
        msg_velocity = 0
        msg_time = 960
        for message in messages:
            if message.type == 'note_on':
                new_message = mido.Message('note_off', note=message.note,velocity=0, time=msg_time) 
                reversed_msg.insert(0,new_message)
                msg_velocity = message.velocity #update velocity
            elif message.type == 'note_off':
                new_message = mido.Message('note_on', note=message.note, velocity=msg_velocity, time=0)
                reversed_msg.insert(0,new_message)
            else:
                continue
       
        for message in reversed_msg:
            track.append(message)
        
        new_mid.save(result_name)

def half_up_every_two(fname,result_name):
    """
        Raises every second note by half step
    """
    mid = MidiFile(fname)
    messages = []
    for message in mid.tracks[1]:
        if not isinstance(message, MetaMessage):
            messages.append(message)

    with MidiFile() as new_mid:
        track = MidiTrack()
        new_mid.tracks.append(mid.tracks[0]) #append first track with all meta data
        new_mid.tracks.append(track)

    new_messages = []
    note_counter = 0
    for message in messages:
        if message.type == 'note_off':
            continue
        elif message.type == 'note_on':
            if note_counter % 2 == 0:
                new_messages.append(mido.Message('note_on', note=message.note+1, velocity=message.velocity, time=960))
                new_messages.append(mido.Message('note_off', note=message.note+1, velocity=message.velocity, time=960))
                note_counter += 1
            else:
                new_messages.append(mido.Message('note_on', note=message.note, velocity=message.velocity, time=960))
                new_messages.append(mido.Message('note_off', note=message.note, velocity=message.velocity, time=960))
                note_counter += 1           
 
    for message in new_messages:
        track.append(message)

    new_mid.save(result_name)
           
def transpose2(fname,result_name):
    """
        Transpose two instruments up by M2
    """
    mid = MidiFile(fname)
    messages = []
    
    with MidiFile() as new_mid:
        new_mid.ticks_per_beat = 960
        new_mid.tracks.append(mid.tracks[0])
        for track in mid.tracks[1:]:
            new_track = MidiTrack()
            for message in track:
                if message.type == 'note_off':
                    continue
                elif message.type == 'note_on':
                    new_track.append(mido.Message('note_on',note=message.note+2,velocity=message.velocity,time=0))
                    new_track.append(mido.Message('note_off',note=message.note+2,velocity=message.velocity,time=960))
                else:
                    new_track.append(message)
            new_mid.tracks.append(new_track)
        new_mid.save(result_name)

def changeRhythm(fname,result_name):
    """
        Change rhythm of two instruments
    """
    mid = MidiFile(fname)
    messages = []
    
    with MidiFile() as new_mid:
        new_mid.ticks_per_beat = 960
        new_mid.tracks.append(mid.tracks[0])

        #track1
        new_track1 = MidiTrack()
        for message in mid.tracks[1]:
            if message.type == 'note_off':
                new_track1.append(mido.Message('note_off',note=message.note,velocity=message.velocity,time=message.time/2))
            elif message.type == 'note_on':
                new_track1.append(mido.Message('note_on',note=message.note,velocity=message.velocity,time=0))
            else:
                new_track1.append(message)
        new_mid.tracks.append(new_track1)

        #track2
        new_track2 = MidiTrack()
        for message in mid.tracks[2]:
            if message.type == 'note_off':
                new_track2.append(mido.Message('note_off',note=message.note,velocity=message.velocity,time=message.time*2))
            elif message.type == 'note_on':
                new_track2.append(mido.Message('note_on',note=message.note,velocity=message.velocity,time=0))
            else:
                new_track2.append(message)
        new_mid.tracks.append(new_track2)

        new_mid.save(result_name)

def indiv_rhythm_change(fname,result_name):
    """
        Change the rhythm of individual note randomly.
    """   
    mid = MidiFile(fname)
    rhythm_conversion = [0.25,0.5,1,2,4] #rhythm change factor   
 
    with MidiFile() as new_mid:
        new_mid.tricks_per_beat = 960
        new_mid.tracks.append(mid.tracks[0])

    #track1
    new_track1 = MidiTrack()
    new_track1.append(MetaMessage('time_signature',numerator=3,denominator=4))
    for message in mid.tracks[1]:
        if message.type == 'note_off':
            new_track1.append(mido.Message('note_off',note=message.note,velocity=message.velocity,time=int(message.time*random.choice(rhythm_conversion))))
        elif message.type == 'note_on':
            new_track1.append(mido.Message('note_on',note=message.note,velocity=message.velocity,time=message.time))
        else:
            new_track1.append(message)
    new_mid.tracks.append(new_track1)

    #track2
    new_track2 = MidiTrack()
    for message in mid.tracks[2]:
        if message.type == 'note_off':
            new_track2.append(mido.Message('note_off',note=message.note,velocity=message.velocity,time=int(message.time*random.choice(rhythm_conversion))))
        elif message.type == 'note_on':
            new_track2.append(mido.Message('note_on',note=message.note,velocity=message.velocity,time=message.time))
        else:
            new_track2.append(message)
    new_mid.tracks.append(new_track2)
    

    new_mid.save(result_name)

def changeGuitar(fname,result_name):
    """
        Changes first 100 notes of guitar by raising half step
    """
    mid = MidiFile(fname)
    
    with MidiFile() as new_mid:
        new_mid.ticks_per_beat = 960
        new_mid.tracks.append(mid.tracks[0])

        guitar_track = mid.tracks[1]
        new_track = MidiTrack()
        note_counter = 0
        #go through first 100 notes and raise notes by half step
        for i in range(len(guitar_track)):
            if note_counter<100:
                if guitar_track[i].type == 'note_on':
                    new_track.append(mido.Message('note_on',note=guitar_track[i].note+1,velocity=guitar_track[i].velocity,time=0))
                    note_counter += 1
                elif guitar_track[i].type == 'note_off':
                    new_track.append(mido.Message('note_off',note=guitar_track[i].note+1,velocity=guitar_track[i].velocity,time=guitar_track[i].time))
                else:
                    new_track.append(guitar_track[i])
            else:
                new_track.append(guitar_track[i])
        new_mid.tracks.append(new_track)
        new_mid.save(result_name)

def changePercussion(fname,result_name):
    mid = MidiFile(fname)

    with MidiFile() as new_mid:
        new_mid.ticks_per_beat = 960
        new_mid.tracks.append(mid.tracks[0])
        
        #change marimba (track 3), raise each note by half step, speed up by factor of 2
        marimba = mid.tracks[3]
        new_marimba = MidiTrack()
        for message in marimba:
            if message.type == 'note_on':
                new_marimba.append(mido.Message('note_on',note=message.note+1, velocity=message.velocity, time=message.time))
            elif message.type == 'note_off':
                new_marimba.append(mido.Message('note_off', note=message.note+1, velocity=message.velocity, time=message.time/2))
            else:
                new_marimba.append(message)
        new_mid.tracks.append(new_marimba)

        #change snare drum (track 1), speed it by factor of 4
        snare_drum = mid.tracks[1]
        new_snare_drum = MidiTrack()
        for message in snare_drum:
            if message.type == 'note_on':
                new_snare_drum.append(mido.Message('note_on', note=message.note, velocity=message.velocity, time=message.time,channel=9))
            elif message.type == 'note_off':
                new_snare_drum.append(mido.Message('note_off', note=message.note, velocity=message.velocity, time=message.time/4, channel=9))
            else:
                new_snare_drum.append(message)
        new_mid.tracks.append(new_snare_drum)
              
        #change cowbell (track 2), slow it by a factor of 2
        cowbell = mid.tracks[2]
        new_cowbell = MidiTrack()
        for message in cowbell:
            if message.type == 'track_name':
                new_cowbell.append(MetaMessage('track_name', name=u'Triangle'))
            elif message.type == 'note_on':
                new_cowbell.append(mido.Message('note_on', note=81, velocity=message.velocity, time=message.time,channel=9))
            elif message.type == 'note_off':
                new_cowbell.append(mido.Message('note_off', note=81, velocity=message.velocity, time=message.time*2, channel=9))
            else:
                new_cowbell.append(message)
        new_mid.tracks.append(new_cowbell)
                 

        new_mid.save(result_name)

#transpose2('two_instrument_rhythm.mid','new_two_instrument_rhythm.mid')
#changeRhythm('two_instrument_rhythm.mid','new_two_instrument_rhythm.mid')
#changeGuitar('vivaldi.mid','new_vivaldi.mid')
#changePercussion('percussion.mid','new_percussion.mid')
indiv_rhythm_change('two_instrument_rhythm.mid','new_diff_rhythm.mid')
