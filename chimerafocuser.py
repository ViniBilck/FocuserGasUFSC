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

class GasFocuser (FocuserBase):

    def __init__(self):
        FocuserBase.__init__(self)

        self._position = 0

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
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)
            print "Connected to {} at {} baud.".format(port, baudrate)
        except serial.SerialException as e:
            print "Failed to connect to {}: {}".format(port, e)
            self.ser = None
        
        self.initial_distance = 0.0
        self.distance = 0.0
        self.new_time = 0.0
        self.old_time = 0.0
        self.mov_time = 0.0
        self.coef = [2.74463053, 0.45783398]



    def __start__(self):
        self._position = int(self.getRange()[1] / 2.0)
        self["model"] = "Gas Focus v.1"

    @lock
    def moveIn(self, n, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        target = self.getPosition() - n

        if self._inRange(target):
            self._setPosition(target)
        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % target)

    @lock
    def moveOut(self, n, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        target = self.getPosition() + n

        if self._inRange(target):
            self._setPosition(target)
        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % target)

    @lock
    def moveTo(self, position, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        if self._inRange(position):
            self._setPosition(position)
        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % int(position))

    @lock
    def getPosition(self, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        return self._position

    def getTime(self, position):
        self.new_time = (-self.coef[0] + position) / self.coef[1]
        print "D = {} mm".format(position)
    
    def getN(self, mm):
        n_mm = 0.5

        self._position
        

    def goTo(self, position):
        time.sleep(1)
        if (position >=  2.2) and (position <= 15):
            self.getTime(position)
            if self.new_time < self.old_time:
                self.mov_time = self.old_time - self.new_time
                print 'time: {}'.format(self.mov_time)
                self.old_time = self.new_time
                self.moveIn()
                time.sleep(self.mov_time)
                self.getStop()
            if self.old_time < self.new_time:
                self.mov_time = self.new_time - self.old_time
                print 'time: {}'.format(self.mov_time)
                self.old_time = self.new_time
                self.moveOut()
                time.sleep(self.mov_time)
                self.getStop()
        else:
            print 'Invalid position'









    def getRange(self, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        return (0, 7000)

    def _setPosition(self, n):
        self.log.info("Changing focuser to %s" % n)
        self._position = n

    def _inRange(self, n):
        min_pos, max_pos = self.getRange()
        return (min_pos <= n <= max_pos)
