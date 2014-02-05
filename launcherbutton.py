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

image_normal = pygame.image.load("graphics/launcher_button.png")
image_active = pygame.image.load("graphics/launcher_button_active.png")
icon_unknown = pygame.image.load("graphics/launcher_icon_unknown.png")

class Launcherbutton:
  image = None
  
  def __init__(self, window, number, launcher):
    self.window = window
    self.number = number
    self.UpdateImage()
    self.rect = self.image.get_rect()
    self.rect.move_ip(0, 48 * number)
    self.new_y = 48 * number
    self.launcher = launcher
  
  def Update(self, mouse_event, mouse_button, new_number):
    self.UpdateWindowStatus(mouse_event, mouse_button)
    self.UpdateImage()
    self.UpdateNumber(new_number)
  
  def UpdateImage(self):
    """Updates the image drawn for this Launcherbutton."""
    if self.window.has_focus:
      self.image = image_active.copy()
    else:
      self.image = image_normal.copy()
    
    if self.window.icon_image != None:
      self.image.blit(self.window.icon_image, [0, 0, 0, 0])
    else:
      self.image.blit(icon_unknown, [0, 0, 0, 0])
  
  def UpdatePosition(self):
    # Returns a Rect covering the area this button was in
    update_rect = self.rect
    move_amount = -(self.rect.y - self.new_y) / 2
    if move_amount != 0:
      self.rect.move_ip(0, move_amount)
    update_rect.union_ip(self.rect)
    return update_rect

  def WindowWasClosed(self):
    # Return whether the associated window was closed
    return self.window == None or self.window.window_closed

  def UpdateNumber(self, new_number):
    self.number = new_number
    self.new_y = 48 * self.number

  def UpdateWindowStatus(self, mouse_event, mouse_button):
    if self.WindowWasClosed():
      return
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if mouse_button == 1 and self.rect.collidepoint(mouse_x, mouse_y):
        self.window.SetFocus(True)
        self.launcher.wm.MaintainWindowOrder()
  
  def UpdateIcon(self):
    """Updates the icon displayed on this Launcherbutton."""
    self.icon_image = self.window.icon_image
    
