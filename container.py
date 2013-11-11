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

import pygame
import widget

class Container(widget.Widget):
  """A special type of Widget which holds other widgets."""
  def __init__(self, parent_widget=None, parent_window=None, child_widgets=[]):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.child_widgets = child_widgets
    if parent_window != None:
      if parent_widget != None:
        self.rect = parent_widget.rect.copy()
      else:
        self.rect = parent_window.content_area_rect.copy()
    else:
      self.rect = None
  
  def AddWidget(self, widget):
    """Adds a new Widget to the child widget list."""
    self.child_widgets.append(widget)
  
  def IsTopLevel(self):
    """Returns true iff this Container contains all other Widgets in this
    window. Every Window should contain a top-level Container widget which
    holds all the other Widgets, including other Containers."""
    return self.parent_widget is None
  
  def UpdateChildWidgetSizes(self):
    """Updates the sizes of the child widgets."""
    for child in self.child_widgets:
      child.rect = self.rect.copy()

  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handle a MOUSEDOWN event. In the case of a Container, just pass it on to
    the child widgets."""
    for child in self.child_widgets:
      child.HandleMouseDownEvent(mouse_x, mouse_y, mouse_button)
