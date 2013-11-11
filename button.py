# This file is part of GxSubOS.
# Copyright (C) 2013 Christopher Kyle Horton <christhehorton@gmail.com>

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

class Button(Widget):
  """A Widget subclass which represents a clickable button within a window."""
  def __init__(self, parent_widget=None, parent_window=None, click_code=None):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.click_code = click_code
  
  def SetClickCode(self, click_code):
    """Sets the Python code which will be executed when this Button is
    left-clicked."""
    self.click_code = click_code
  
  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handle a MOUSEDOWN event."""
    if PointInsideWidget(mouse_x, mouse_y):
      if mouse_button == 1:
        exec self.click_code
