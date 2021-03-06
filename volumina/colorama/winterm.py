###############################################################################
#   volumina: volume slicing and editing library
#
#       Copyright (C) 2011-2014, the ilastik developers
#                                <team@ilastik.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the Lesser GNU General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# See the files LICENSE.lgpl2 and LICENSE.lgpl3 for full text of the
# GNU Lesser General Public License version 2.1 and 3 respectively.
# This information is also available on the ilastik web site at:
#		   http://ilastik.org/license/
###############################################################################

from . import win32


# from wincon.h
class WinColor(object):
    BLACK   = 0
    BLUE    = 1
    GREEN   = 2
    CYAN    = 3
    RED     = 4
    MAGENTA = 5
    YELLOW  = 6
    GREY    = 7

# from wincon.h
class WinStyle(object):
    NORMAL = 0x00 # dim text, dim background
    BRIGHT = 0x08 # bright text, dim background


class WinTerm(object):

    def __init__(self):
        self._default = win32.GetConsoleScreenBufferInfo(win32.STDOUT).wAttributes
        self.set_attrs(self._default)
        self._default_fore = self._fore
        self._default_back = self._back
        self._default_style = self._style

    def get_attrs(self):
        return self._fore + self._back * 16 + self._style

    def set_attrs(self, value):
        self._fore = value & 7
        self._back = (value >> 4) & 7
        self._style = value & WinStyle.BRIGHT

    def reset_all(self, on_stderr=None):
        self.set_attrs(self._default)
        self.set_console(attrs=self._default)

    def fore(self, fore=None, on_stderr=False):
        if fore is None:
            fore = self._default_fore
        self._fore = fore
        self.set_console(on_stderr=on_stderr)

    def back(self, back=None, on_stderr=False):
        if back is None:
            back = self._default_back
        self._back = back
        self.set_console(on_stderr=on_stderr)

    def style(self, style=None, on_stderr=False):
        if style is None:
            style = self._default_style
        self._style = style
        self.set_console(on_stderr=on_stderr)

    def set_console(self, attrs=None, on_stderr=False):
        if attrs is None:
            attrs = self.get_attrs()
        handle = win32.STDOUT
        if on_stderr:
            handle = win32.STDERR
        win32.SetConsoleTextAttribute(handle, attrs)

    def set_cursor_position(self, position=None, on_stderr=False):
        if position is None:
            #I'm not currently tracking the position, so there is no default.
            #position = self.get_position()
            return
        handle = win32.STDOUT
        if on_stderr:
            handle = win32.STDERR
        win32.SetConsoleCursorPosition(handle, position)

    def erase_data(self, mode=0, on_stderr=False):
        # 0 (or None) should clear from the cursor to the end of the screen.
        # 1 should clear from the cursor to the beginning of the screen.
        # 2 should clear the entire screen. (And maybe move cursor to (1,1)?)
        #
        # At the moment, I only support mode 2. From looking at the API, it 
        #    should be possible to calculate a different number of bytes to clear, 
        #    and to do so relative to the cursor position.
        if mode[0] not in (2,):
            return
        handle = win32.STDOUT
        if on_stderr:
            handle = win32.STDERR
        # here's where we'll home the cursor
        coord_screen = win32.COORD(0,0) 
        csbi = win32.GetConsoleScreenBufferInfo(handle)
        # get the number of character cells in the current buffer
        dw_con_size = csbi.dwSize.X * csbi.dwSize.Y
        # fill the entire screen with blanks
        win32.FillConsoleOutputCharacter(handle, ord(' '), dw_con_size, coord_screen)
        # now set the buffer's attributes accordingly
        win32.FillConsoleOutputAttribute(handle, self.get_attrs(), dw_con_size, coord_screen );
        # put the cursor at (0, 0)
        win32.SetConsoleCursorPosition(handle, (coord_screen.X, coord_screen.Y))
