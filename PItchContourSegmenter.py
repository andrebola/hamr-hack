'''
Created on Oct 24, 2015

@author: joro
'''
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages/")
from essentia.standard import *
from Note import Note
import csv

def extractPitch(fname):
    
    hopSize=256
    
    audio = MonoLoader(filename = fname)()
    run_pred = PredominantPitchMelodia(guessUnvoiced=True, frameSize=2048, hopSize=hopSize)
    pitchSeries, b =run_pred(audio)
    
    return audio, pitchSeries, hopSize


def segmentNotesFromPitch(pitchSeries, audio, sampleRate, hopSize ):
        ################# pitch contour segmentation
        
        pitchContourSegmenter = PitchContourSegmentation(sampleRate=sampleRate,
                                               hopSize=hopSize, minDur = 0.3);
        onsets, durations, MIDIpitches =    pitchContourSegmenter(pitchSeries, audio )
        
        notesArray = []
    
        exportToCsv(onsets, durations, MIDIpitches)
            
        for triple in zip(onsets, durations, MIDIpitches ):
            notesArray.append(Note(triple[0], triple[1], triple[2] ))
#             print " at {}  with duration {} and MIDIpitch: {} ".format( )  
    
        return notesArray

def exportToCsv(onsets,durations,midipitches):
    data = []
    for i in zip(onsets,durations,midipitches):
        data.append([i[0],i[1],i[2]])
    
    with open('segm.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in data:
            spamwriter.writerow(i) 
