from collections import defaultdict
from Queue import Queue, Empty
import logging
import time

class EventHub(object):
    def __init__(self):
        self.registry = defaultdict(list)

    def subscribe(self, namespace):
        if type(namespace) not in (list, tuple):
            namespace = [namespace]
        mailbox = EventMailbox(namespace)
        for ns in namespace:
            self.registry[ns] += [mailbox]
        return mailbox

    def emit(self, namespace, **kwargs):
        logging.info("Event received: " + namespace + ' ' + str(kwargs))
        mailboxes = self.registry[namespace]
        kwargs['timestamp'] = time.time()
        kwargs['namespace'] = namespace
        if len(mailboxes) == 0:
            logging.warning('Warning: received event for unregistered namespace "%s"' % namespace)
        for box in mailboxes:
            box.put(kwargs)

class EventMailbox(Queue, object):
    def __init__(self, namespace):
        super(EventMailbox, self).__init__()
        self.namespace = namespace
    def get_all(self):
        msgs = []
        while True:
            try:
                msg = self.get_nowait()
                if msg is not None:
                    msgs += [msg]
                    self.task_done()
            except Empty:
                return msgs
