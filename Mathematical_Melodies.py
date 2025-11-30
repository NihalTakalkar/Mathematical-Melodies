import math, os, streamlit as st
from mido import Message, MidiFile, MidiTrack

instruments_dict = {
    
    # Pianos
    "Acoustic Grand Piano": 0,
    "Electric Piano": 4,

    # Strings
    "Violin": 40,
    "Viola": 41,
    "Cello": 42,
    "Contrabass": 43,
    "Tremolo Strings": 44,
    "Pizzicato Strings": 45,
    "Orchestral Harp": 46,
    "Church Organ": 19,

    # Brass
    "Trumpet": 56,
    "Trombone": 57,
    "Tuba": 58,
    "French Horn": 60,
    "Brass Section": 61,

    # Woodwinds
    "Soprano Sax": 64,
    "Alto Sax": 65,
    "Tenor Sax": 66,
    "Baritone Sax": 67,
    "Oboe": 68,
    "Bassoon": 70,
    "Clarinet": 71,
    "Piccolo": 72,
    "Flute": 73,

    # Percussion
    "Snare Drum": 38,
    "Snare Drum (roll)": 39,
    "Bass Drum": 35,
    "Hi-Hat (closed)": 42,
    "Hi-Hat (open)": 46,
    "Crash Cymbal": 49,
    "Ride Cymbal": 51,
    "Splash Cymbal": 55,
    "Tom 1": 41,
    "Tom 2": 43,
    "Tom 3": 45,
    "Tom 4": 47,
    "Xylophone": 13,
    "Marimba": 12,
    "Vibraphone": 11,
    "Glockenspiel": 10,
    "Tubular Bells": 14,
    "Chimes": 15,
    "Triangle": 81,
    "Tambourine": 54,
    "Woodblock": 76,
    "Cowbell": 56,
    "Maracas": 70,
    "Timpani": 47,
    "Timpani Roll": 48,
    "Cymbal Roll": 52,

    # Choir
    "Choir Aahs": 52,
    "Voice Oohs": 53
}

octaves = {

    "Trombone": -12,
    "Tuba": -24,
    "Viola": -12,
    "Cello": -12,
    "Contrabass": -24,
    "Flute": 12,
    "Piccolo": 24
}

def generate_midi(filename, sequence):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=instrument, time=0))

    for n in sequence:
        note = key[n % len(key)]
        note = int(note) 
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=480))
        
    mid.save(folder_name + filename)


def generate_fibonacci(n):
    fib = [0, 1]
    for num in range(2, n):
        fib.append(fib[num-1] + fib[num-2])
        
    return fib
    
def generate_primes(n):
    primes = []
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
    return primes        

def multiples_of_two(n):
    multiples = []
    for num in range(1, n):
        if num % 2 == 0:
            multiples.append(num)
    return multiples

def multiples_of_five(n):
    multiples = []
    for num in range(1, n):
        if num % 5 == 0:
            multiples.append(num)
    return multiples


instrument_choice = st.selectbox("What instrument do you want? ", list(instruments_dict.keys()))
instrument = instruments_dict[instrument_choice]
Key = st.selectbox("Select a key: ", 
                   ("C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", 
                    "G♯/A♭", "A", "A♯/B♭", "B"))
major_or_minor = st.selectbox("Major or Minor? ", ("Major", "Minor"))

if Key == "C":
    if major_or_minor == "Minor":
        key = [60, 62, 63, 65, 67, 68, 70]
    elif major_or_minor == "Major":
        key = [60, 62, 64, 65, 67, 69, 71]
elif Key == "C♯/D♭":
    if major_or_minor == "Minor":
        key = [61, 63, 64, 66, 68, 69, 71]
    elif major_or_minor == "Major":
         key = [61, 63, 65, 66, 68, 70, 72]
elif Key == "D":
    if major_or_minor == "Minor":
        key = [62, 64, 65, 67, 69, 70, 72]
    elif major_or_minor == "major":
        key = [62, 64, 66, 68, 69, 71, 73]
elif Key == "D♯/E♭":
    if major_or_minor == "Minor":
        key = [63, 65, 66, 68, 70, 71, 73]
    elif major_or_minor == "Major":
        key = [63, 65, 67, 68, 70, 72, 74]
elif Key == "E":
    if major_or_minor == "Minor":
        key = [64, 66, 67, 69, 71, 72, 74]
    elif major_or_minor == "Major":
        key = [64, 66, 68, 69, 71, 73, 75]
elif Key == "F":
    if major_or_minor == "Minor":
        key = [65, 67, 68, 70, 72, 73, 75]
    elif major_or_minor == "Major":
        key = [65, 67, 69, 70, 72, 74, 76]
elif Key == "F♯/G♭":
    if major_or_minor == "Minor":
        key = [66, 68, 69, 71, 73, 74, 76]
    elif major_or_minor == "Major":
        key = [66, 68, 70, 71, 73, 75, 77]
elif Key == "G":
    if major_or_minor == "Minor":
        key = [67, 69, 70, 72, 74, 75, 77]
    elif major_or_minor == "Major":
        key = [67, 69, 71, 72, 74, 76, 78]
elif Key == "G♯/A♭":
    if major_or_minor == "Minor":
        key = [68, 70, 71, 73, 75, 76, 78]
    elif major_or_minor == "Major":
        key = [68, 70, 72, 73, 75, 77, 79]
elif Key == "A":
    if major_or_minor == "Minor":
        key = [69, 71, 72, 74, 76, 77, 79]
    elif major_or_minor == "Major":
        key = [57, 59, 61, 62, 64, 66, 68]
elif Key == "A♯/B♭":
    if major_or_minor == "Minor":
        key = [70, 72, 73, 75, 77, 78, 80]
    elif major_or_minor == "Major":
        key = [58, 60, 62, 63, 65, 67, 69]
elif Key == "B":
    if major_or_minor == "Minor":
        key = [71, 73, 74, 76, 78, 79, 81]
    elif major_or_minor == "Major":
        key = [59, 61, 63, 64, 66, 68, 70]

octave_adjustment = octaves.get(instrument_choice, 0)
key = [note + octave_adjustment for note in key]


if st.button("Generate Musical MIDI Files"):
    folder_name = "C:/Mathematical_Melodies/"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    fibNum = generate_fibonacci(100)
    primeNum = generate_primes(100)
    twoNum = multiples_of_two(100)
    fiveNum = multiples_of_five(100)
    generate_midi("Fibonacci.mid", fibNum)
    generate_midi("Prime.mid", primeNum)
    generate_midi("Two.mid", twoNum)
    generate_midi("Five.mid", fiveNum)
    st.write("MIDI files have been generated.")

