# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Nathan Young
#
# SPDX-License-Identifier: MIT
"""
`unicornhathd`
================================================================================

CircuitPython framebuf based driver for Pimoroni's Unicorn HAT HD


* Author(s): Nathan Young

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni's Unicorn HAT HD <https://shop.pimoroni.com/products/unicorn-hat-hd>`

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

# * Adafruit's framebuf library: https://github.com/adafruit/Adafruit_CircuitPython_framebuf
"""

# imports__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/NathanY3G/CircuitPython_Unicorn_HAT_HD.git"

from micropython import const
from adafruit_framebuf import FrameBuffer, RGB888

try:
    # Only used for type hints
    import busio
    import digitalio
except ImportError:
    pass


START_OF_FRAME = const(0x72)


class UnicornHATHD:
    def __init__(
        self,
        spi: busio.SPI,
        chip_select_pin: digitalio.DigitalInOut,
        frequency: int = 5_000_000,
    ):
        self._spi = spi
        self._frequency = frequency
        self._chip_select_pin = chip_select_pin
        self._frame_buffer = FrameBuffer(
            bytearray(self.width * self.height * 3), self.width, self.height, RGB888
        )

    @property
    def width(self) -> int:
        return 16

    @property
    def height(self) -> int:
        return 16

    @property
    def depth(self) -> int:
        return 8

    @property
    def rotation(self) -> int:
        return self._frame_buffer.rotation

    @rotation.setter
    def rotation(self, val: int) -> None:
        self._frame_buffer.rotation = val

    def fill(self, color: int) -> None:
        self._frame_buffer.fill(color)

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        self._frame_buffer.fill_rect(x, y, width, height, color)

    def pixel(self, x, y, color=None) -> None:
        self._frame_buffer.pixel(x, y, color)

    def hline(self, x: int, y: int, width: int, color: int) -> None:
        self._frame_buffer.hline(x, y, width, color)

    def vline(self, x: int, y: int, height: int, color: int) -> None:
        self._frame_buffer.vline(x, y, height, color)

    def line(self, x_0: int, y_0: int, x_1: int, y_1: int, color: int) -> None:
        self._frame_buffer.line(x_0, y_0, x_1, y_1, color)

    def circle(self, center_x: int, center_y: int, radius: int, color: int) -> None:
        self._frame_buffer.circle(center_x, center_y, radius, color)

    def rect(
        self, x: int, y: int, width: int, height: int, color: int, *, fill: bool = False
    ) -> None:
        self._frame_buffer.rect(x, y, width, height, color, fill=fill)

    def text(self, string, x, y, color, *, font_name="font5x8.bin", size=1) -> None:
        self._frame_buffer.text(string, x, y, color, font_name=font_name, size=size)

    def image(self, img) -> None:
        self._frame_buffer.image(img)

    def scroll(self, delta_x: int, delta_y: int) -> None:
        self._frame_buffer.scroll(delta_x, delta_y)

    def show(self) -> None:
        """Update the display"""
        while not self._spi.try_lock():
            pass

        self._spi.configure(baudrate=self._frequency, phase=0, polarity=0)

        self._chip_select_pin.value = False

        self._spi.write(bytearray([START_OF_FRAME]))
        self._spi.write(self._frame_buffer.buf)

        self._chip_select_pin.value = True

        self._spi.unlock()