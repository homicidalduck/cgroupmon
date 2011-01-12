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

def restorescreen():
    "Restores the terminal back to normal operation mode"
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def display(scrn, cgrp, offset):
    "Updates the screen"
    row = 0
    scrn.clear()
    for line in repr(cgrp).split('\n'):
        if offset > 0:
            offset = offset - 1
        elif row < curses.LINES:
            scrn.addstr(row, 0, line)
            row = row + 1
        else: break
    scrn.refresh()
    
def run(cdir):
    "Runs the Curses UI"
    try:
        scrn = curses.initscr()
        curses.noecho()
        curses.cbreak()
        cgrp = CGroup(cdir)
        offset = 0
        display(scrn, cgrp, offset)
        while True:
            c = scrn.getch()
            c = chr(c)
            if c == 'j':
                if offset < (len(repr(cgrp).split('\n')) - curses.LINES):
                    offset = offset + 1
                    display(scrn, cgrp, offset)
            elif c == 'k':
                if offset > 0:
                    offset = offset - 1
                    display(scrn, cgrp, offset)
            elif c == 'u':
                if not cgrp.update(): break
                display(scrn, cgrp, offset)
            elif c == 'q': break
        restorescreen()
    except:
        restorescreen()
        traceback.print_exc()
