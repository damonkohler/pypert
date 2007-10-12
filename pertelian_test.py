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

"""Tests for Python interface to the Pertelian X2040 display."""

import unittest
import pertelian


class MockPertelian(pertelian.Pertelian):

  """Mock out the serial port parts of Pertelian for testing."""

  def __init__(self, tty='tty'):
    pass

  def _Setup(self):
    pass

  def __del__(self):
    pass

  def _SendBytes(self, bytes, delay=0, pack='B'):
    raise NotImplementedError


class TestPertelian(unittest.TestCase):

  def testWrapMessage(self):
    msgs = [
        'This is the longest message and should use all four lines of display.',
        'This is a very long message that should be wrapped properly.',
        'This one is not quite as long.',
        ]
    p = MockPertelian()
    p.Message = lambda msg: lines.append(msg)
    for msg in msgs:
      lines = []
      p.WrapMessage(msg)
      print lines
      for line in lines:
        self.assertEqual(len(line), pertelian.CHARACTER_WIDTH,
            '%r is the wrong length.' % line)


if __name__ == '__main__':
  unittest.main()
