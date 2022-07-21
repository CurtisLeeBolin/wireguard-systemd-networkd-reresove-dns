#!/usr/bin/env python3
#
#  wireguard-systemd-networkd-reresove-dns.py
#  Copyright (C) 2022 Curtis Lee Bolin <CurtisLeeBolin@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import os
import fnmatch
import re
import time

for fileName in os.listdir('/etc/systemd/network/'):
  if fnmatch.fnmatch(fileName, 'wg*.netdev'):
    file = '/etc/systemd/network/{}'.format(fileName)

    _unique = 0
    config = {}

    with open(file, 'r', encoding="utf-8") as f:
      for line in f.readlines():
        line = line[:-1]
        line = line.strip()
        if line:
          if not line[0] == '#':
            if line[0] == '[':
              section = line[1:-1]
              if section == 'WireGuardPeer':
                _unique += 1
                section += str(_unique)
              if section not in config:
                config[section] = {}
              else:
                raise Exception('Section \'{}\' already exists in dict.'.format(section))
            else:
              (key, val) = line.split('=', 1)
              if key not in config[section]:
                  config[section][key] = val
              else:
                raise Exception('Key \'{}\' already exists in section \'{}\'.'.format(key, section))
    interface = config['NetDev']['Name']
    epochSeconds = int(time.time())
    latest_handshakesString = os.popen('wg show {} latest-handshakes'.format(interface))
    latest_handshakesDict = {}
    for line in latest_handshakesString.readlines():
      (publicKey, handshakeTime) = line.split('\t')
      latest_handshakesDict[publicKey] = int(handshakeTime)
    for section in config:
      if fnmatch.fnmatch(section, 'WireGuardPeer*'):
        if 'Endpoint' in config[section].keys():
          publicKey = config[section]['PublicKey']
          endpoint = config[section]['Endpoint']
          (server, port) = endpoint.split(':')
          if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", server):
            if (epochSeconds - latest_handshakesDict[publicKey]) > 135:
              os.popen('wg set {} peer {} endpoint {}'.format(interface, publicKey, endpoint))
              print('Updating {} {} {}'.format(interface, publicKey, endpoint))
