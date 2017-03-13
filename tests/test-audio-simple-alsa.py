"""PyAudio Example: Play a wave file."""

import alsaaudio
import wave
import sys
import soundfile as sf

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)



wf = wave.open(sys.argv[1], 'rb')

device = alsaaudio.PCM()
device.setchannels(wf.getnchannels())
device.setrate(wf.getframerate())

# 8bit is unsigned in wav files
if wf.getsampwidth() == 1:
    device.setformat(alsaaudio.PCM_FORMAT_U8)
# Otherwise we assume signed data, little endian
elif wf.getsampwidth() == 2:
    device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
elif wf.getsampwidth() == 3:
    device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
elif wf.getsampwidth() == 4:
    device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
else:
    raise ValueError('Unsupported format')

device.setperiodsize(CHUNK)

# instantiate PyAudio (1)
# p = pyaudio.PyAudio()

# open stream (2)
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    # stream.write(data)
    device.write(data)
    data = wf.readframes(CHUNK)




# stop stream (4)
# stream.stop_stream()
# stream.close()

# close PyAudio (5)
# p.terminate()
