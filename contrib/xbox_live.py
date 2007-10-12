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
import pertelian
import sys
import time
import traceback
import urllib2

FRIEND_TABLE_CLASS = 'XbcProfileTable XbcFriendsListTable'
GAMER_TAG_CLASS = 'XbcGamerTag'
GAMER_PRESENCE_CLASS = 'XbcGamerPresence'


def GetXboxLiveFriends(login, passwd):
  """Return a list of tuples (gamer_tag, gamer_presence)."""
  br = Browser()
  br.open('http://live.xbox.com/en-US/profile/Friends.aspx')
  br.select_form(name='f1')
  br['login'] = login
  br['passwd'] = passwd
  br.submit()  # Submit login form.
  br.select_form(name='fmHF')
  response = br.submit()  # Submit redirect form.
  friend_list = response.read()
  response.close()

  soup = BeautifulSoup(friend_list)
  friend_table = soup.find('table', {'class': FRIEND_TABLE_CLASS})
  friends = []
  for row in friend_table.contents[1:]:  # Skip header row.
    gamer_tag = row.find('td', {'class': GAMER_TAG_CLASS})
    gamer_tag = str(gamer_tag.find('a').contents[0])
    gamer_presence = row.find('td', {'class': GAMER_PRESENCE_CLASS})
    gamer_presence = str(gamer_presence.find('h4').contents[0])
    friends.append((gamer_tag, gamer_presence))
  return friends


if __name__ == '__main__':
  assert len(sys.argv) == 3, 'Usage: xbox_live.py login passwd'
  login, passwd = sys.argv[1:3]
  try:
    p = pertelian.Pertelian()
    while True:
      try:
        friends = GetXboxLiveFriends(login, passwd)
      except urllib2.URLError:
        traceback.print_exc()
        p.Clear()
        p.WrapMessage('Failed to retrieve friends list.')
      else:
        online = []
        for friend in friends:
          if friend[1] == 'Online':
            online.append(friend[0])
        online.sort()
        p.Clear()
        if online:
          p.Backlight(True)
          p.WrapMessage(', '.join(online))
        else:
          p.Backlight(False)
          p.WrapMessage('No friends online.')
      time.sleep(30)
  except KeyboardInterrupt:
    pass
