"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import soundfile
import sounddevice
import numpy

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wav/ogg file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

sound = soundfile.SoundFile(sys.argv[1], 'r')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=pyaudio.paInt16,
                channels=sound.channels,
                rate=sound.samplerate,
                output=True)

# read data
data = sound.read(CHUNK, 'int16')

# play stream (3)
while len(data) > 0:
    stream.write(data.tostring())
    data = sound.read(CHUNK, 'int16')

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
