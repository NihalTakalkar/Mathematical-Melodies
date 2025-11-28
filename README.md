Our goal is to make a software that uses fibonacci sequences and prime numbers to generate music through asking the user what tempo, key signature, and time signature they want.

mido.readthedocs.io 

Python code
1. create a function to generate a sequence of first 10 prime numbers
2. create a function to generate a sequence of first 10 Fibonacci series numbers
3. create a function to generate a sequence of first 10 Multiple of 2s numbers
4. create a function to generate a sequence of first 10  Multiple of 5s numbers
5. create a function to generate midi files. Send the above sequence, filename and tempo number (480) to this function
	- basically with for loop match each number in sequence with a scale to create a note
	- then append that note to the track
	- after the loop, save the midi file with your filename.

Step 1: Run three main experiments:
1. Fibonacci vs Prime Numbers
	- Input: Fibonacci sequence mapped to C major scale vs prime numbers mapped to C major scale.
	- Output: Two MIDI files.
	- Observation: Fibonacci produces smoother, repeating motifs; primes sound more irregular.

2. Multiples of 2 vs Multiples of 5
	- Input: Multiples of 2 control rhythm, multiples of 5 control tempo.
	- Output: Two MIDI files.
	- Observation: Multiples of 2 → predictable rhythm; multiples of 5 → shifting tempo.
3. Scale Comparison
	- Input: Same sequence (e.g., Fibonacci), mapped to major vs minor scale.
	- Output: Two MIDI files.
	- Observation: Major feels “happy,” minor feels “sad,” even though the math sequence is identical.

Step 2: Generate MIDI Files
	- Use Python + MIDIUtil to create MIDI files.
	- Each experiment will generate two MIDI files (using different math concepts).
	- Save them with clear names: fibonacci_major.mid, prime_major.mid, etc.

Step 3: AI Analysis of MIDI Files
Use music21 Python library to extract features from MIDI to compare:
Pitch distribution → clustered vs scattered.
Intervals → small steps vs large jumps.
Durations → regular vs irregular rhythms.
Repetition → motifs that repeat vs randomness.

Step 4: Generate a Report
Turn your above analysis into reports or tables 

Step 5: Iteration Based on Report
Now you use the report metrics to decide how to change inputs:
eg: Report shows Prime has high pitch variance and irregular rhythm.
	- Restrict Prime mapping to pentatonic scale + fix rhythm by mapping primes to fixed durations.
	- Regenerate Prime MIDI.


