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

import pygame

glass_blur_amount = 5
glass_color = pygame.color.Color(0, 20, 20)
content_area_color = pygame.color.Color(10, 40, 40)
highlight_color = 0, 255, 255
glass_alpha = 210
accent_color = pygame.color.Color(0, 255, 255)
enable_blur = True
enable_transparency = True

def Blur(surface):
  if not enable_blur:
    return surface
  size = surface.get_size()
  for i in range(glass_blur_amount):
    surface2 = pygame.transform.smoothscale(surface,(size[0]/2,size[1]/2))
    surface2 = pygame.transform.smoothscale(surface2,size)
    surface = pygame.transform.smoothscale(surface2,size)
  return surface

def DrawBackground(screen, surface, rect):
  # Draws the screen onto the given surface with an offset
  offset_rect = screen.get_rect().move(-rect.x, -rect.y)
  surface.blit(screen, offset_rect)

def UpdateBlurredDesktopSurface(blurred_desktop_surface, desktop_surface):
  if enable_blur:
    blurred_desktop_surface = Blur(desktop_surface)
  else:
    blurred_desktop_surface = None
