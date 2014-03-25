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
from indicator import Indicator
import glass, shadow

transparent = pygame.color.Color(0, 0, 0, 0)

class IndicatorTray():
  
  '''A class implementing a tray where various Indicators are displayed.'''
  
  tray_color = glass.glass_color
  tray_color_opaque = glass.glass_color
  tray_color.a = glass.glass_alpha
  tray_height = 24

  def __init__(self, screenw, screenh):
    self.indicator_list = []
    self.surface = glass.MakeTransparentSurface(screenw, self.tray_height)
    if glass.enable_transparency:
      self.surface.fill(self.tray_color)
      self.color_surface = pygame.Surface((screenw, self.tray_height), pygame.SRCALPHA)
      self.color_surface.fill(self.tray_color)
    else:
      self.surface.fill(self.tray_color_opaque)
      self.color_surface = pygame.Surface((screenw, self.tray_height))
      self.color_surface.fill(self.tray_color_opaque)
    self.update_rect = pygame.Rect(0, 0, 0, 0)
    self.wm = None

  def SetWindowManager(self, windowmanager):
    '''Sets the WindowManager that this IndicatorTray will connect to.'''
    self.wm = windowmanager

  def GetIndicatorsWidth(self):
    '''Returns the total width in pixels of all the Indicators currently stored
    in the indicator_list.'''
    width = 0
    for indicator in self.indicator_list:
      width += indicator.width
    return width

  def UpdateIndicatorPositions(self):
    '''Updates the positions of all the Indicators in the list.'''
    next_right = 0
    for indicator in self.indicator_list:
      new_x = pygame.display.Info().current_w - next_right - indicator.width
      self.update_rect.union_ip(indicator.UpdatePosition(new_x))
      next_right += indicator.width

  def RedrawBackground(self, screen):
    '''Redraw the background behind the Indicators.'''
    tray_width = self.GetIndicatorsWidth()
    tray_left = pygame.display.Info().current_w - tray_width
    glass.DrawBackground(screen, self.surface, self.surface.get_rect())
    if glass.enable_transparency:
      self.surface = glass.Blur(self.surface)
    self.surface.blit(self.color_surface, [0, 0, 0, 0])
    triangle_points = [(tray_left - self.tray_height, 0), (tray_left - self.tray_height, self.tray_height), (tray_left, self.tray_height)]
    pygame.draw.polygon(self.surface, transparent, triangle_points)
    pygame.draw.rect(self.surface, transparent, pygame.Rect(0, 0, tray_left - self.tray_height, self.tray_height))

  def DrawTray(self, screen):
    '''Draws this IndicatorTray onto the provided Surface. Returns a Rect
    containing the area which was drawn to.'''
    screen.blit(self.surface, (0, 0))
    for indicator in self.indicator_list:
      screen.blit(indicator.image, indicator.rect)
    return self.update_rect

  def UpdateWholeTray(self, screen):
    '''Update the whole IndicatorTray and its Indicators.'''
    self.UpdateIndicatorPositions()
    for indicator in self.indicator_list:
      indicator.RunFrameCode()
    self.RedrawBackground(screen)
