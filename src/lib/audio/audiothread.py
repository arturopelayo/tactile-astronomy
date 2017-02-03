
import threading
import time
import logging

from audiofile import AudioFile

import pyaudio

from audiomixer import AudioMixer

class AudioThread(threading.Thread):
    def __init__(self, eventhub):
        super(AudioThread, self).__init__()
        self.eventhub = eventhub
        self.daemon = True
        self.running = False
        self.voices = {
            'narration': None,
            'system': None,
        }
        self.register(eventhub)

    def start(self):
        self.running = True
        super(AudioThread, self).start()

    def process_events(self):
        # process mail
        mail = self._mailbox.get_all()
        for msg in mail:
            # work out narration or system
            _, name, command = msg['namespace'].split('.')
            voice = self.voices[name]
            if command == 'play':
                path = msg.get('path')
                if path is not None:
                    # stop and change track
                    if voice is not None:
                        voice.stop()
                    voice = AudioFile(path)
                if voice is not None:
                    voice.play()
            if command == 'pause':
                if voice is not None:
                    voice.pause()
            elif command == 'stop' :
                if voice is None:
                    logging.warning('Event received to stop inactive voice')
                    continue
                voice.stop()
            self.voices[name] = voice


    def register(self, eventhub):
        namespaces = []
        for name in self.voices:
            for command in ["play", "stop", "pause"]:
                namespaces += ['audio.%s.%s' % (name, command)]
        self._mailbox = eventhub.subscribe(namespaces)

    def run(self):
        # open stream (2)
        p = pyaudio.PyAudio()
        speaker = p.open(format=pyaudio.paInt16,
                         channels=2,
                         rate=44100,
                         output=True)
        mixer = AudioMixer()
        CHUNK = 1024
        while self.running:
            # read events
            self.process_events()

            voicedata = []
            for name, voice in self.voices.items():
                if voice is None or not voice.is_playing:
                    continue
                data = voice.read(CHUNK)
                if len(data) > 0:
                    voicedata += [data]

            if len(voicedata) == 0:
                time.sleep(0.3)
            else:
                combined = mixer.mixdown(voicedata)
                speaker.write(combined.tostring())

            # read chunks for each track
            # mix chunks down
            # output to speaker
