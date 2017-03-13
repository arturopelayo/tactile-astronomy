#!/usr/bin/python

from mraa import Gpio, DIR_OUT
import time


PIN_BEEP = 12
PIN_VIBRATION = 16

beep_io = Gpio(PIN_BEEP)
beep_io.dir(DIR_OUT)

vibr_io = Gpio(PIN_VIBRATION)
vibr_io.dir(DIR_OUT)

beep_io.write(1)
time.sleep(0.5)
beep_io.write(0)
time.sleep(1)
vibr_io.write(1)
time.sleep(0.5)
vibr_io.write(0)
time.sleep(1)
