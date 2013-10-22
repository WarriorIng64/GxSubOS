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
from window import Window
from launcherbutton import Launcherbutton
import shadow

class WindowManager:
  def __init__(self, launcher):
    self.window_list = []
    self.launcher = launcher
    self.redraw_needed = True
    self.update_rect = pygame.Rect((0, 0), (pygame.display.Info().current_w, pygame.display.Info().current_h))
  
  def CreateWindow(self, x, y, width, height, titlebar_text=''):
    # Properly create a new application window that the launcher knows about
    for window in self.window_list:
      window.SetFocus(False)
    new_window = Window(x, y, width, height, titlebar_text)
    self.window_list.append(new_window)
    self.launcher.AddLauncherbutton(new_window)
    self.RequireRedraw()
    return new_window
  
  def FindFocusedWindow(self, mouse_x, mouse_y):
    # Set the correct focused window for a MOUSEBUTTONDOWN event
    for window in reversed(self.window_list):
      if window.WindowClicked(mouse_x, mouse_y):
        window.SetFocus(True)
        break
      else:
        window.SetFocus(False)
  
  def RemoveClosedWindows(self):
    # Looks for and removes windows closed
    # Returns true iff any closed windows are found
    for window in reversed(self.window_list):
      if window.window_closed:
        self.window_list.remove(window)
        self.RequireRedraw()
        self.launcher.UpdateLauncherbuttonList()
        return True
    return False
  
  def MaintainWindowOrder(self):
    # Maintain proper window order
    # Returns true iff the order is changed
    for window in self.window_list[:-1]:
      if window.has_focus:
        # This is always last in the window_list so it's drawn on top
        focused_window = window
        self.window_list.remove(window)
        self.window_list.append(focused_window)
        self.RequireRedraw()
        for other_window in self.window_list[:-1]:
          other_window.SetFocus(False)
        return True
    return False
  
  def UpdateWindows(self, mouse_event, mouse_button):
    # General function for updating the state of all windows and the list
    # Returns true iff a redraw of all windows is required
    redraw_needed = self.RemoveClosedWindows(mouse_event, mouse_button)
    redraw_needed = redraw_needed or self.MaintainWindowOrder()
    return redraw_needed
  
  def DrawDesktopSurface(self, desktop_surface, wallpaper):
    # Update the surface behind the focused window
    if self.RedrawNeeded():
      desktop_surface.blit(wallpaper.image, wallpaper.rect)
      for window in self.window_list[:-1]:
        window.Redraw(desktop_surface)
        if not window.is_maximized:
          shadow.DrawWindowShadow(desktop_surface, window.rect)
        desktop_surface.blit(window.surface, window.rect)
      desktop_surface.convert()
      # The redraw was performed
      self.redraw_needed = False
  
  def DrawTopWindow(self, surface, blurred_surface=None):
    # Draws the top window onto the given surface
    # A blurred version of the surface behind the window can be passed in to save time
    # Returns a Rect containing the updated area
    if len(self.window_list) < 1:
      return
    window = self.window_list[-1]
    window.Redraw(surface, blurred_surface)
    if not window.is_maximized:
      if window.has_focus:
        shadow.DrawFocusedWindowShadow(surface, window.rect)
      else:
        shadow.DrawWindowShadow(surface, window.rect)
    surface.blit(window.surface, window.rect)
    return self.update_rect
  
  def MaximizedWindowExists(self):
    # Return true iff there is a maximized window
    for window in reversed(self.window_list):
      if window.is_maximized:
        return True
    return False
  
  def GetEntireWindowArea(self, window):
    # Returns a Rect representing the entire drawable area the window covers,
    # including the shadow.
    size_increase = shadow.shadow_width * 2
    return window.rect.inflate(size_increase, size_increase)
  
  def UpdateUpdateRect(self, window):
    # Updates update_rect based on the current rect for the given window
    self.update_rect.union_ip(self.GetEntireWindowArea(window))
  
  def UpdateRectFunction(self, window, f):
    # Usage: UpdateRectFunction(window, lambda: functioncall(args))
    # Use when performing a window management operation where the update_rect
    # itself needs to be updated.
    self.UpdateUpdateRect(window)
    f()
    self.UpdateUpdateRect(window)
  
  def DragWindows(self, mouse_x, mouse_y):
    # Drags windows which are in the state of being dragged
    if len(self.window_list) < 1:
      return
    window = self.window_list[-1]
    if window.has_focus and window.being_dragged:
      self.UpdateRectFunction(window, lambda: window.Drag(mouse_x, mouse_y))
  
  def ResizeWindows(self, mouse_x, mouse_y):
    # Resizes windows which are in the state of being resized
    if len(self.window_list) < 1:
      return
    window = self.window_list[-1]
    if window.has_focus and window.being_resized:
      self.UpdateRectFunction(window, lambda: window.MouseResize(mouse_x, mouse_y))
  
  def StopAllWindowDragging(self):
    # Stops all window dragging, such as when the user releases the mouse button
    for window in self.window_list:
      window.being_dragged = False
  
  def StopAllWindowResizing(self):
    # Stops all window resizing, such as when the user releases the mouse button
    for window in self.window_list:
      window.being_resized = False
  
  def HandleMouseMotionEvent(self, mouse_x, mouse_y):
    # General function for handling mouse motion events for windows
    self.DragWindows(mouse_x, mouse_y)
    self.ResizeWindows(mouse_x, mouse_y)
  
  def HandleMouseButtonUpEvent(self, mouse_x, mouse_y, mouse_button):
    # General function for handling mouse button release events for windows
    if mouse_button == 1:
      if len(self.window_list) > 0:
        window = self.window_list[-1]
        if window.being_dragged:
          if mouse_y <= 5 and not window.is_maximized:
            self.UpdateRectFunction(window, lambda: window.Maximize())
          else:
            self.UpdateRectFunction(window, lambda: window.Unmaximize())
      self.StopAllWindowDragging()
      self.StopAllWindowResizing()
  
  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    # General function for handling mouse button press events for windows
    if mouse_button == 1:
      for window in reversed(self.window_list):
        if window.WindowClicked(mouse_x, mouse_y):
          if window.CloseButtonClicked(mouse_x, mouse_y):
            window.window_closed = True
            self.RemoveClosedWindows()
          elif window.ResizeButtonClicked(mouse_x, mouse_y):
            window.StartResizing(mouse_x, mouse_y)
          elif window.TitlebarClicked(mouse_x, mouse_y):
            window.StartDragging(mouse_x, mouse_y)
          break
      self.FindFocusedWindow(mouse_x, mouse_y)
      self.MaintainWindowOrder()
  
  def RedrawNeeded(self):
    # Returns true iff a redraw of the nonfocused windows is needed
    return self.redraw_needed
  
  def RequireRedraw(self):
    # Updates the current state to require a redraw
    self.redraw_needed = True
  
  def ResetUpdateRect(self):
    # Resets the update_rect
    self.update_rect = pygame.Rect(0, 0, 0, 0)
