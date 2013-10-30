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
from wallpaper import Wallpaper

class WallpaperSwitcher:
  def __init__(self, wallpaper=None):
    self.wallpaper = wallpaper
    self.preview_list = []
    self.current_selection = 0

  def SetWallpaper(self, wp):
    self.wallpaper = wp

  def UpdatePreviewList(self):
    for i in range(self.wallpaper.GetNumWallpapers()):
      self.preview_list.append(self.wallpaper.GetWallpaperPreview(i))

  def IncrementCurrentSelection(self):
    self.current_selection += 1
    if self.current_selection >= len(self.preview_list):
      self.current_selection = 0

  def DecrementCurrentSelection(self):
    self.current_selection -= 1
    if self.current_selection < 0:
      self.current_selection = len(self.preview_list) - 1
