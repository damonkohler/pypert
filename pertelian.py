#!/usr/bin/python

# The MIT License
#
# Copyright (c) 2007 Damon Kohler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Python interface to the Pertelian X2040 display."""

import serial
import struct
import time

CHARACTER_WIDTH = 20  # Number of characters that will fit on a line.
INSTRUCTION_DELAY = 0.01  # Number of seconds to wait between bytes.


class Pertelian(object):

  def __init__(self, tty='/dev/ttyUSB0'):
    self.ser = serial.Serial(tty)
    self.ser.open()
    self._Setup()

  def __del__(self):
    """Close the serial connection when this object is destroyed."""
    self.ser.close()

  def _Setup(self):
    """Set up the display.

    Function set with 8-bit data length, 2 lines, and 5x7 dot size.
    Entry mode set; increment cursor direction; do not automatically shift.
    Cursor/display shift; cursor move.
    Display On; cursor off; do not blink.

    """
    for byte in (0x38, 0x06, 0x10, 0x0c, 0x01):
      self._SendInstruction(byte)

  def _SendBytes(self, bytes, delay=INSTRUCTION_DELAY, pack='B'):
    """Send a stream of bytes to the Pertelian.

    Also, sleep for delay seconds between sending each byte.

    """
    for byte in struct.pack(pack * len(bytes), *bytes):
      self.ser.write(byte)
      time.sleep(delay)

  def _SendInstruction(self, byte):
    """Send an instruction byte to the Pertelian."""
    self._SendBytes((0xfe, byte))

  def Power(self, on):
    """Turn the power on or off."""
    if on:
      self._SendInstruction(0x0c)
    else:
      self._SendInstruction(0x08)

  def Backlight(self, on):
    """Turn the backlight on or off."""
    if on:
      self._SendInstruction(0x03)
    else:
      self._SendInstruction(0x02)

  def Clear(self):
    """Clear the display."""
    self._SendInstruction(0x01)

  def Message(self, msg):
    """Display a message."""
    self._SendBytes(msg, pack='c')

  def WrapMessage(self, msg):
    """Wrap messages to display on the Pertelian.

    TODO(damonkohler): Add support for words longer than CHARACTER_WIDTH and
    for new lines.

    """
    words = msg.split()
    lines = []
    line = words[0]
    for word in words[1:]:
      assert len(word) <= CHARACTER_WIDTH, 'Word too long.'
      if len(line) + len(word) < CHARACTER_WIDTH:
        line += ' ' + word
      else:
        lines.append(line.ljust(CHARACTER_WIDTH))
        line = word
    lines.append(line.ljust(CHARACTER_WIDTH))
    while len(lines) < 4:
      lines.append(' ' * CHARACTER_WIDTH)  # Add any missing blank lines.
    # The Pertelian displays lines a little out of order.
    self.Message(lines[0])
    self.Message(lines[2])
    self.Message(lines[1])
    self.Message(lines[3])


if __name__ == '__main__':
  p = Pertelian()
  p.Message('Hello World!')
