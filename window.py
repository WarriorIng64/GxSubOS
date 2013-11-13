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
import glass, drawingshapes, container

pygame.font.init()

titlebar_height = 24
titlebar_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 18)

class Window:
  """A class for the application windows in the desktop environment of GxSubOS."""
  window_color = glass.glass_color
  window_color_opaque = glass.glass_color
  window_color.a = glass.glass_alpha
  content_color = glass.content_area_color
  content_color_opaque = glass.content_area_color
  content_color.a = glass.glass_alpha
  
  def __init__(self, x, y, width, height, titlebar_text=''):
    self.rect = pygame.rect.Rect(x, y, width, height)
    self.close_image = pygame.image.load("graphics/close.png")
    self.resize_image = pygame.image.load("graphics/resize.png")
    self.close_rect = self.close_image.get_rect()
    self.resize_rect = self.resize_image.get_rect()
    self.resize_rect.move_ip(width - titlebar_height, height - titlebar_height)
    self.content_area_rect = pygame.Rect(0, titlebar_height, self.rect.width, self.rect.height - 2 * titlebar_height)
    
    self.CreateSurfaces(width, height)
    self.titlebar_text = titlebar_text
    self.being_dragged = False
    self.being_resized = False
    self.is_maximized = False
    self.restore_rect = self.rect
    self.has_focus = True
    self.top_level_container = container.Container(None, self)
    self.DrawWindowSurface()
    self.click_x, self.click_y = 0, 0
    self.window_closed = False
  
  def Redraw(self, screen, blurred_surface=None):
    """Redraws this Window's surface in preparation for the next blitting."""
    if glass.enable_transparency:
      if glass.enable_blur and blurred_surface != None:
        self.background_surface.blit(blurred_surface, blurred_surface.get_rect().move(-self.rect.x, -self.rect.y))
      else:
        glass.DrawBackground(screen, self.background_surface, self.rect)
        self.background_surface = glass.Blur(self.background_surface)
    else:
      self.background_surface.fill(self.window_color_opaque)
    self.surface.blit(self.background_surface, [0, 0, 0, 0])
    self.surface.blit(self.window_surface, [0, 0, 0, 0])
  
  def DrawTitlebarSeparator(self, surface, upper):
    """Draws a titlebar separator on the given surface. upper is a Boolean
    indicating whether this is for the top titlebar."""
    if upper:
      height = titlebar_height
    else:
      height = self.rect.height - titlebar_height
    drawingshapes.DrawHSeparator(surface, self.rect.width, height)
  
  def DrawTitlebarSeparators(self):
    separator_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    self.DrawTitlebarSeparator(separator_surface, True)
    self.DrawTitlebarSeparator(separator_surface, False)
    self.window_surface.blit(separator_surface, [0, 0, 0, 0])
  
  def DrawTitlebar(self):
    """Draw the titlebars on the window_surface."""
    # Draw titlebar background
    pygame.draw.rect(self.window_surface, glass.glass_color, [0, 0, self.rect.width, titlebar_height])
    pygame.draw.rect(self.window_surface, glass.glass_color, [0, self.rect.height - titlebar_height, self.rect.width, titlebar_height])
    # Draw separators
    self.DrawTitlebarSeparators()
    # Draw titlebar text
    text_surf = titlebar_font.render(self.titlebar_text, True, glass.accent_color)
    text_surf.get_rect().x = self.rect.x + titlebar_height
    text_surf.get_rect().y = self.rect.y
    self.window_surface.blit(text_surf, [titlebar_height, 1, 0, 0])
  
  def MoveByAmount(self, x, y):
    """Moves this Window by the given x and y values."""
    self.rect.move_ip(x, y)
    self.restore_rect = self.rect
  
  def CloseButtonClicked(self, x, y):
    """Returns true if the given x and y values are inside the area where the
    close button is."""
    close_x1, close_x2 = self.rect.left, self.rect.left + titlebar_height
    close_y1, close_y2 = self.rect.top, self.rect.top + titlebar_height
    return close_x1 < x < close_x2 and close_y1 < y < close_y2
  
  def ResizeButtonClicked(self, x, y):
    """Returns true if the given x and y values are inside the area where the
    resize button is. This function will always return false if the window is
    maximized."""
    if self.is_maximized:
      return False
    resize_x1 = self.rect.x + self.rect.width - titlebar_height
    resize_x2 = self.rect.x + self.rect.width
    resize_y1 = self.rect.y + self.rect.height - titlebar_height
    resize_y2 = self.rect.y + self.rect.height
    return resize_x1 < x < resize_x2 and resize_y1 < y < resize_y2
  
  def TitlebarClicked(self, x, y):
    """Returns true if the given x and y values are inside the area where the
    titlebars are."""
    x1, x2 = self.rect.left, self.rect.right
    y1, y2 = self.rect.top, self.rect.top + titlebar_height
    top_titlebar_clicked = x1 < x < x2 and y1 < y < y2
    y1, y2 = self.rect.bottom - titlebar_height, self.rect.bottom
    bottom_titlebar_clicked = x1 < x < x2 and y1 < y < y2
    return top_titlebar_clicked or bottom_titlebar_clicked
  
  def WindowClicked(self, x, y):
    """Returns true if the given x and y values are inside the area of this
    Window."""
    x1, x2 = self.rect.left, self.rect.right
    y1, y2 = self.rect.top, self.rect.bottom
    return x1 < x < x2 and y1 < y < y2
  
  def DrawWindowSurface(self):
    """Updates the window surface, but not the background or anything else."""
    # Draw the window chrome and prepare the window_surface for blitting
    w, h = self.rect.width, self.rect.height
    window_rect = self.window_surface.get_rect()
    self.window_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(self.window_surface, glass.content_area_color, self.content_area_rect)
    self.DrawTitlebar()
    self.window_surface.blit(self.close_image, self.close_rect)
    if not self.is_maximized:
      self.window_surface.blit(self.resize_image, self.resize_rect)
    self.window_surface.convert_alpha()
    self.top_level_container.Redraw()
    self.window_surface.blit(self.top_level_container.surface, self.top_level_container.rect)
  
  def SetFocus(self, focus):
    """Sets the focused state of this Window."""
    if self.has_focus != focus:
      self.has_focus = focus
      self.DrawWindowSurface()
    else:
      self.has_focus = focus
  
  def Resize(self, new_width, new_height):
    """Resizes this Window to the new width and height values provided."""
    correct_width = max(new_width, titlebar_height * 2)
    correct_height = max(new_height, titlebar_height * 2)
    x, y = self.rect.x, self.rect.y
    self.rect = pygame.rect.Rect(x, y, correct_width, correct_height)
    self.CreateSurfaces(correct_width, correct_height)
    self.DrawWindowSurface()
    self.resize_rect = self.resize_image.get_rect()
    self.resize_rect.move_ip(correct_width - titlebar_height, correct_height - titlebar_height)
    self.UpdateContentAreaRect()
    self.top_level_container.Redraw()
  
  def UpdateContentAreaRect(self):
    """Updates the Rect denoting the area Widgets occupy."""
    t_h = titlebar_height
    w = self.rect.width
    h = self.rect.height
    self.content_area_rect = pygame.Rect(0, t_h, w, h - 2 * t_h)
  
  def CreateSurfaces(self, w, h):
    """Creates the surfaces this Window will use for its different drawing
    layers."""
    self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
    self.window_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    self.background_surface = pygame.Surface((w, h), pygame.SRCALPHA)
  
  def Maximize(self):
    """Maximizes this Window."""
    self.restore_rect = self.rect
    maximized_width = pygame.display.Info().current_w - 48
    maximized_height = pygame.display.Info().current_h
    self.rect.x = 48 # Replace this later with a variable for desktop size
    self.rect.y = 0
    self.Resize(maximized_width, maximized_height)
    self.DrawWindowSurface()
    self.is_maximized = True
  
  def Unmaximize(self):
    """Unmaximizes this Window."""
    if self.is_maximized:
      self.rect.x = self.restore_rect.x
      self.rect.y = self.restore_rect.y
      self.Resize(self.restore_rect.width, self.restore_rect.height)
      self.DrawWindowSurface()
      self.is_maximized = False
  
  def Drag(self, mouse_x, mouse_y):
    """Drags this Window using the given mouse coordinates and comparing them
    to internally stored coordinates where the initial click occurred."""
    offset_x, offset_y = mouse_x - self.click_x, mouse_y - self.click_y
    self.MoveByAmount(offset_x, offset_y)
    # Dragging limits
    if self.rect.y < 0:
      self.rect.y = 0
    if self.rect.y + titlebar_height > pygame.display.Info().current_h:
      self.rect.y = pygame.display.Info().current_h - titlebar_height
    self.click_x = mouse_x
    self.click_y = mouse_y
  
  def MouseResize(self, mouse_x, mouse_y):
    """Resizes this window using the given mouse coordinates."""
    offset_x, offset_y = mouse_x - self.click_x, mouse_y - self.click_y
    self.Resize(self.rect.width + offset_x, self.rect.height + offset_y)
    self.click_x = mouse_x
    self.click_y = mouse_y
  
  def StartResizing(self, mouse_x, mouse_y):
    """Puts this Window into resize mode."""
    self.being_resized = True
    self.click_x, self.click_y = mouse_x, mouse_y
  
  def StartDragging(self, mouse_x, mouse_y):
    """Puts this Window into dragging mode."""
    self.being_dragged = True
    self.click_x, self.click_y = mouse_x, mouse_y
  
  def AddWidget(self, widget, parent_widget=None):
    """Adds a new Widget to this window."""
    if parent_widget == None:
      self.top_level_container.AddWidget(widget)
    else:
      if isinstance(parent_widget, container.Container):
        parent_widget.AddWidget(widget)
        self.DrawWindowSurface()
      else:
        print "Warning: Attempt to add child widget to non-Container."
