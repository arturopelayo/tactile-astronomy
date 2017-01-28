modprobe i2c-dev
modprobe snd-bcm2835
# after changes are pushed by resin, new libraries are not seen for some reason
# ldconfig fixes this
ldconfig
python app.py
