# This file is part of GxSubOS.
# Copyright (C) 2014 Christopher Kyle Horton <christhehorton@gmail.com>

# GxSubOS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GxSubOS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GxSubOS. If not, see <http://www.gnu.org/licenses/>.

import pygame

class Multiline:
  def __init__(self, text, font, width):
    '''Initialize with text of the given font within the given width.'''
    self.text = text
    self.font = font
    self.width = width
    self.lines = []
    self.UpdateLines()

  def UpdateLines(self):
    '''Split the current text up according to size requirements.'''
    self.lines = []
    text_copy = self.text.copy()
    
    next_line = ""
    for x in self.text:
      if self.font.size(next_line + x)[0] > self.width:
        self.lines.append(next_line + x)
        next_line = ""
  
  def GetLines(self):
    '''Return the current list of lines.'''
    return self.lines

  def SetText(self, text):
    '''Change the current text and update.'''
    self.text = text
    self.UpdateLines()

  def SetFont(self, font):
    '''Change the current font and update.'''
    self.font = font
    self.UpdateLines()

  def SetWidth(self, width):
    '''Change the current width and update.'''
    self.width = width
    self.UpdateLines()
