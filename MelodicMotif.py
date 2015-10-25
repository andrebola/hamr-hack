'''
Created on Oct 24, 2015

@author: joro
'''

class MelodicMotif(object):
    """ generated source for class MelodicMotif """
    

    def __init__(self):
        """ generated source for method __init__ """
        self.notes = []
        
    def __str_(self):
        strOutput = '' 
        for note in self.notes:
#             print "{} ".format(note.intervalToNext)
              
              strOutput += note.__str__()
        return strOutput
