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

image_normal = pygame.image.load("graphics/launcher_button.png")
image_active = pygame.image.load("graphics/launcher_button_active.png")

class Launcherbutton:
  image = None
  
  def __init__(self, window, number, launcher):
    self.image = image_normal
    self.rect = self.image.get_rect()
    self.window = window
    self.number = number
    self.rect.move_ip(0, 48 * number)
    self.new_y = 48 * number
    self.launcher = launcher
  
  def Update(self, mouse_event, mouse_button, new_number):
    self.UpdateWindowStatus(mouse_event, mouse_button)
    self.UpdateImage()
    self.UpdateNumber(new_number)
  
  def UpdateImage(self):
    if self.window.has_focus:
      self.image = image_active
    else:
      self.image = image_normal
  
  def UpdatePosition(self):
    move_amount = -(self.rect.y - self.new_y) / 2
    if move_amount != 0:
      self.rect.move_ip(0, move_amount)

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
    
