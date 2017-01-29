
import mraa
import time
import logging

class OutputIO(object):

    def __init__(self, pin, namespace, value=0):
        self._io = mraa.Gpio(pin)
        self.expiry = 0
        self.value = value
        self.namespace = namespace

        self._io.dir(mraa.DIR_OUT)
        self._io.write(value)

    def register(self, eventhub):
        self._mailbox = eventhub.subscribe(self.namespace)

    def process_events(self):
        # process mail
        mail = self._mailbox.get_all()
        for msg in mail:
            time_now = time.time()
            # ignore expired messages
            deadline = msg['timestamp'] + msg.get('duration', 0.5)
            if deadline < time_now:
                logging.info('Dropping too old event - %0.1f secs too late' % (time_now - deadline))
                continue
            self.expiry = max(deadline, self.expiry)
        # set outputs
        time_now = time.time()
        if self.expiry > time_now:
            self._io.write(1)
        else:
            self._io.write(0)
