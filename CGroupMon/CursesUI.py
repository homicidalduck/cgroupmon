#!/usr/bin/env python
# Copyright 2011 Matt Larson
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import curses
import traceback
import os
from CGroup import CGroup
from Config import Config

class CursesUI():
    "The cgroupmon curses interface"
    def __init__(self, cgroupdir, config = None):
        self.offset = 0
        self.cgrp = CGroup(cgroupdir)
        self.updatebuffer()
        
    def restorescreen(self):
        "Restores the terminal back to normal operation mode"
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def display(self):
        "Updates the screen"
        row = 0
        self.scrn.clear()
        tmpoffset = self.offset
        for line in self.buffer:
            if tmpoffset > 0:
                tmpoffset = tmpoffset - 1
            elif row < curses.LINES:
                self.scrn.addstr(row, 0, line)
                row = row + 1
            else: break
        self.scrn.refresh()

    def updatebuffer(self):
        "Updates the buffer"
        self.buffer = repr(self.cgrp).strip().split('\n')
    
    def run(self):
        """Runs the Curses UI
        'j': scroll down
        'k': scroll up
        'u': update cgroups
        'q': quit"""
        try:
            self.scrn = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.display()
            while True:
                c = self.scrn.getch()
                c = chr(c)
                if c == 'j':
                    if self.offset < (len(self.buffer) - curses.LINES):
                        self.offset = self.offset + 1
                        self.display()
                    elif self.offset > (len(self.buffer) - curses.LINES):
                        self.offset = len(self.buffer) - curses.LINES
                        self.display()
                elif c == 'k':
                    if self.offset > 0:
                        if self.offset > (len(self.buffer) - curses.LINES):
                            self.offset = len(self.buffer) - curses.LINES
                        else:
                            self.offset = self.offset - 1
                            self.display()
                elif c == 'u':
                        if not self.cgrp.update(): break
                        self.updatebuffer()
                        self.display()
                elif c == 'q': break
            self.restorescreen()
        except:
            self.restorescreen()
            traceback.print_exc()
