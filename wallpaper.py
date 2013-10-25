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

import os, pygame
from os import listdir
from os.path import isfile, join

wallpaper_path = "graphics/wallpapers/"
default_path = wallpaper_path + "default_wallpaper_2.0.png"

class Wallpaper:
  def __init__(self, screen_size, path=default_path):
    self.image = pygame.image.load(path)
    self.image = pygame.transform.smoothscale(self.image, screen_size)
    self.image = self.image.convert()
    self.rect = self.image.get_rect()
    self.rect.topleft = (0, 0)
    self.wallpaper_list = []
    self.UpdateWallpaperList()
  
  def LoadWallpaper(self, path):
    del self.image
    self.image = pygame.image.load(path)
    self.image = pygame.transform.smoothscale(self.image, screen_size)
    self.image = self.image.convert()
    self.rect = self.image.get_rect()
    self.rect.topleft = (0, 0)
  
  def UpdateWallpaperList(self):
    self.wallpaper_list = [wf for wf in listdir(wallpaper_path) if isfile(join(wallpaper_path, wf))]
