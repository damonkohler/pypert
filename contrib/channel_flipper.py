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

"""Flips through multiple channels."""

import itertools
import pertelian
import sys
import time
import traceback

import clock
import gmail_notifier
import weather
import xbox_live

CYCLE_DELAY = 5


if __name__ == '__main__':
  p = pertelian.Pertelian()
  p.Backlight(True)
  channels = [
      clock.Clock(p),
      gmail_notifier.GmailNotifier(p),
      weather.Weather(p),
      xbox_live.XboxLive(p),
      ]
  for c in channels:
    try:
      c.SetUp()
    except KeyboardInterrupt:
      sys.exit(1)
    except:
      traceback.print_exc()
  try:
    for c in itertools.cycle(channels):
      try:
        c.Display()
      except KeyboardInterrupt:
        raise
      except:
        traceback.print_exc()
      else:
        time.sleep(CYCLE_DELAY)
  finally:
    for c in channels:
      try:
        c.TearDown()
      except:
        traceback.print_exc()
