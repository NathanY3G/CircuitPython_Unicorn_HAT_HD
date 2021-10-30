# SPDX-FileCopyrightText: Copyright (c) 2021 Nathan Young
#
# SPDX-License-Identifier: MIT
from time import sleep

import board
from digitalio import DigitalInOut, Direction
from rainbowio import colorwheel

from unicornhathd import UnicornHATHD

# TODO: Change this pin to match your wiring
chip_select_pin = DigitalInOut(board.D0)
chip_select_pin.direction = Direction.OUTPUT
chip_select_pin.value = True

display = UnicornHATHD(board.SPI(), chip_select_pin)

# Display rainbow colours ♥
for i in range(0, display.width * display.height):
    pixel_colour = colorwheel(i % 256)
    display.pixel(i // display.width, i % display.width, pixel_colour)

display.show()

sleep(60)
