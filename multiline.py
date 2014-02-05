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
    next_line = ""
    for x in self.text:
      next_line += x
      if self.font.size(next_line)[0] > self.width:
        self.lines.append(next_line)
        next_line = ""
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
    self.width = width
    self.UpdateLines()

  def Render(self):
    '''Return a Surface with the Multiline text properly rendered.'''
    # Trivial cases
    if len(self.lines) == 0:
      return self.font.render(" ", True, glass.accent_color)
    if len(self.lines) == 1:
      return self.font.render(self.lines[0], True, glass.accent_color)

    # For more than one line, render with proper spacing
    line_surfaces = []
    render_height = 0
    space_height = self.font.size(" ")[1]
    for line in self.lines:
      line_surfaces.append(self.font.render(line, True, glass.accent_color))
      render_height += self.font.size(line)[1] + space_height
    render_height -= space_height
    render_surface = pygame.Surface((self.width, render_height), pygame.SRCALPHA)
    # Render each line surface onto the main surface
    current_top = 0;
    for line_surface in line_surfaces:
      render_surface.blit(line_surface, (0, current_top))
      current_top += line_surface.get_height() + space_height
    return render_surface
