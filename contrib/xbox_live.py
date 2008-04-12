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

"""Displays a list of your Xbox Live friends that are online.

This script requires:
  -BeautifulSoup, http://www.crummy.com/software/BeautifulSoup/
  -mechanize, http://wwwsearch.sourceforge.net/mechanize/
  -ClientForm, http://wwwsearch.sourceforge.net/ClientForm/

"""
from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import channel
import getpass
import pertelian
import sys
import time
import traceback
import urllib2

FRIEND_TABLE_CLASS = 'XbcProfileTable XbcFriendsListTable'
GAMER_TAG_CLASS = 'XbcGamerTag'
GAMER_PRESENCE_CLASS = 'XbcGamerPresence'


class XboxLiveError(Exception):
  pass


class XboxLive(channel.Channel):

  def SetUp(self):
    print 'Xbox Live Channel Setup'
    print 'Login:',
    self.login = str(raw_input())
    self.passwd = getpass.getpass()

  def GetXboxLiveFriends(self):
    """Return a list of tuples (gamer_tag, gamer_presence)."""
    br = Browser()
    br.open('http://live.xbox.com/en-US/profile/Friends.aspx')
    br.select_form(name='f1')
    br['login'] = self.login
    br['passwd'] = self.passwd
    br.submit()  # Submit login form.
    br.select_form(name='fmHF')
    response = br.submit()  # Submit redirect form.
    friend_list = response.read()
    response.close()

    soup = BeautifulSoup(friend_list)
    friend_table = soup.find('table', {'class': FRIEND_TABLE_CLASS})
    if friend_table is None:
      raise XboxLiveError('Parsing failure.')

    friends = []
    for row in friend_table.contents[1:]:  # Skip header row.
      gamer_tag = row.find('td', {'class': GAMER_TAG_CLASS})
      gamer_tag = str(gamer_tag.find('a').contents[0])
      gamer_presence = row.find('td', {'class': GAMER_PRESENCE_CLASS})
      gamer_presence = str(gamer_presence.find('h4').contents[0])
      friends.append((gamer_tag, gamer_presence))
    return friends

  def Display(self):
    try:
      friends = self.GetXboxLiveFriends()
    except (urllib2.URLError, XboxLiveError):
      print 'Error on %s'.center(80, '*') % time.ctime()
      traceback.print_exc()
      self.pert.Clear()
      self.pert.WrapMessage('Failed to retrieve friends list.')
    else:
      online = []
      for friend in friends:
        if friend[1] == 'Online':
          online.append(friend[0])
      online.sort()
      self.pert.Clear()
      if online:
        self.pert.WrapMessage(', '.join(online))
      else:
        self.pert.WrapMessage('No friends online.')
