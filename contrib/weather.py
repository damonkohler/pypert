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

import channel
import pymetar


class Weather(channel.Channel):

  def SetUp(self):
    print 'Weather Channel'
    if self.settings:
      self.icao = self.settings['icao']
      print 'Loaded saved settings.'
    else:
      print 'ICAO:',
      self.icao = str(raw_input())
      self.Save({'icao': self.icao})

  def Display(self):
    fetcher = pymetar.ReportFetcher()
    report = fetcher.FetchReport(self.icao)
    parser = pymetar.ReportParser()
    parser.ParseReport(report)
    temperature = report.getTemperatureCelsius()
    # NOTE(damonkohler): There is no 'Weather' heading for clear weather.
    weather = report.getWeather() or 'Clear'
    self.pert.Clear()
    self.pert.WrapMessage('%d\xdfC %s' % (temperature, weather))
