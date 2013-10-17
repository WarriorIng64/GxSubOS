import pygame
from window import Window
from launcherbutton import Launcherbutton
import shadow

class WindowManager:
  def __init__(self):
    self.window_list = []
  
  def CreateWindow(self, x, y, width, height, launcher_list, titlebar_text=''):
    # Properly create a new application window that the launcher knows about
    for window in self.window_list:
      window.SetFocus(False)
    self.window_list.append(Window(x, y, width, height, titlebar_text))
    lb = Launcherbutton(self.window_list[-1], len(self.window_list))
    launcher_list.append(lb)
    return self.window_list[-1]
  
  def FindFocusedWindow(self, mouse_x, mouse_y):
    # Set the correct focused window for a MOUSEBUTTONDOWN event
    focused_window_found = False
    for window in reversed(self.window_list):
      if window.WindowClicked(mouse_x, mouse_y) and not focused_window_found:
        window.SetFocus(True)
        focused_window_found = True
      else:
        window.SetFocus(False)
  
  def RemoveClosedWindows(self, mouse_event, mouse_button):
    # Looks for and removes closed windows, and returns true iff any are found
    closed_window_found = False
    for window in self.window_list:
      window.Update(mouse_event, mouse_button)
      if window.window_closed:
        self.window_list.remove(window)
        closed_window_found = True
    return closed_window_found
  
  def MaintainWindowOrder(self):
    # Maintain proper window order
    # Returns true iff the order is changed
    order_changed = False
    for window in self.window_list[:-1]:
      if window.has_focus:
        # This is always last in the window_list so it's drawn on top
        focused_window = window
        self.window_list.remove(window)
        self.window_list.append(focused_window)
        order_changed = True
    return order_changed
  
  def DrawDesktopSurface(self, desktop_surface, wallpaper, wallpaper_rect):
    # Update the surface behind the focused window
    desktop_surface.blit(wallpaper, wallpaper_rect)
    for window in self.window_list[:-1]:
      window.Redraw(desktop_surface)
      if not window.is_maximized:
        shadow.DrawWindowShadow(desktop_surface, window.rect)
      desktop_surface.blit(window.surface, window.rect)
    desktop_surface.convert()
  
  def DrawTopWindow(self, surface):
    # Draws the top window onto the given surface
    if len(self.window_list) < 1:
      return
    window = self.window_list[-1]
    window.Redraw(surface)
    if not window.is_maximized:
      if window.has_focus:
        shadow.DrawFocusedWindowShadow(surface, window.rect)
      else:
        shadow.DrawWindowShadow(surface, window.rect)
    surface.blit(window.surface, window.rect)