from periphery import PWM

# Open PWM channel 0, pin 0
pwm = PWM(0, 0)

# Set frequency to 1 kHz
pwm.frequency = 1e3
# Set duty cycle to 75%
pwm.duty_cycle = 0.75

pwm.enable()

time.sleep(1)

# Change duty cycle to 50%
pwm.duty_cycle = 0.50

time.sleep(1)

pwm.disable()

pwm.close()


# playlist = [
#     ("io.vibe", duration=0.5, strength=1.0),
#     ("io.vibe", delay=1.0, strength=1.0, duration=0.5)
# ]

playlist = {
    'default': [
        ('play.audio': 'http://service.example/intro.ogg'),
        ('delay': 1.0),
        ('play.system': 'alerts/tone.ogg'),
    ],
    'menu': [
        ('play.audio': 'template/menu/press_A.ogg'),
        ('delay': 1.0),
        ('play.audio': 'http://service.example/optionA.ogg'),
    ],
}
