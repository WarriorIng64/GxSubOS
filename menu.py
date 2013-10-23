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
import math
import drawingshapes, glass

pygame.font.init()

menu_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 16)
roundness = 10
padding = 10

class Menu:
  def __init__(self, creator, x=0, y=0):
    # creator is the object instance this menu references for executing commands
    self.creator = creator
    self.options_list = []
    self.rect = pygame.Rect(x, y, 0, 0)
    self.surface = self.surface = pygame.Surface((0, 0), pygame.SRCALPHA)
    self.menu_color = glass.glass_color
    self.menu_color.a = glass.glass_alpha
    self.menu_closed = False
    self.option_highlighted = -1

  def AddMenuOption(self, option_text, option_code):
    # Adds the given menu option to this menu's options list.
    new_option = (option_text, option_code)
    self.options_list.append(new_option)
    self.UpdateSurface()

  def UpdateSurface(self):
    # Update this menu's surface based on its current state.
    max_menu_width = 1
    max_entry_height = 2
    for option in self.options_list:
      max_menu_width = max(max_menu_width, menu_font.size(option[0])[0])
      max_entry_height = max(max_entry_height, menu_font.size(option[0])[1])
    menu_width = max_menu_width + 2 * padding
    menu_height = max_entry_height * len(self.options_list) + 2 * padding
    self.surface = self.surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
    sep_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
    self.rect = pygame.Rect(self.rect.x, self.rect.y, menu_width, menu_height)
    #drawingshapes.DrawRoundRect(self.surface, self.menu_color, pygame.Rect(0, 0, menu_width, menu_height), roundness)
    pygame.draw.rect(self.surface, self.menu_color, pygame.Rect(0, 0, menu_width, menu_height))
    i = 0
    for option in self.options_list:
      option_surface = menu_font.render(option[0], True, (0, 255, 255))
      self.surface.blit(option_surface, (padding, i * max_entry_height + padding))
      if self.option_highlighted is i:
        pygame.draw.rect(sep_surface, pygame.Color(0, 255, 255, 100), pygame.Rect(0, i * max_entry_height + padding, self.surface.get_width(), max_entry_height))
      drawingshapes.DrawHSeparator(sep_surface, self.rect.width, (i + 1) * max_entry_height + padding)
      i += 1
    self.surface.blit(sep_surface, (0, 0))
  
  def PointInsideMenu(self, x, y):
    # Determines if this point is inside the menu.
    inside_x = self.rect.x < x < self.rect.x + self.rect.width
    inside_y = self.rect.y < y < self.rect.y + self.rect.height
    return inside_x and inside_y
  
  def GetIndexOfOptionClicked(self, y):
    # Determines which menu option was clicked, assuming the click is within
    # the menu boundaries.
    option_height = (self.surface.get_height() - 2 * padding) / len(self.options_list)
    raw_value = (y - self.rect.y - padding) / option_height
    int_value = int(math.floor(raw_value))
    if 0 > int_value >= len(self.options_list):
      return -1
    else:
      return int(math.floor(raw_value))
  
  def HandleMouseButtonDownEvent(self, mouse_event, mouse_button):
    # Handle mouse clicks with respect to the menu.
    mouse_x, mouse_y = mouse_event.pos
    if mouse_button is 1 and self.PointInsideMenu(mouse_x, mouse_y):
      option_clicked = self.GetIndexOfOptionClicked(mouse_y)
      if option_clicked != -1:
        option = self.options_list[option_clicked]
        exec option[1]
    self.menu_closed = True
  
  def HandleMouseMotionEvent(self, mouse_event):
    # Handle mouse motion events with respect to the menu.
    update_rect = self.rect
    mouse_x, mouse_y = mouse_event.pos
    if self.PointInsideMenu(mouse_x, mouse_y):
      option_h = self.GetIndexOfOptionClicked(mouse_y)
      if option_h != self.option_highlighted:
        update_rect = self.rect
        self.option_highlighted = option_h
        self.UpdateSurface()
    return update_rect
