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

"""Gmail notifier channel."""

import os

import channel
import feedparser
import getpass

GMAIL_FEED = 'https://%s:%s@gmail.google.com/gmail/feed/atom'


class GmailNotifier(channel.Channel):

  def SetUp(self):
    print 'Gmail Notifier Channel Setup'
    while True:
      print 'Login:',
      self.login = str(raw_input())
      self.passwd = getpass.getpass()
      if 'Error' in self.GetFeed().feed.subtitle:
        print 'Error. Please try again.'
      else:
        break

  def GetFeed(self):
    return feedparser.parse(GMAIL_FEED % (self.login, self.passwd))

  def Display(self):
    d = self.GetFeed()
    new_messages = int(d.feed.fullcount)
    authors = ', '.join(str(e.author_detail.name) for e in d.entries)
    self.pert.Clear()
    if new_messages:
      self.pert.WrapMessage(
          '%d new messages: %s' % (new_messages, authors))
    else:
      self.pert.WrapMessage('No new messages.')
