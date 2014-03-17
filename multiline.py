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
import glass

class Multiline:
  def __init__(self, text, font, area_rect, split_by_words=True):
    '''Initialize with text of the given font within the given width.'''
    self.text = text
    self.font = font
    self.area_rect = area_rect
    self.lines = []
    self.split_by_words = split_by_words
    self.scroll_amount = 0
    self.UpdateLines()

  def UpdateLines(self):
    '''Split the current text up according to size requirements.'''
    self.lines = []
    if not self.split_by_words:
      # Split by characters instead
      next_line = ""
      for x in self.text:
        if self.font.size(next_line + x)[0] > self.area_rect.width or x == '\n':
          self.lines.append(next_line)
          next_line = ""
        if not (next_line == "" and x == ' '):
          next_line += x
      if next_line != "":
        self.lines.append(next_line)
    else:
      # Split by words
      next_line = ""
      next_word = ""
      for x in self.text:
        if self.font.size(next_line + " " + next_word)[0] > self.area_rect.width:
          self.lines.append(next_line)
          next_line = ""
        if x == '\n':
          if next_line != "":
            next_line += " "
          next_line += next_word
          next_word = ""
          self.lines.append(next_line)
          next_line = ""
        elif x == ' ':
          if next_line != "":
            next_line += " "
          next_line += next_word
          next_word = ""
        else:
          next_word += x
      if next_word != "":
        if next_line != "":
          next_line += " "
        next_line += next_word
      if next_line != "":
        self.lines.append(next_line)
  
  def GetLines(self):
    '''Return the current list of lines.'''
    return self.lines

  def GetText(self):
    '''Return the current text as a single string.'''
    return self.text

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
    self.area_rect.width = width
    self.UpdateLines()

  def SetHeight(self, height):
    '''Change the current height and update.'''
    self.area_rect.height = height
    self.UpdateLines()

  def SetAreaRect(self, area_rect):
    '''Change the current area Rect and update.'''
    self.area_rect = area_rect
    self.UpdateLines()

  def ScrollUp(self, pixels):
    '''Scroll the text up by the given number of pixels.'''
    self.scroll_amount += pixels
    if self.scroll_amount > 0:
      self.scroll_amount = 0

  def ScrollDown(self, pixels):
    '''Scroll the text down by the given number of pixels.'''
    self.scroll_amount -= pixels
    # TODO: Keep the bottom of the text from scrolling above the bottom of the
    # Multiline surface area.

  def Render(self):
    '''Return a Surface with the Multiline text properly rendered.'''
    # Trivial cases
    if len(self.lines) == 0:
      return self.font.render(" ", True, glass.accent_color)
    if len(self.lines) == 1:
      return self.font.render(self.lines[0], True, glass.accent_color)

    # For more than one line, render with proper spacing
    line_surfaces = []
    render_height = len(self.lines) * self.font.get_linesize()
    for line in self.lines:
      line_surfaces.append(self.font.render(line, True, glass.accent_color))
    render_surface = glass.MakeTransparentSurface(self.area_rect.width, render_height)
    # Render each line surface onto the main surface
    current_top = self.scroll_amount;
    for line_surface in line_surfaces:
      render_surface.blit(line_surface, (0, current_top))
      current_top += self.font.get_linesize()
    return render_surface
