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
  def __init__(self, text, font, area_rect, long_lines=False):
    '''Initialize with text of the given font within the given width.'''
    self.text = text
    self.font = font
    self.area_rect = area_rect
    self.long_lines = long_lines
    self.lines = []
    self.scroll_amount = 0
    self.UpdateLines()

  def UpdateLines(self):
    '''Split the current text up according to size requirements.'''
    self.lines = self.text.splitlines()
    # TODO: Honor self.long_lines
  
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
    lines_height = len(self.lines) * self.font.get_linesize()
    if lines_height > self.area_rect.height:
      self.scroll_amount -= pixels
      if lines_height + self.scroll_amount < self.area_rect.height:
        self.scroll_amount = self.area_rect.height - lines_height

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
      if current_top > -self.font.get_linesize() and current_top < self.area_rect.height:
        render_surface.blit(line_surface, (0, current_top))
      current_top += self.font.get_linesize()
    return render_surface
