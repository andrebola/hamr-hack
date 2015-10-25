'''
Created on Oct 24, 2015

@author: joro
'''
from MelodicMotif import MelodicMotif

        
        
class Song(object):
    """ generated source for class Song """

    def __init__(self, name,  notesArray, minSplitTimeMotif=1):
        #  TODO: tool to extract song name from path or metadata
        self.name = name
        self.melodicMotives = []
        
        currMelodicMotif = MelodicMotif()
        previousOffset = notesArray[0].onset
        
        for note in notesArray:
            
            motifSplitTime = note.onset - previousOffset
            if motifSplitTime >= minSplitTimeMotif: # start NewMotiv
                self.melodicMotives.append(currMelodicMotif)
                currMelodicMotif = MelodicMotif()
                
            if  note.MIDIpitch != -1:
                
                currMelodicMotif.notes.append(note)
                previousOffset = note.onset + note.duration
        
        # append last motif        
        self.melodicMotives.append(currMelodicMotif)
        
        self.intervalize()    
                    
                    
    def printIt(self):
       print "intervals: " 
       
       for motif in self.melodicMotives:
           print "    motiv: "
           for note in motif.notes:
#             print "{} ".format(note.intervalToNext)
              print note
           
           print
    
        
                         

    #
    def intervalize(self):
        """ convert notes to intervals in each melodic motiv  """

        for currMelodicMotif in self.melodicMotives:
 
            if len(currMelodicMotif.notes) == 1:
                continue
            
            
            i = 0
            while (i < len(currMelodicMotif.notes) - 1):
                currentMIDInote = currMelodicMotif.notes[i].MIDIpitch
                nextMIDInote = currMelodicMotif.notes[i+1].MIDIpitch 
                currMelodicMotif.notes[i].intervalToNext = nextMIDInote - currentMIDInote
                i = i + 1
    

    def queryPattern(self, queryPatternIntervals):
        resultHits = [] 
        for currMelodicMotif in self.melodicMotives:
                
                # TODO: skip motifs of length smaller than query ? 
#                 if len(currMelodicMotif.notes) == 1:
#                     continue
                
                # skip same note, e.g. zero interval
                currMelodicMotifNoZeroIntervals = []
                for currNote in currMelodicMotif.notes:
                    if currNote.intervalToNext and currNote.intervalToNext != 0:
                         currMelodicMotifNoZeroIntervals.append(currNote)
                
                # NOTE: No zero skipping : currMelodicMotif.notes used instead of currMelodicMotifNoZeroIntervals
                hitIndices = subfinder(currMelodicMotif.notes, queryPatternIntervals)
                lenHit = len(queryPatternIntervals)
                
                # add result hit to current indices
                for idx in hitIndices:
                    notesHit = currMelodicMotif.notes[idx:idx+lenHit + 1]
                    resultHits.append(notesHit) 
                return resultHits    
                         
            
    
    
def subfinder(mylistNotes, queryPatternIntervals):
        '''
        find subpattern of three intervals
        '''
        indicesFound = [] 
        for idx in range(len(mylistNotes)):
            if mylistNotes[idx].intervalToNext == queryPatternIntervals[0]: # check first token first. for speed up
                
                # make list of intervals
                intervalsTarget = []
                for note in  mylistNotes[idx:idx+len(queryPatternIntervals)]:
                    intervalsTarget.append(note.intervalToNext)
                
                if intervalsTarget == queryPatternIntervals: # check whole interval
                    indicesFound.append(idx)
        return indicesFound
        
        