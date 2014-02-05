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
from multiline import Multiline
import glass

textbox_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 16)

class TextBox(Widget):
  """A Widget subclass which represents a TextBox within a window."""
  def __init__(self, parent_widget=None, parent_window=None, initial_text=None):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.surface = None
    self.text = ""
    self.multiline = Multiline(self.text, textbox_font, 1000)
    self.text_surface = None
    self.SetText(initial_text)
    self.hovered = False
  
  def SetText(self, text):
    """Sets the text displayed in the textbox."""
    self.text = text
    self.multiline.SetText(text)
  
  def HandleMouseMotionEvent(self, mouse_x, mouse_y):
    """Handle a MOUSEMOTION event."""
    is_hovered = self.PointInsideWidget(mouse_x, mouse_y)
    if self.hovered != is_hovered:
      self.hovered = is_hovered
      self.Redraw()
      self.RedrawParentWindow()
  
  def Redraw(self):
    """Redraw this TextBox."""
    padding = 4
    textbox_color = glass.accent_color
    textbox_color.a = 50
    if self.rect == None:
      return;
    self.multiline.SetWidth(self.rect.width - padding * 2)
    self.text_surface = self.multiline.Render()
    self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    border_rect = self.surface.get_rect().inflate(-padding, -padding).move(padding / 2, padding / 2)
    if self.hovered:
      pygame.draw.rect(self.surface, textbox_color, border_rect)
    else:
      pygame.draw.rect(self.surface, textbox_color, border_rect, 2)
    if self.text_surface is not None:
      text_left_align = padding
      text_top_align = padding
      self.surface.blit(self.text_surface, (text_left_align, text_top_align))
    
