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

button_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 16)

class Button(Widget):
  """A Widget subclass which represents a clickable button within a window."""
  def __init__(self, parent_widget=None, parent_window=None, button_text=None, click_code=None):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.surface = None
    self.button_text = ""
    self.text_surface = None
    self.SetButtonText(button_text)
    self.click_code = click_code
    self.hovered = False
    self.requested_width = 0
    self.requested_height = 0
  
  def SetClickCode(self, click_code):
    """Sets the Python code which will be executed when this Button is
    left-clicked."""
    self.click_code = click_code
  
  def SetButtonText(self, button_text):
    """Sets the text displayed on the button."""
    self.button_text = button_text
    if self.button_text != "":
      self.text_surface = button_font.render(self.button_text, True, glass.accent_color)
  
  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handle a MOUSEDOWN event."""
    if self.PointInsideWidget(mouse_x, mouse_y) and mouse_button == 1:
      self.SetAsFocusedWidget(self)
      exec self.click_code
  
  def HandleMouseMotionEvent(self, mouse_x, mouse_y):
    """Handle a MOUSEMOTION event."""
    is_hovered = self.PointInsideWidget(mouse_x, mouse_y)
    if self.hovered != is_hovered:
      self.hovered = is_hovered
      self.Redraw()
      self.RedrawParentWindow()
  
  def Redraw(self):
    """Redraw this Button."""
    padding = 2
    button_color = glass.accent_color
    button_color.a = 100
    if self.rect == None:
      return;
    self.surface = glass.MakeTransparentSurface(self.rect.width, self.rect.height)
    border_rect = self.surface.get_rect().inflate(-padding * 2, -padding * 2).move(padding / 2, padding / 2)
    if self.hovered:
      pygame.draw.rect(self.surface, button_color, border_rect)
    else:
      pygame.draw.rect(self.surface, button_color, border_rect, 2)
    if self.text_surface is not None:
      text_left_align = self.surface.get_width() / 2 - self.text_surface.get_width() / 2
      text_top_align = self.surface.get_height() / 2 - self.text_surface.get_height() / 2
      self.surface.blit(self.text_surface, (text_left_align, text_top_align))
    
