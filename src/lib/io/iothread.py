
import threading
import time
import logging

from outputs import OutputIO

PIN_BEEP = 12
PIN_VIBRATION = 16

class IOThread(threading.Thread):
    def __init__(self, eventhub):
        super(IOThread, self).__init__()
        self.eventhub = eventhub
        self.daemon = True
        self.running = False

        self.beep = OutputIO(PIN_BEEP, 'io.beep')
        self.beep.register(self.eventhub)
        self.vibe = OutputIO(PIN_VIBRATION, 'io.vibration')
        self.vibe.register(self.eventhub)

    def start(self):
        self.running = True
        super(IOThread, self).start()

    def run(self):
        while self.running:
            try:
                # wait for time
                # read inputs

                # process mail
                self.beep.process_events()
                self.vibe.process_events()
                time.sleep(0.05)
            except Exception as err:
                logging.exception('IOThread')
                time.sleep(1)
