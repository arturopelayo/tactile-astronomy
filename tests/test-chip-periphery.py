import time

from periphery import GPIO

# Open GPIO 10 with input direction
gpio = {}
gpio["user_btn1"] = GPIO(117, "in")
gpio["user_btn2"] = GPIO(119, "in")
gpio["user_btn3"] = GPIO(122, "in")
gpio["user_btn4"] = GPIO(121, "in")
gpio["aux_btn1"] = GPIO(131, "in")
gpio["aux_btn2"] = GPIO(133, "in")
gpio["reset_btn"] = GPIO(129, "in")
# Open GPIO 12 with output direction
gpio["led1_blue"] = GPIO(134, "out")
gpio["led1_green"] = GPIO(136, "out")
gpio["led1_red"] = GPIO(138, "out")

gpio["led2_blue"] = GPIO(135, "out")
gpio["led2_green"] = GPIO(137, "out")
gpio["led2_red"] = GPIO(139, "out")

try:
    while True:
        gpio["led1_red"].write(gpio["user_btn1"].read())
        gpio["led1_green"].write(gpio["user_btn2"].read())
        gpio["led1_blue"].write(gpio["user_btn3"].read())
        gpio["led2_red"].write(gpio["user_btn4"].read())
        gpio["led2_green"].write(gpio["aux_btn1"].read())
        gpio["led2_blue"].write(gpio["aux_btn2"].read())
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    for io in gpio.values():
        io.close()



# LCD_D21 - USER_BTN1 - 117
# LCD_D23 - USER_BTN2 - 119
# LCD_HSYNC - USER_BTN3 - 122
# LCD_DE - USER_BTN4 - 121
#
# LED1_BLUE - CSID2 - 134
# LED1_GREEN - CSID4 - 136
# LED1_RED - CSID6 - 138
#
# CSICK - RESET_BTN - 129
# CSIVSYNC - AUX_BTN1 - 131
# CSID1 - AUX_BTN2 - 133
# CSID3 - LED2_BLUE - 135
# CSID5 - LED2_GREEN - 137
# CSID7 - LED2_RED - 139
