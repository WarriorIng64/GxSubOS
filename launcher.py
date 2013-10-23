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
from launcherbutton import Launcherbutton
from startbutton import Startbutton
import glass, shadow

transparent = pygame.color.Color(0, 0, 0, 0)

class Launcher:
  launcher_color = glass.glass_color
  launcher_color_opaque = glass.glass_color
  launcher_color.a = glass.glass_alpha
  launcher_width = 48
  
  def __init__(self, screenw, screenh):
    lsw = self.launcher_width + shadow.shadow_width
    self.launcher_list = []
    self.startbutton = Startbutton(self)
    self.rect = pygame.rect.Rect(0, 0, lsw, screenh)
    self.surface = pygame.Surface((lsw, screenh), pygame.SRCALPHA)
    if glass.enable_transparency:
      self.surface.fill(self.launcher_color)
      self.color_surface = pygame.Surface((lsw, screenh), pygame.SRCALPHA)
      self.color_surface.fill(self.launcher_color)
    else:
      self.surface.fill(self.launcher_color_opaque)
      self.color_surface = pygame.Surface((lsw, screenh))
      self.color_surface.fill(self.launcher_color_opaque)
    self.max_exists = False
    self.buttons_edge = self.surface.get_height()
    self.wm = None
    self.update_rect = pygame.Rect(0, 0, 0, 0)
  
  def SetWindowManager(self, windowmanager):
    self.wm = windowmanager
    self.startbutton.SetWindowManager(windowmanager)
  
  def RedrawBackground(self, screen, wm):
    # Redraw the launcher background
    lw = self.launcher_width
    glass.DrawBackground(screen, self.surface, self.rect)
    if glass.enable_transparency:
      self.surface = glass.Blur(self.surface)
    self.surface.blit(self.color_surface, [0, 0, 0, 0])
    mid = lw / 2
    sw = shadow.shadow_width
    if not self.max_exists:
      tri_b = self.buttons_edge + mid
      triangle_points = [(lw, self.buttons_edge), (lw, tri_b), (mid, tri_b)]
      transparent_rect_outer = [lw, 0, sw, self.buttons_edge + mid]
      transparent_rect_inner = [mid, tri_b, mid, self.surface.get_height() - self.buttons_edge]
      pygame.draw.polygon(self.surface, transparent, triangle_points)
      pygame.draw.rect(self.surface, transparent, transparent_rect_inner)
    transparent_rect_outer = [lw, 0, sw, self.surface.get_height()]
    pygame.draw.rect(self.surface, transparent, transparent_rect_outer)
    shadow.DrawLauncherShadow(self)

  def SmoothUpdateLauncherBottom(self, new_buttons_edge):
    # Smoothly advances the bottom of the buttons area to its new location
    lw = self.launcher_width
    self.update_rect.union_ip(pygame.Rect(0, self.buttons_edge - lw, self.surface.get_width(), 2 * lw))
    self.buttons_edge = (self.buttons_edge + new_buttons_edge) / 2
    self.update_rect.union_ip(pygame.Rect(0, self.buttons_edge - lw, self.surface.get_width(), 2 * lw))

  def UpdateWholeLauncher(self, screen, window_manager):
    # Update all components of the launcher except start button
    for button in self.launcher_list:
      self.update_rect.union_ip(button.UpdatePosition())
    self.max_exists = window_manager.MaximizedWindowExists()
    if len(self.launcher_list) > 0 and not self.max_exists:
      self.SmoothUpdateLauncherBottom(self.launcher_list[-1].rect.bottom)
    else:
      self.SmoothUpdateLauncherBottom(self.launcher_width)
    self.RedrawBackground(screen, window_manager)

  def UpdateLauncherbuttonList(self):
    # Update the Launcherbutton list
    # Handy when closing windows from the window manager
    new_button_number = 0
    for button in self.launcher_list:
      new_button_number += 1
      button.UpdateNumber(new_button_number)
      if button.WindowWasClosed():
        self.launcher_list.remove(button)
  
  def HandleMouseButtonDownEvent(self, mouse_event, mouse_button):
    # Handle the MOUSEBUTTONDOWN event, and update launcher buttons
    new_button_number = 0
    for button in self.launcher_list:
      new_button_number += 1
      button.Update(mouse_event, mouse_button, new_button_number)
      if button.WindowWasClosed():
        self.launcher_list.remove(button)
    self.UpdateStartbutton(mouse_event, mouse_button)

  def DrawLauncher(self, screen):
    # Draws the launcher onto the given surface
    # Returns a Rect containing the area drawn to.
    screen.blit(self.surface, (0, 0))
    for button in self.launcher_list:
      screen.blit(button.image, button.rect)
    screen.blit(self.startbutton.image, self.startbutton.rect)
    if self.startbutton.startmenu != None:
      screen.blit(self.startbutton.startmenu.surface, self.startbutton.startmenu.rect)
    return self.update_rect

  def AddLauncherbutton(self, window):
    # Create a new launcherbutton for the given window
    lb = Launcherbutton(window, len(self.launcher_list) + 1, self)
    self.launcher_list.append(lb)

  def UpdateStartbutton(self, mouse_event, mouse_button):
    # Update the startbutton based on the provided event
    self.update_rect.union_ip(self.startbutton.Update(mouse_event, mouse_button))

  def ResetUpdateRect(self):
    self.update_rect = pygame.Rect(0, 0, 0, 0)
