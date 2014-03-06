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

import sys, pygame
from widget import Widget
import glass

label_font = pygame.font.Font("fonts/Roboto/Roboto-Light.ttf", 16)
LEFT, CENTER, RIGHT = range(3)

class Label(Widget):
  """A Widget subclass which represents a label within a window."""
  def __init__(self, parent_widget=None, parent_window=None, label_text=None, halign=CENTER):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.surface = None
    self.button_text = ""
    self.text_surface = None
    self.SetLabelText(label_text)
    self.hovered = False
    self.requested_width = 0
    self.requested_height = 0
    self.halign = halign
  
  def SetLabelText(self, label_text):
    """Sets the text displayed on the label."""
    self.label_text = label_text
    render_text = self.label_text if self.label_text != "" else " "
    self.text_surface = label_font.render(render_text, True, glass.accent_color)
    self.RedrawParentWindow()

  def GetLabelText(self):
    """Gets the text displayed on the label."""
    return self.label_text

  def SetHorizontalAlignment(self, halign):
    """Sets the horizontal text alignment to whatever is passed in.
    Acceptable values should be one of the following:
      label.LEFT
      label.CENTER
      label.RIGHT
    """
    self.halign = halign
  
  def Redraw(self):
    """Redraw this Label."""
    padding = 4
    if self.rect == None:
      return;
    self.surface = glass.MakeTransparentSurface(self.rect.width, self.rect.height)
    if self.text_surface is not None:
      if self.halign == LEFT:
        text_left_align = 0
      elif self.halign == RIGHT:
        text_left_align = self.surface.get_width() - self.text_surface.get_width()
      else:
        # Default to centered text
        text_left_align = self.surface.get_width() / 2 - self.text_surface.get_width() / 2
      text_top_align = self.surface.get_height() / 2 - self.text_surface.get_height() / 2
      self.surface.blit(self.text_surface, (text_left_align, text_top_align))
    
