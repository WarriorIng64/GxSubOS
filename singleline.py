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

import copy
import pygame
import glass, drawingshapes

class Singleline():

  '''A class for displaying a single line of text.'''

  def __init__(self, text, font, width):
    '''Initialize with text of the given font within the given width.'''
    self.text = text
    self.font = font
    self.width = width
    self.scroll_amount = 0
  
  def GetText(self):
    '''Return the current text as a single string.'''
    return self.text
  
  def SetText(self, text):
    '''Change the current text and update.'''
    self.text = text
  
  def SetFont(self, font):
    '''Change the current font and update.'''
    self.font = font
  
  def SetWidth(self, width):
    '''Change the current width and update.'''
    self.area_rect.width = width
  
  def Render(self):
    '''Return a Surface with the Singleline text properly rendered.'''
    return self.font.render(self.text, True, glass.accent_color)
