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

import sys, datetime, pygame
import glass

indicator_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 18)
unknown_indicator_image = pygame.image.load("graphics/indicator_icon_unknown.png")

class Indicator:
  
  '''A class implementing indicators for the indicator tray.'''
  
  def __init__(self, number, name="an indicator", wm=None, frame_code="", click_code="", icon=unknown_indicator_image, image=unknown_indicator_image):
    self.number = number
    self.indicator_name = name
    self.wm = wm
    self.frame_code = frame_code
    self.click_code = click_code
    self.icon = icon
    self.image = image
    self.width = 24
    self.rect = self.image.get_rect()
    self.rect.x = pygame.display.Info().current_w
    self.closed = False

  def RunSetupCode(self, path):
    '''Accepts a string containing the path to the Python script this will run
    to set up all of its variables.'''
    exec(open(path).read())
  
  def SetWindowManager(self, wm):
    '''Provides this Indicator with a reference to the WindowManager.'''
    self.wm = wm
  
  def SetFrameCode(self, code):
    '''Accepts a string containing Python code. This code will be executed once
    each frame for continuous operation. For this reason, code to be passed in
    should be fast to keep the whole SubOS running smoothly.'''
    self.frame_code = code

  def SetClickCode(self, code):
    '''Accepts a string containing Python code. This code will be executed once
    per left click on the Indicator.'''
    self.click_code = code

  def SetIcon(self, icon):
    '''Accepts a surface to use as the icon for this Indicator.'''
    self.icon = icon
  
  def SetIndicatorName(self, name):
    '''Sets this Indicator's display name.'''
    self.indicator_name = name
  
  def RunFrameCode(self):
    '''Executes the currently-set frame code. Meant to be called once each
    frame of the SubOS execution.'''
    if not self.closed:
      try:
        exec(self.frame_code)
      except Exception as e:
        self.closed = True
        print("***" + self.indicator_name + " CRASH: " + str(e))
        if self.wm != None:
          self.wm.ShowPopupMessage("Indicator Crash", "Sorry, but " + self.indicator_name + " needs to close due to an error.")

  def RunClickCode(self):
    '''Executes the currently-set click code. Meant to be called once each
    time the Indicator is left-clicked.'''
    exec(self.click_code)

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

  def HandleMouseButtonDownEvent(self, mouse_event, mouse_button):
    '''Handle a MOUSEDOWN event. Namely, if this indicator is left-clicked, we
    should run the click code.'''
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if mouse_button == 1 and self.rect.collidepoint(mouse_x, mouse_y):
        self.RunClickCode()
