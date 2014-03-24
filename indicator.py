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
import glass

indicator_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 18)
unknown_indicator_image = pygame.image.load("graphics/unknown_indicator_image.png")

class Indicator:
  
  '''A class implementing indicators for the indicator tray.'''
  
  def __init__(self, number, frame_code="", click_code="", image=unknown_indicator_image):
    self.number = number
    self.frame_code = frame_code
    self.image = image
    self.width = 24
  
  def SetFrameCode(self, code):
    '''Accepts a string containing Python code. This code will be executed once
    each frame for continuous operation. For this reason, code to be passed in
    should be fast to keep the whole SubOS running smoothly.'''
    self.frame_code = code

  def SetClickCode(self, code):
    '''Accepts a string containing Python code. This code will be executed once
    per left click on the Indicator.'''
    self.click_code = code
  
  def RunFrameCode(self):
    '''Executes the currently-set frame code. Meant to be called once each
    frame of the SubOS execution.'''
    exec self.frame_code

  def RunClickCode(self):
    '''Executes the currently-set click code. Meant to be called once each
    time the Indicator is left-clicked.'''
    exec self.click_code

  def SetWidth(self, width):
    '''Update this Indicator's width in pixels. If a width is not passed in,
    the default width will be used, which should be the same as the height of
    the indicator tray.'''
    self.width = width
  
  def UpdatePosition(self, new_x):
    ''' Returns a Rect covering the area this Indicator was in, if it is moving
    to new_x.'''
    update_rect = self.rect
    move_amount = -(self.rect.x - new_x) / 2
    if move_amount != 0:
      self.rect.move_ip(move_amount, 0)
    update_rect.union_ip(self.rect)
    return update_rect
    
  def UpdateNumber(self, new_number):
    '''Updates this Indicator's number. A number of 0 indicates the rightmost
    position of the indicator tray, with increasingly positive numbers placing
    the Indicator further left. The IndicatorTray is responsible for the correct
    positioning of each Indicator according to their numbers.'''
    self.number = new_number
