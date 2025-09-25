import math
import numpy
import pygame

pygame.init()

bits = 16
sample_rate = 44100
pygame.mixer.pre_init(sample_rate, )

def sine_x(amp, freq, time):
    return round(amp * math.sin(2 * math.pi * freq * time))


