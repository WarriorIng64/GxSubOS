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
from widget import Widget
import window, glass

class Container(Widget):
  """A special type of Widget which holds other widgets."""
  def __init__(self, parent_widget=None, parent_window=None, child_widgets=[]):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.child_widgets = child_widgets
    self.rect = None
    self.UpdateRect()
    self.surface = None
    self.requested_width = 0
    self.requested_height = 0
    self.focused_widget = None
  
  def UpdateRect(self):
    """Updates this Container's rect."""
    if self.parent_window != None:
      if self.parent_widget != None:
        self.rect = self.parent_widget.rect.copy()
      else:
        self.rect = self.parent_window.content_area_rect.move(0, -window.titlebar_height)
    else:
      self.rect = None
    self.UpdateChildWidgetSizes()
  
  def AddWidget(self, widget):
    """Adds a new Widget to the child widget list."""
    if widget is self:
      print("Warning: Attempt to add a Container to its own widget list.")
      return
    if widget is self.parent_widget:
      print("Warning: Attempt to add a parent widget to a widget list.")
      return
    if isinstance(widget, Widget):
      # Successfully add the Widget
      self.child_widgets.append(widget)
      self.UpdateChildWidgetSizes()
      self.Redraw()
    else:
      print("Warning: Attempt to add non-Widget to container widget list.")
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
        print("Warning: self in widgets list. This has been removed.")
  
  def Redraw(self):
    """Redraw this Container. This is done by telling all child widgets to
    redraw themselves."""
    self.UpdateRect()
    if self.rect == None:
      return;
    self.surface = glass.MakeTransparentSurface(self.rect.width, self.rect.height)
    for child in self.child_widgets:
      self.surface.blit(child.surface, child.rect.topleft)

  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handle a MOUSEDOWN event. In the case of a Container, just pass it on to
    the child widgets."""
    for child in self.child_widgets:
      child.HandleMouseButtonDownEvent(mouse_x - self.rect.x, mouse_y - self.rect.y, mouse_button)
    if self.PointInsideWidget(mouse_x, mouse_y):
      self.Redraw()
  
  def HandleMouseMotionEvent(self, mouse_x, mouse_y):
    """Handle a MOUSEMOTION event. In the case of a Container, just pass it on to
    the child widgets."""
    for child in self.child_widgets:
      child.HandleMouseMotionEvent(mouse_x - self.rect.x, mouse_y - self.rect.y)
    if self.PointInsideWidget(mouse_x, mouse_y):
      self.Redraw()

  def HandleKeyDownEvent(self, event):
    """Handle a KEYDOWN event. In the case of a Container, just pass it on to
    the currently focused child widget."""
    if self.parent_widget == None:
      if self.focused_widget != None:
        self.focused_widget.HandleKeyDownEvent(event)

  def HasDescendantWidget(self, descendant):
    """Checks whether this Container or any of its child Containers contains the
    descendant Widget passed in."""
    for child in self.child_widgets:
      if isinstance(child, Container):
        if child.HasDescendantWidget(descendant):
          return True
      if child is descendant:
          return True
    return False

  def SetAsFocusedWidget(self, new_focused_widget):
    """Sets a new focused Widget in this hierarchy."""
    if self.parent_widget == None:
      self.focused_widget = new_focused_widget
    else:
      self.GetTopLevelContainer().focused_widget = (new_focused_widget)

class HBox(Container):
  def UpdateChildWidgetSizes(self):
    """Updates the sizes and positions of the child widgets so they are
    arranged from left to right, filling the vertical space of the HBox.
    This also respects the requested widths of child widgets if they are set."""
    if len(self.child_widgets) == 0:
      return
    total_requested_width = 0
    total_widgets_requesting = 0
    for child in self.child_widgets:
      # Only a requested_width of 0 means a requested width is not set
      if child.requested_width != 0:
        total_requested_width += child.requested_width
        total_widgets_requesting += 1
    
    ch = self.rect.height
    if total_widgets_requesting >= len(self.child_widgets):
      # All widgets will set their own width
      current_left = 0
      for child in self.child_widgets:
        rect = pygame.Rect(current_left, 0, child.requested_width, ch)
        child.rect = rect.copy()
        current_left += child.requested_width
    elif total_widgets_requesting == 0:
      # No widgets set their own width
      cw = self.rect.width / len(self.child_widgets)
      for i in range(len(self.child_widgets)):
        rect = pygame.Rect(i * cw, 0, cw, ch)
        self.child_widgets[i].rect = rect.copy()
    else:
      # Some widgets set their own width; adjust the rest accordingly
      cw = (self.rect.width - total_requested_width) /  (len(self.child_widgets) - total_widgets_requesting)
      current_left = 0
      for child in self.child_widgets:
        current_width = child.requested_width if child.requested_width != 0 else cw
        rect = pygame.Rect(current_left, 0, current_width, ch)
        child.rect = rect.copy()
        current_left += current_width
    self.RedrawChildWidgets()
  
  def UpdateRect(self):
    """Updates this HBox's rect."""
    self.UpdateChildWidgetSizes()
    return

class VBox(Container):
  def UpdateChildWidgetSizes(self):
    """Updates the sizes and positions of the child widgets so they are
    arranged from top to bottom, filling the horizontal space of the VBox.
    This also respects the requested heights of child widgets if they are set."""
    if len(self.child_widgets) == 0:
      return
    total_requested_height = 0
    total_widgets_requesting = 0
    for child in self.child_widgets:
      # Only a requested_height of 0 means a requested height is not set
      if child.requested_height != 0:
        total_requested_height += child.requested_height
        total_widgets_requesting += 1
    
    cw = self.rect.width
    if total_widgets_requesting >= len(self.child_widgets):
      # All widgets will set their own height
      current_top = 0
      for child in self.child_widgets:
        rect = pygame.Rect(0, current_top, cw, child.requested_height)
        child.rect = rect.copy()
        current_top += child.requested_height
    elif total_widgets_requesting == 0:
      # No widgets set their own height
      ch = self.rect.height / len(self.child_widgets)
      for i in range(len(self.child_widgets)):
        rect = pygame.Rect(0, i * ch, cw, ch)
        self.child_widgets[i].rect = rect.copy()
    else:
      # Some widgets set their own height; adjust the rest accordingly
      ch = (self.rect.height - total_requested_height) /  (len(self.child_widgets) - total_widgets_requesting)
      current_top = 0
      for child in self.child_widgets:
        current_height = child.requested_height if child.requested_height != 0 else ch
        rect = pygame.Rect(0, current_top, cw, current_height)
        child.rect = rect.copy()
        current_top += current_height
    self.RedrawChildWidgets()
  
  def UpdateRect(self):
    """Updates this HBox's rect."""
    self.UpdateChildWidgetSizes()
    return
