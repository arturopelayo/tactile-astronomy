
import evdev
from evdev import ecodes
from select import select

from lib.eventhub import EventHub
from lib.io import IOThread
from lib.nfc import NFCThread
from lib.audio import AudioThread

import threading
import logging
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

class MainThread(threading.Thread):
    def __init__(self, eventhub):
        super(MainThread, self).__init__()
        self.eventhub = eventhub
        self.daemon = True
        self.running = False

        self._mailbox = eventhub.subscribe(['nfc.tagchange'])

    def start(self):
        self.running = True
        super(MainThread, self).start()

    def process_events(self):
        # process mail
        mail = self._mailbox.get_all()
        for msg in mail:
            if msg['namespace'] == 'nfc.tagchange':
                print msg
                self.eventhub.emit('io.beep', duration=0.5)

    def run(self):
        while self.running:
            self.process_events()
            time.sleep(0.1)

def handle_keyevents(eventhub):
    devices = map(evdev.InputDevice, evdev.list_devices())
    devices = {dev.fd: dev for dev in devices}
    while True:
        r, _, _ = select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                if event.type != ecodes.EV_KEY:
                    continue
                event = evdev.KeyEvent(event)
                if event.keycode == "KEY_A":
                    eventhub.emit('io.beep', duration=0.5)
                elif event.keycode == "KEY_S":
                    eventhub.emit('io.vibration', duration=0.5)
                elif event.keycode == "KEY_D":
                    eventhub.emit('audio.narration.pause', duration=0.5)
                elif event.keycode == "KEY_F":
                    eventhub.emit('audio.narration.stop', duration=0.5)
                elif event.keycode == "KEY_G":
                    song = os.path.join(BASE_DIR, '..', 'tests', 'sound', 'ACDC_-_Back_In_Black-sample.ogg')
                    eventhub.emit('audio.narration.play', path=song)
                elif event.keycode == "KEY_H":
                    song = os.path.join(BASE_DIR, '..', 'tests', 'sound', 'Coldplay_-_The_Scientist.ogg')
                    eventhub.emit('audio.narration.play', path=song)

def main():
    eventhub = EventHub()
    threads = {}
    threads['io'] = IOThread(eventhub)
    threads['main'] = MainThread(eventhub)
    threads['nfc'] = NFCThread(eventhub)
    threads['audio'] = AudioThread(eventhub)

    for name in threads:
        threads[name].start()

    handle_keyevents(eventhub)

main()
