
from nfclib import (
    nfc_context, nfc_version, nfc_init, nfc_list_devices, nfc_connstring,
    nfc_open, nfc_initiator_init, nfc_device_get_name,
    nfc_initiator_select_passive_target, nfc_initiator_poll_target,
    nfc_modulation, NMT_ISO14443A, NBR_106, nfc_close, nfc_exit, nfc_target
)

from ctypes import (
    pointer, byref
)

def bytes_to_int(bytes, length):
    value = 0
    for i in range(length):
        b = bytes[i]
        value <<= 8
        value |= b
    return value

def bytes_to_hex(bytes, length):
    if length == 0:
        return None
    value = []
    for i in range(length):
        value += [hex(bytes[i])[2:].rjust(2, '0')]
    return ''.join(value)

class NFCTarget(object):
    def __init__(self, target):
        nai = target.nti.nai
        self.atqs = bytes_to_hex(nai.abtAtqa, 2)
        self.sak = bytes_to_hex([nai.btSak], 1)
        self.uid = bytes_to_hex(nai.abtUid, nai.szUidLen)
        self.ats = bytes_to_hex(nai.abtAts, nai.szAtsLen)

class NFC(object):

    def __init__(self):
        self._context = pointer(nfc_context())
        self._device = None

        nfc_init(byref(self._context))
        if self._context is None:
            raise Exception("Unable to init libnfc")

    def __del__(self):
        if self._device:
            nfc_close(self._device)
            self._device = None
        if self._context:
            nfc_exit(self._context)
            self._context = None

    def list_devices(self, count=1):
        devices = (nfc_connstring * 1)()
        count = nfc_list_devices(self._context, devices, 1)
        return [d for d in devices[:count]]

    def open(self, path=None):
        if path is None:
            devices = self.list_devices(count=1)
            if len(devices) == 0:
                raise Exception('No NFC devices found')
            path = devices[0]
        self._device = nfc_open(self._context, path)
        if self._device is None:
            raise Exception('Unable to open NFC device')
        if nfc_initiator_init(self._device) < 0:
            raise Exception("Unable to set device to initiator mode")

    def close(self):
        if self._device:
            nfc_close(self._device)
            self._device = None

    def device_name(self):
        if self._device:
            return str(nfc_device_get_name(self._device))

    def read(self, blocking=True, interval=10):
        modulation = nfc_modulation()
        modulation.nmt = NMT_ISO14443A
        modulation.nbr = NBR_106

        target = nfc_target()

        if blocking:
            result = nfc_initiator_select_passive_target(self._device,
                                                         modulation, None, 0,
                                                         byref(target))
            if result < 0:
                raise Exception("NFC select returned negative return code")
        else:
            TIMES_TO_POLL = 1
            result = nfc_initiator_poll_target(self._device,
                                               byref(modulation), 1,
                                               TIMES_TO_POLL,
                                               interval,
                                               byref(target))
            if result < 0:
                raise Exception("NFC poll returned negative return code")

        if result > 0:
            data = NFCTarget(target)
            return data
        elif result == 0:
            return None
        else:
            raise Exception("NFC negative return code")
