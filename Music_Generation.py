import math
from mido import Message, MidiFile, MidiTrack, MetaMessage

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
     "Soprano Sax": 64,
    "Alto Sax": 65,
    "Tenor Sax": 66,
    "Baritone Sax": 67,
    "Oboe": 68,
    "Bassoon": 70,
    "Clarinet": 71,
    "Piccolo": 72,
    "Flute": 73,
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

def generate_midi(filename, inst_math_choices, key, numMeasures, time_signature):
    mid = MidiFile() # Create a new MIDI file object
    track_tempo = MidiTrack() # Create a new MIDI track for tempo and time signature
    mid.tracks.append(track_tempo) # Add tempo track to MIDI file

    track_tempo.append(MetaMessage('set_tempo', tempo=500000, time=0)) # Set tempo to 120 BPM

    TICKS_PER_BEAT = mid.ticks_per_beat # Default is 480 ticks per beat (aka quarter note denomination)

    if time_signature == "4/4": # 4 quarter notes per measure
        numerator = 4
        denominator = 4
        NOTE_TICKS = TICKS_PER_BEAT
        beats_per_measure = 4

    elif time_signature == "3/4": # 3 quarter notes per measure
        numerator = 3
        denominator = 4
        NOTE_TICKS = TICKS_PER_BEAT
        beats_per_measure = 3

    elif time_signature == "6/8": # 6 eighth notes per measure (eigth note gets the beat)
        numerator = 6
        denominator = 8
        NOTE_TICKS = TICKS_PER_BEAT // 2 # Eighth note gets half the ticks of a quarter note
        beats_per_measure = 6

    TOTAL_TICKS = numMeasures * beats_per_measure * NOTE_TICKS # Total ticks in the entire piece is number of measures times beats per measure times ticks per beat

    track_tempo.append(MetaMessage('time_signature', numerator=numerator, denominator=denominator, time=0)) # Set time signature

    for idx, (instrument, concept) in enumerate(inst_math_choices.items()): # For each selected instrument and its mathematical concept
        track = MidiTrack()
        track.append(MetaMessage('track_name', name=instrument, time=0))
        mid.tracks.append(track)

        channel = 9 if instrument in percussion_instruments else (idx % 15) # Channel 9 is reserved for percussion

        if instrument not in percussion_instruments: # Set the instrument program change
            program = instruments_dict[instrument] # Get the MIDI program number
            octave = octaves.get(instrument, 0) # Get octave adjustment if any
            track.append(Message('program_change', program=program, time=0, channel=channel))
        else:
            octave = 0

        sequence = assign_instrument_algorithm(concept) # Get the number series based on the selected mathematical concept
        numTicks = 0 # Total ticks played so far
        indexSeq = idx * 5 # Offsets the starting index in the sequence for each instrument so that they don't all start the same
        lenSeq = len(sequence) # Length of the sequence

        
    
        step = 1 # Controls how we step through the sequence. Larger step means bigger melody jumps.
        if instrument in brass_instruments:
            step = 2 
        elif instrument in percussion_instruments:
            step = 3

        while numTicks < TOTAL_TICKS: # Continue until we've filled the total ticks for the piece
            n = sequence[indexSeq % lenSeq] # Get the current number from the sequence by getting the remainder of indexSeq divided by length of sequence

            duration = NOTE_TICKS * (1 + (n % 3)) # Note ticks is multiplied by 1 plus remainder of n divided by 3 to vary note lengths

            if instrument in percussion_instruments:
                note = instruments_dict[instrument]
            else:
                degree = n % len(key) # Map number to a degree in the selected key
                register = (n // len(key)) % 3 # Determines which octave/register to play the note in
                note = key[degree] + octave + (register * 12) # key note + instrument octave adjustment + register shift

            note = max(0, min(127, int(note))) # Ensure note is within MIDI range

            track.append(Message('note_on', note=note, velocity=64, time=0, channel=channel)) 
            track.append(Message('note_off', note=note, velocity=64, time=duration, channel=channel)) # Plays note for 'duration' ticks

            numTicks += duration # Update total ticks played
            indexSeq += step # Move to next index in sequence based on step size
        
    mid.save(filename)

def generate_fibonacci(n):
    fib = [0, 1] # Starting values
    for num in range(2, n):
        fib.append(fib[num-1] + fib[num-2]) # Next Fibonacci number is sum of previous two
        
    return fib
    
def generate_primes(n):
    primes = []
    for num in range(2, n + 1): # Check each number from 2 to n
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)): # Check divisibility by all numbers up to sqrt(num) because if num is divisible by any number larger than its square root, it must also be divisible by a smaller number
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

def assign_instrument_algorithm(concept): # Assigns the appropriate number generation function based on the selected concept
    if concept == "Fibonacci Sequence":
        return generate_fibonacci(100) # Generate first 100 Fibonacci numbers
    elif concept == "Prime Numbers":
        return generate_primes(100) # Generate prime numbers up to 100
    elif concept == "Multiples of 2":
        return multiples_of_two(100) # Generate multiples of 2 up to 100
    elif concept == "Multiples of 5":
        return multiples_of_five(100) # Generate multiples of 5 up to 100
    else: # if no concept is selected, default to Fibonacci
        return generate_fibonacci(100)
    
def key_to_midi(Key, major_or_minor):
                                                # Converts each note of the selected key scale to its corresponding MIDI note number
    key_choices = {
        "C": [60, 62, 64, 65, 67, 69, 71],
        "C♯/D♭": [61, 63, 65, 66, 68, 70, 72],
        "D": [62, 64, 66, 68, 69, 71, 73],
        "D♯/E♭": [63, 65, 67, 68, 70, 72, 74],
        "E": [64, 66, 68, 69, 71, 73, 75],
        "F": [65, 67, 69, 70, 72, 74, 76],
        "F♯/G♭": [66, 68, 70, 71, 73, 75, 77],
        "G": [67, 69, 71, 72, 74, 76, 78],
        "G♯/A♭": [68, 70, 72, 73, 75, 77, 79],
        "A": [69, 71, 72, 74, 76, 77, 79],
        "A♯/B♭": [70, 72, 74, 75, 77, 79, 81],
        "B": [71, 73, 75, 76, 78, 80, 82]
        }
    
    minor_adjustments = [0, 0, -1, 0, 0, -1, -1] # Adjustments to convert major scale to minor scale

    scale = key_choices[Key]
    if major_or_minor == "Minor":
        scale = [note + minor_adjustments[i] for i, note in enumerate(scale)] # Apply minor adjustments for each degree of the scale

    return scale
