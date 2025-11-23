from mido import Message, MidiFile, MidiTrack
import math, os

n = input("Enter how many prime numbes you want: ")
filename = "song.mid"

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def map_prime_to_midi(n):
    return (n % 60) + 30

def primes_to_midi(filename="prime_Nihal.mid", count=50):
    primes = generate_primes(count)

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=0))

    for p in primes:
        note = map_prime_to_midi(p)

        track.append(Message('note_on', note=note, velocity=80, time=0))
        track.append(Message('note_off', note=note, velocity=80, time=240))

    mid.save('C:/Science Fair/Mathematical-Melodies/')
    print(f"MIDI file saved as: {'C:/Science Fair/Mathematical-Melodies/'}")