import math, os, streamlit as st
from mido import Message, MidiFile, MidiTrack


pianos = {
    "Acoustic Grand Piano": 0,
    "Electric Piano": 4,
}

string_instruments = {
    "Violin": 40,
    "Viola": 41,
    "Cello": 42,
    "Contrabass": 43,
    "Tremolo Strings": 44,
    "Pizzicato Strings": 45,
    "Orchestral Harp": 46,
    "Church Organ": 19,
}

brass_instruments = {
    "Trumpet": 56,
    "Trombone": 57,
    "Tuba": 58,
    "French Horn": 60,
    "Brass Section": 61
}

woodwind_instruments = {
     "Soprano Sax": 65,
    "Alto Sax": 66,
    "Tenor Sax": 67,
    "Baritone Sax": 68,
    "Oboe": 69,
    "Bassoon": 71,
    "Clarinet": 72,
    "Piccolo": 73,
    "Flute": 74,
}

percussion_instruments = {
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
}

choir = {
    "Choir Aahs": 52,
    "Voice Oohs": 53
}

instruments_dict = {**pianos, **string_instruments, **brass_instruments, **woodwind_instruments, **percussion_instruments, **choir}

octaves = {

    "Trombone": -12,
    "Tuba": -24,
    "Viola": -12,
    "Cello": -12,
    "Contrabass": -24,
    "Flute": 12,
    "Piccolo": 24,
    "Baritone Sax": -24,
    "Tenor Sax": -12,
    "Bassoon": -12,
    "Soprano Sax": 12
}

def generate_midi(filename, sequence, key):
    mid = MidiFile()

    for i in instrument_choice:
        track = MidiTrack()
        mid.tracks.append(track)

        combined_program = instruments_dict[i]
        if i in octaves:
            combined_program += octaves[i]
            
        track.append(Message('program_change', program=combined_program, time=0))

        sequence = assign_instrument_algorithm(i)

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

def assign_instrument_algorithm(instrument_name):
    if instrument_name in brass_instruments:
        return generate_primes(100)
    if instrument_name in string_instruments or instrument_name in woodwind_instruments:
        return generate_fibonacci(100)
    if instrument_name in percussion_instruments or instrument_name in pianos:
        return multiples_of_two(100) + multiples_of_five(100)
    
    return generate_fibonacci(100)
    
    
st.title("Mathematical Melodies")
instrument_choice = st.multiselect("Which instruments do you want? ", list(instruments_dict.keys()))
instrument = instruments_dict[instrument_choice[0]] if instrument_choice else 0
Key = st.selectbox("Select a key: ", 
                   ("None Selected", "C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", 
                    "G♯/A♭", "A", "A♯/B♭", "B"))
major_or_minor = st.selectbox("Major or Minor? ", ("Major", "Minor"))

if Key == "None Selected":
    st.warning("Please select a key to proceed.")
elif Key == "C":
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


if st.button("Generate Musical MIDI Files"):
    folder_name = "C:/Mathematical Melodies/"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    
    generate_midi("mathematical_melody.mid", instrument, key)


    st.write('MIDI files have been generated. Go to your C drive and locate a folder called "Mathematical Melodies" to find them!')

