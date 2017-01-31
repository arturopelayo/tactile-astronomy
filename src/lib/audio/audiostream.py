

class AudioStream(object):
    def __init__(self, path):
        pass

    def read(self):


thread
- pyaudio
- mixer


stream
- play
- pause
- stop
- seek time
- audio finished
- skip back
- skip forward

2stream


"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import soundfile
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

--- SNIPPED TO THREAD

voices = [sound]

N = 2
OFFSET = 1
start = time.time()

voices += [soundfile.SoundFile(sys.argv[1], 'r') for i in range(N)]
datas = [sound.read(CHUNK, 'int16', always_2d=True) for sound in voices]
start_times = [(start + OFFSET * i) for i in range(N + 1)]

--- SNIPPED TO MIXER

# play stream (3)
while any([len(d) > 0 for d in datas]):
    rundata = []
    for i in range(len(voices)):
        if start_times[i] > lap_time or len(datas[i]) == 0:
            rundata += [None]
        else:
            rundata += [datas[i]]
            datas[i] = voices[i].read(CHUNK, 'int16', always_2d=True)
    combined = mixer(rundata)
    stream.write(combined.tostring())

# SAMPLE RATE CHANGE
cvstate = None
while data != '':
    newdata, cvstate = audioop.ratecv(
        data, wf_sampwidth, wf_channels, wf_samplerate,
        dev_samplerate, cvstate)
    stream.write(newdata)
data = wf.readframes(CHUNK)


# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
