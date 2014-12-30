#!/usr/bin/env python
#
# i2cdisplayr.py
#
# Copyright (c) 2014 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
import argparse
import smbus

class MPTHDisplay(object):

    def __init__(self, bus, chip_address, width=16, height=2):
        """ Construct a display with a port number of i2c bus and chip address.

        Args:
          bus: an integer port number of i2c bus.
          chip_addres: an integer chip address.
          width: width of the display.
          height: height of the display.
        """
        self._bus = smbus.SMBus(bus)
        self._chip_address = chip_address

        self._width = width
        self._height = height
        self._x = 0
        self._y = 0

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def write(self, s):
        """ Write a string to the display.
        
        Args:
          s: a string.
        """
        if "\n" in s:
            self.writelines(s.split("\n"))

        else:
            self._raw_write(map(ord, s))

    def writelines(self, lines):
        """ Write lines.
        
        Args:
          lines: a list of strings.
        """
        for line in lines:
            self.write(line)
            self.newline()

    def newline(self):
        """ Write a new line.
        """
        self._raw_write([0x20]*(self.width-self._x))

    def clear(self):
        """ Clear display.
        """
        self._raw_write([0x80, 0x05, 0x01])

    def cursor(self, on):
        """ Turn on/off a cursor.

        Args:
          on: If True, a cursor will be shown.
        """
        if on:
            self._raw_write([0x80, 0x05, 0x0e])
        else:
            self._raw_write([0x80, 0x05, 0x0c])

    def backlight(self, value):
        """ Change blightness of the back light.

        Args:
          value: an integer in 0 to 255.
        """
        if value < 0 or value > 255:
            raise ValueError("value must be in 0 to 255.")
        self._raw_write([0x80, 0x01, value])

    def _incliment(self, v):
        self._x += v
        self._x = self._x % self.width
        self._y += self._x / self.width
        self._y %= self.height   

    def _raw_write(self, s):
        self._bus.write_i2c_block_data(self._chip_address, s[0], s[1:])
        self._incliment(len(s))


def _cbool(v):
    if v.lower() == "false":
        return False
    else:
        return True


def _write_action(display, input, **kwargs):
    if len(input) == 1:
        display.write(input[0])
    else:
        display.writelines(input)


def _clear_action(display, **kwargs):
    display.clear()


def _cursor_action(display, on, **kwargs):
    display.cursor(on)


def _bl_action(display, value, **kwargs):
    display.backlight(value)


def _exec(func, bus, address, width, height, **kwargs):
    display = MPTHDisplay(bus, address, width, height)
    func(display, **kwargs)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("bus", type=int, help="an integer port number of i2c bus.")
    parser.add_argument("address", type=int, help="an integer chip address.")
    parser.add_argument("-W", "--width", default=16, type=int,
                        help="width of the display. (default: 16)")
    parser.add_argument("-H", "--height", default=2, type=int,
                        help="height of the display. (default: 2)")

    subparsers = parser.add_subparsers()
    
    write_cmd = subparsers.add_parser("write", help="show texts.")
    write_cmd.add_argument("input", nargs="+")
    write_cmd.set_defaults(func=_write_action)

    clear_cmd = subparsers.add_parser("clear", help="clear display.")
    clear_cmd.set_defaults(func=_clear_action)
        
    cursor_cmd = subparsers.add_parser("cursor", help="on/off a cursor.")
    cursor_cmd.add_argument("on", type=_cbool, help="If True, a cursor will be shown.")
    cursor_cmd.set_defaults(func=_cursor_action)

    bl_cmd = subparsers.add_parser("backlight", help="change blightness.")
    bl_cmd.add_argument("value", type=int, help="an integer in 0-255.")
    bl_cmd.set_defaults(func=_bl_action)

    _exec(**vars(parser.parse_args()))
  

if __name__ == "__main__":
    main()
