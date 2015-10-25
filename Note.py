'''
Created on Oct 24, 2015

@author: joro
'''

class Note(object):
    """ generated source for class Note """
    onset = float()
    duration = float()
    intervalToNext = None

    def __init__(self, onset, duration, midiPitch):
        """ generated source for method __init__ """
        self.MIDIpitch = midiPitch
        self.onset = onset
        self.duration = duration
    
    def __str__(self):
        return "onset: {} , offset {}, MIDI {}  ".format(self.onset, self. onset + self.duration, self.MIDIpitch)
    
    