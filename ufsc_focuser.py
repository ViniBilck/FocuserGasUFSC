#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# chimera - observatory automation system
# Copyright (C) 2006-2007  P. Henrique Silva <henrique@astro.ufsc.br>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from chimera.core.lock import lock

from chimera.interfaces.focuser import (FocuserFeature,
                                        InvalidFocusPositionException, FocuserAxis)

from chimera.instruments.focuser import FocuserBase

import serial

import time




class FakeFocuser(FocuserBase):

    def __init__(self):
        FocuserBase.__init__(self)
        self._port = self['device']
        self._baudrate = 9600
        self._focusConfig = {"dt": 26.768, #Seconds
                             "pulse_dt": 0.2, #Seconds
                             "function_coef": [2.74463053, 0.45783398],
                             }
        try:
            self.ser = serial.Serial(self['device'], self._baudrate, timeout=1)
            time.sleep(2)
            print "Connected to {} at {} baud.".format(self['device'], self._baudrate)
        except serial.SerialException as e:
            print "Failed to connect to {}: {}".format(self['device'], e)
            self.ser = None

        self._supports = {FocuserFeature.TEMPERATURE_COMPENSATION: False,
                          FocuserFeature.POSITION_FEEDBACK: True,
                          FocuserFeature.ENCODER: True,
                          FocuserFeature.CONTROLLABLE_X: False,
                          FocuserFeature.CONTROLLABLE_Y: False,
                          FocuserFeature.CONTROLLABLE_Z: True,
                          FocuserFeature.CONTROLLABLE_U: False,
                          FocuserFeature.CONTROLLABLE_V: False,
                          FocuserFeature.CONTROLLABLE_W: False,
                          }
        self._range = (0, int(self._focusConfig['dt'] / float(self._focusConfig["pulse_dt"])))
        self._position = 0
        self._mov = 0

    def __start__(self):
        self["model"] = "Fake Focus v.1"


    def getTime(self, position):
        new_time = (-self._focusConfig['function_coef'][0] + position) / self._focusConfig['function_coef'][1]
        return new_time

    @lock
    def moveIn(self, n, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        time_spend = self._focusConfig['pulse_dt'] * n
        target = self.getPosition() + n
        if self._inRange(target):
            if self.ser and self.ser.is_open:
                self.ser.write(b'L')
                time.sleep(time_spend)
                self.ser.write(b'S')
                self._setPosition(target)
                print "Sent command to move in."
            else:
                print "Serial connection not open. Cannot send command."
        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % target)

    @lock
    def moveOut(self, n, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        time_spend = self._focusConfig['pulse_dt'] * n
        target = self.getPosition() + n
        if self._inRange(target):
            if self.ser and self.ser.is_open:
                self.ser.write(b'H')
                time.sleep(time_spend)
                self.ser.write(b'S')
                self._setPosition(target)
                print "Sent command to move in."
            else:
                print "Serial connection not open. Cannot send command."

        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % target)

    @lock
    def moveTo(self, position, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        if self._inRange(position):
            if position < self.getPosition():
                self._mov = self.getPosition() - position
                self.moveIn(self._mov)
                self._setPosition(position)

            if self.getPosition() < position:
                self._mov = position - self.getPosition()
                self.moveOut(self._mov)
                self._setPosition(position)

        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % int(position))
    @lock
    def getPosition(self, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        return self._position

    def getRange(self, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        return self._range

    def _setPosition(self, n):
        self.log.info("Changing focuser to %s" % n)
        self._position = n

    def _inRange(self, n):
        min_pos, max_pos = self.getRange()
        return (min_pos <= n <= max_pos)
