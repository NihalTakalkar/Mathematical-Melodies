import math, os
from mido import Message, MidiFile, MidiTrack

folder_name = "C:/Mathematical_Melodies/"
os.mkdir(folder_name)

def generate_midi(filename, sequence):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=instrument, time=0))

    scale = [60, 62, 64, 65, 67, 69, 71]

    for n in sequence:
        note = scale[n % len(scale)]
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

instrument = int(input("What instrument do you want? "))


fibNum = generate_fibonacci(100)
primeNum = generate_primes(100)
twoNum = multiples_of_two(100)
fiveNum = multiples_of_five(100)
generate_midi("fibonacci.mid", fibNum)
generate_midi("prime.mid", primeNum)
generate_midi("two.mid", twoNum)
generate_midi("five.mid", fiveNum)
print("Your file has been created!")

