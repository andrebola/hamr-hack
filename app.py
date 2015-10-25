from flask import Flask, request
from flask import render_template, jsonify
import json

from PItchContourSegmenter import extractPitch, segmentNotesFromPitch
from Song import Song


#import search

app = Flask("abzlabs", static_url_path="/static", static_folder="static")
app.debug = True

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    data = dict((key, request.form.getlist(key)) for key in request.form.keys())    
    sorted_keys = data.keys()
    sorted_keys.sort(key=lambda tup: tup[0])    
    notes = [] 
    for i in sorted_keys:
        notes.append(int(data[i][0]))
    last = None
    out = []
    for i in notes:
        if last:
            out.append(i - last)
        last = i
    songFileName = "/vagrant/data/hack/static/spanish_caravan_voice_and_drums.wav"    
    result_notes =  doit(songFileName, out)
    return render_template("search.html",notes=result_notes)

def doit(songFileName, queryPatternIntervals ):
    
    audio, pitchSeries, hopSize = extractPitch(songFileName)
    
    sampleRate = 44100
    notesArray = segmentNotesFromPitch(pitchSeries, audio, sampleRate, hopSize )
    song = Song('doors', notesArray)
    
    
    hits = song.queryPattern(queryPatternIntervals)
    if len(hits) == 0:
        return "no results"
    
    firstHit = hits[0]
    resultNotes = []
    
    for note in firstHit:
        resultNotes.append( [note.onset, note.duration, note.MIDIpitch])
    return resultNotes
    
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
