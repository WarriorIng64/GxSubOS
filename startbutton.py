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
from menu import Menu

class Startbutton:
  image = pygame.image.load("graphics/start.png")
  
  def __init__(self, launcher):
    self.rect = self.image.get_rect()
    self.startmenu = None
    self.launcher = launcher
    self.wm = None

  def SetWindowManager(self, wm):
    self.wm = wm
  
  def HandleMouseButtonDownEvent(self, mouse_event, mouse_button):
    update_rect = self.rect
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if self.startmenu != None:
        # Execute a menu option (if clicked)
        self.startmenu.HandleMouseButtonDownEvent(mouse_event, mouse_button)
        update_rect = update_rect.union(self.startmenu.rect)
      if mouse_button == 1 and self.rect.collidepoint(mouse_x, mouse_y):
        if self.startmenu is None:
          # Open the start menu
          self.startmenu = Menu(self.launcher.wm, self.launcher.surface.get_width(), 0)
          self.startmenu.AddMenuOption("Create new window", "self.creator.CreateWindow(48, 0, 300, 200, 'Untitled')")
          self.startmenu.AddMenuOption("Change wallpaper...", "self.creator.InitializeWallpaperSwitcher()")
          self.startmenu.AddMenuOption("Shutdown GxSubOS", "pygame.quit();sys.exit()")
          update_rect = update_rect.union(self.startmenu.rect)
        else:
          # Close the menu
          update_rect = update_rect.union(self.startmenu.rect)
          del self.startmenu
          self.startmenu = None
      elif self.startmenu != None:
        # Close the menu
        update_rect = update_rect.union(self.startmenu.rect)
        del self.startmenu
        self.startmenu = None
    return update_rect
  
  def HandleMouseMotionEvent(self, mouse_event):
    update_rect = pygame.Rect(0, 0, 0, 0)
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if self.startmenu != None:
        update_rect = self.startmenu.HandleMouseMotionEvent(mouse_event)
    return update_rect
