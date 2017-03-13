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

# open stream (2)
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=sound.samplerate,
                output=True)

voices = [sound]

N = 2
OFFSET = 1
start = time.time()

voices += [soundfile.SoundFile(sys.argv[1], 'r') for i in range(N)]
datas = [sound.read(CHUNK, 'int16', always_2d=True) for sound in voices]
start_times = [(start + OFFSET * i) for i in range(N + 1)]

def mixer(voices):
    active_voices = filter(lambda x: x is not None, voices)
    if len(active_voices) > 1:
        lengths = [len(v) for v in active_voices]
        max_len = max(lengths)
        min_len = min(lengths)
        # if there are differences in lengths, we need to pad
        if max_len != min_len:
            for i in range(len(active_voices)):
                len_diff = max_len - len(active_voices[i])
                if len_diff > 0:
                    # pad difference with zeroes
                    active_voices[i] = numpy.pad(active_voices[i],
                                                 ((0, len_diff), (0, 0)),
                                                 'constant',
                                                 constant_values=(0, 0))
    return numpy.mean(active_voices, axis=0, dtype=numpy.int16)

# play stream (3)
lap_time = time.time()
while any([len(d) > 0 for d in datas]) or any(st > lap_time for st in start_times):
    rundata = []
    lap_time = time.time()
    for i in range(len(voices)):
        if start_times[i] > lap_time or len(datas[i]) == 0:
            rundata += [None]
        else:
            rundata += [datas[i]]
            datas[i] = voices[i].read(CHUNK, 'int16', always_2d=True)
    combined = mixer(rundata)
    stream.write(combined.tostring())


# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
