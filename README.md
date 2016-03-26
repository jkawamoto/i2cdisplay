i2cdisplay
==========
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Code Climate](https://codeclimate.com/github/jkawamoto/i2cdisplay/badges/gpa.svg)](https://codeclimate.com/github/jkawamoto/i2cdisplay)

A Python library for LCDs connected via I2C.
Now, this library supports LCDs with SpikenzieLabs's [MPTH](https://www.spikenzielabs.com/SpikenzieLabs/MPTH.html).

Useage
------
Initialize with bus number `<bus>` and device address `<addr>`.
You can find those parameters by `sudo i2cdetect 0` and/or `sudo i2cdetect 1`.

```python
d = MPTHDisplay(<bus>, <addr>)
```

Then, you can write strings, new lines, and clear them.

```python
# Write a single string.
d.write("Hello")

# Write a new line and another string.
d.newline()
d.write("MPTH")

# Clear display.
d.clear()

# Write multi strings.
d.writelines(["Hello", "world"])
```

As a command
-------------
Basic formula is `./i2cdisplay.py <bus> <addr> {write|clear|cursor|backlight}`
where `<bus>` and `<addr>` are the bus number and address of the display.
You also need to run this command as root.

This command has four sub commands; write, clear, cursor, backlight.

### write
Write mult lines.

```sh
./i2cdisplay.py <bus> <addr> write "abc" "def"
```

### clear
Clear display.

```sh
./i2cdisplay.py <bus> <addr> clear
```

### cursor
Turn on/off cursor.

```sh
# Turn on
./i2cdisplay.py <bus> <addr> cursor True
# Turn off
./i2cdisplay.py <bus> <addr> cursor False
```

### backlight
Change backlight's brightness.

```sh
./i2cdisplay.py <bus> <addr> backlight 128 # Chose from 0-255
```

License
--------
This software is released under the MIT License, see LICENSE.
