import time
import logging
import threading

from nfcreader import NFC

class NFCThread(threading.Thread):
    def __init__(self, eventhub):
        super(NFCThread, self).__init__()
        self.eventhub = eventhub
        self.daemon = True
        self.running = False

    def start(self):
        self.running = True
        super(NFCThread, self).start()

    def run(self):
        nfc = NFC()
        nfc.open()
        last_id = None
        while self.running:
            try:
                tag = nfc.read()
                if tag.uid != last_id:
                    self.eventhub.emit('nfc.tagchange', uid=tag.uid)
                    last_id = tag.uid
                time.sleep(0.5)
            except Exception as err:
                logging.exception('NFCThread')
                time.sleep(1)
