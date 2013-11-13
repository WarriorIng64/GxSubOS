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
from widget import Widget
import window

class Container(Widget):
  """A special type of Widget which holds other widgets."""
  def __init__(self, parent_widget=None, parent_window=None, child_widgets=[]):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.child_widgets = child_widgets
    self.rect = None
    self.UpdateRect()
    self.surface = None
  
  def UpdateRect(self):
    """Updates this Container's rect."""
    if self.parent_window != None:
      if self.parent_widget != None:
        self.rect = self.parent_widget.rect.copy()
      else:
        self.rect = self.parent_window.content_area_rect.move(0, -window.titlebar_height / 2)
    else:
      self.rect = None
    self.UpdateChildWidgetSizes()
  
  def AddWidget(self, widget):
    """Adds a new Widget to the child widget list."""
    if widget is self:
      print "Warning: Attempt to add a Container to its own widget list."
      return
    if widget is self.parent_widget:
      print "Warning: Attempt to add a parent widget to a widget list."
      return
    if isinstance(widget, Widget):
      # Successfully add the Widget
      self.child_widgets.append(widget)
      self.UpdateChildWidgetSizes()
      self.Redraw()
    else:
      print "Warning: Attempt to add non-Widget to container widget list."
      return
  
  def IsTopLevel(self):
    """Returns true iff this Container contains all other Widgets in this
    window. Every Window should contain a top-level Container widget which
    holds all the other Widgets, including other Containers."""
    return self.parent_widget is None
  
  def UpdateChildWidgetSizes(self):
    """Updates the sizes of the child widgets."""
    for child in self.child_widgets:
      child.rect = pygame.Rect((0, 0), (self.rect.size))
    self.RedrawChildWidgets()
  
  def RedrawChildWidgets(self):
    """Tells all child widgets to redraw themselves, such as after a resizing."""
    for child in self.child_widgets:
      if child is not self:
        child.Redraw()
      else:
        self.child_widgets.remove(child)
        print "Warning: self in widgets list. This has been removed."
  
  def Redraw(self):
    """Redraw this Container. This is done by telling all child widgets to
    redraw themselves."""
    self.UpdateRect()
    if self.rect == None:
      return;
    self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
    for child in self.child_widgets:
      self.surface.blit(child.surface, child.rect.topleft)

  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handle a MOUSEDOWN event. In the case of a Container, just pass it on to
    the child widgets."""
    for child in self.child_widgets:
      child.HandleMouseButtonDownEvent(mouse_x - self.rect.x, mouse_y - self.rect.y, mouse_button)

class HBox(Container):
  def UpdateChildWidgetSizes(self):
    """Updates the sizes and positions of the child widgets so they are
    arranged from left to right, filling the vertical space of the HBox."""
    if len(self.child_widgets) == 0:
      return
    cw = self.rect.width / len(self.child_widgets)
    ch = self.rect.height
    for i in range(len(self.child_widgets)):
      rect = pygame.Rect(i * cw, 0, cw, ch)
      self.child_widgets[i].rect = rect.copy()
    self.RedrawChildWidgets()

class VBox(Container):
  def UpdateChildWidgetSizes(self):
    """Updates the sizes and positions of the child widgets so they are
    arranged from top to bottom, filling the horizontal space of the VBox."""
    if len(self.child_widgets) == 0:
      return
    cw = self.rect.width
    ch = self.rect.height / len(self.child_widgets)
    for i in range(len(self.child_widgets)):
      rect = pygame.Rect(0, i * ch, cw, ch)
      self.child_widgets[i].rect = rect.copy()
    self.RedrawChildWidgets()
