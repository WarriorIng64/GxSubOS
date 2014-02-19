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

class Widget:
  """A base class for implementing various widgets in windows. This is where
  the building blocks for windows' content area GUIs come from."""
  def __init__(self, parent_widget=None, parent_window=None):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.surface = None
    self.requested_width = 0
    self.requested_height = 0
  
  def PointInsideWidget(self, x, y):
    """Returns True if the given point is inside this Widget's rect."""
    x1, x2 = self.rect.left, self.rect.right
    y1, y2 = self.rect.top, self.rect.bottom
    return x1 < x < x2 and y1 < y < y2

  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handle a MOUSEDOWN event."""
    return
  
  def HandleMouseMotionEvent(self, mouse_x, mouse_y):
    """Handle a MOUSEMOTION event."""
    return

  def HandleKeyDownEvent(self, event):
    """Handle a KEYDOWN event."""
    return

  def RedrawParentWindow(self):
    """Force the parent window to redraw and reflect app changes."""
    self.parent_window.top_level_container.Redraw()
    self.parent_window.DrawWindowSurface()
    self.parent_window.wm.UpdateUpdateRect(self.parent_window)
  
  def RequestWidth(self, width):
    """Set a preferred width for this instance."""
    self.requested_width = width
  
  def RequestHeight(self, height):
    """Set a preferred height for this instance."""
    self.requested_height = height

  def GetTopLevelContainer(self):
    """Returns the top-level Container for this Widget."""
    if self.parent_widget == None:
      return self
    else:
      return self.parent_widget.GetTopLevelContainer()

  def SetAsFocusedWidget(self, new_focused_widget):
    """Sets a new focused Widget in this hierarchy."""
    self.GetTopLevelContainer().focused_widget = new_focused_widget

class EmptyWidget(Widget):
  """A class implementing a Widget which is invisible and doesn't do anything.
  These can be used as dynamically-resizing empty spaces in UIs."""
  def Redraw(self):
    """Redraw this EmptyWidget."""
    if self.rect == None:
      return;
    self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
