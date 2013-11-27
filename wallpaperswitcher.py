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
import glass

padding = 16

class WallpaperSwitcher:
  """A class for implementing a wallpaper switcher."""
  def __init__(self, wallpaper=None):
    switcher_color = glass.glass_color
    switcher_color_opaque = glass.glass_color
    switcher_color.a = glass.glass_alpha
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
    self.wallpaper = wallpaper
    self.preview_list = []
    self.preview_list_rects = []
    self.current_selection = 0
    self.closed = False
    self.surface = pygame.Surface((w / 3, h), pygame.SRCALPHA)
    self.rect = pygame.Rect((w * 2 / 3, 0), (w / 3 + 2, h))
    self.background_surface = pygame.Surface((w / 3, h), pygame.SRCALPHA)
    self.pane_surface = pygame.Surface((w / 3, h), pygame.SRCALPHA)
    self.pane_surface.fill(switcher_color)

    self.preview_size = (w / 3 - 2 * padding, h / 3 - 2 * padding)
    self.top_drawn = 0

    self.UpdatePreviewList()

  def SetWallpaper(self, wp):
    """Assigns a Wallpaper instance to this WallpaperSwitcher."""
    self.wallpaper = wp

  def UpdatePreviewList(self):
    """Updates the list of previews this WallpaperSwitcher will display."""
    for i in range(self.wallpaper.GetNumWallpapers()):
      preview_rect = pygame.Rect((padding, padding + (padding + self.preview_size[1]) * i), self.preview_size)
      self.preview_list.append(self.wallpaper.GetWallpaperPreview(i, preview_rect))
      self.preview_list_rects.append(preview_rect)

  def IncrementCurrentSelection(self):
    """Moves the selection rectangle up one."""
    self.current_selection += 1
    if self.current_selection >= len(self.preview_list):
      self.current_selection = 0
    self.UpdateTopDrawn()

  def DecrementCurrentSelection(self):
    """Moves the selection rectangle down one."""
    self.current_selection -= 1
    if self.current_selection < 0:
      self.current_selection = len(self.preview_list) - 1
    self.UpdateTopDrawn()

  def UpdateTopDrawn(self):
    """Updates which preview will be drawn at the top of the switcher."""
    if self.current_selection < self.top_drawn:
      self.top_drawn = self.current_selection
    if self.current_selection >= self.top_drawn + 3:
      self.top_drawn = self.current_selection - 2
  
  def HandleKeyDownEvent(self, event):
    """Handles a KEYDOWN event for wallpaper scrolling and selection."""
    if event.key == pygame.K_DOWN:
      self.IncrementCurrentSelection()
    elif event.key == pygame.K_UP:
      self.DecrementCurrentSelection()
    elif event.key == pygame.K_RETURN:
      self.wallpaper.SwitchToWallpaperInList(self.current_selection)
      self.closed = True
    elif event.key == pygame.K_ESCAPE:
      self.closed = True

  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handles a MOUSEDOWN event for wallpaper scrolling with the scroll wheel."""
    if mouse_x > self.rect.left:
      if mouse_button == 4:
        # Scroll up
        self.DecrementCurrentSelection()
      elif mouse_button == 5:
        # Scroll down
        self.IncrementCurrentSelection()
  
  def Redraw(self, screen, blurred_surface=None):
    """Redraws the appearance of this WallpaperSwitcher."""
    if glass.enable_transparency:
      if glass.enable_blur and blurred_surface != None:
        self.background_surface.blit(blurred_surface, blurred_surface.get_rect().move(-self.rect.x, -self.rect.y))
      else:
        glass.DrawBackground(screen, self.background_surface, self.rect)
        self.background_surface = glass.Blur(self.background_surface)
    else:
      self.background_surface.fill(self.switcher_color_opaque)
    self.surface.blit(self.background_surface, [0, 0, 0, 0])
    self.surface.blit(self.pane_surface, [0, 0, 0, 0])
    for i in range(len(self.preview_list))[self.top_drawn:]:
      self.surface.blit(self.preview_list[i], self.preview_list_rects[i - self.top_drawn])
      if self.current_selection == i:
        pygame.draw.rect(self.surface, glass.highlight_color, self.preview_list_rects[i - self.top_drawn], 4)
