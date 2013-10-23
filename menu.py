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
import drawingshapes, glass

pygame.font.init()

menu_font = pygame.font.SysFont("Droid Sans", 11)
roundness = 4

class Menu:
  def __init__(self, x=0, y=0):
    self.options_list = []
    self.surface = self.surface = pygame.Surface((0, 0), pygame.SRCALPHA)
    self.menu_color = glass.glass_color
    self.menu_color.a = glass.glass_alpha
    self.x, self.y = x, y

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
    menu_width = max_menu_width
    menu_height = max_entry_height * len(self.options_list)
    self.surface = self.surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
    drawingshapes.DrawRoundRect(self.surface, self.menu_color, pygame.Rect(0, 0, menu_width, menu_height), 4)
