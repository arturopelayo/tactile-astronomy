"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import soundfile
import sounddevice
import numpy
import time

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wav/ogg file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# read data
sound = soundfile.SoundFile(sys.argv[1], 'r')
data = sound.read(CHUNK, 'int16')

# open stream (2)
stream = p.open(format=pyaudio.paInt16,
                channels=sound.channels,
                rate=sound.samplerate,
                output=True)

sound2 = soundfile.SoundFile(sys.argv[1], 'r')
data2 = sound2.read(CHUNK, 'int16')

start = time.time() + 1

def mixer(v1, v2):
    len1 = len(v1)
    len2 = len(v2)

    # average of two
    if len1 < len2:
        v1 = numpy.pad(v1, ((0, len2 - len1), (0, 0)), 'constant', constant_values=(0, 0))

    elif len2 < len1:
        v2 = numpy.pad(v2, ((0, len1 - len2), (0, 0)), 'constant', constant_values=(0, 0))

    result = numpy.mean([v1, v2], axis=0, dtype=numpy.int16)

    return result



# play stream (3)
while len(data) > 0 or len(data2) > 0:
    if start > time.time():
        combined = mixer(data, numpy.empty((1024, 2)))
        if len(data) > 0:
            data = sound.read(CHUNK, 'int16')
    else:
        combined = mixer(data, data2)
        if len(data) > 0:
            data = sound.read(CHUNK, 'int16')
        if len(data2) > 0:
            data2 = sound2.read(CHUNK, 'int16')
    stream.write(combined.tostring())


# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
