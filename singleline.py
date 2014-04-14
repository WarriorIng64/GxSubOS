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

import copy
import pygame
import glass, drawingshapes

class Singleline():

  '''A class for displaying a single line of text.'''

  def __init__(self, text, font, width):
    '''Initialize with text of the given font within the given width.'''
    self.text = text
    self.font = font
    self.width = width
    self.scroll_amount = 0
  
  def GetText(self):
    '''Return the current text as a single string.'''
    return self.text
  
  def SetText(self, text):
    '''Change the current text and update.'''
    self.text = text
  
  def SetFont(self, font):
    '''Change the current font and update.'''
    self.font = font
  
  def SetWidth(self, width):
    '''Change the current width and update.'''
    self.width = width
  
  def Render(self):
    '''Return a Surface with the Singleline text properly rendered.'''
    return self.font.render(self.text, True, glass.accent_color)


class EditorSingleline(Singleline):
  
  '''A Singleline subclass which also displays a cursor for text entry.'''
  
  def __init__(self, text, font, width):
    '''Initialize with text of the given font within the given width.'''
    self.text = text
    self.font = font
    self.width = width
    self.cursor_pos = 0
    self.scroll_amount = 0

  def MoveCursorLeft(self):
    '''Moves the current cursor position left one character, if able.'''
    if self.cursor_pos > 0:
      self.cursor_pos -= 1
  
  def MoveCursorRight(self):
    '''Moves the current cursor position right one character, if able.'''
    if self.text != "":
      if self.cursor_pos < len(self.text):
        self.cursor_pos += 1
  
  def SetCursorAtBeginning(self):
    '''Moves the cursor all the way back to the start of the text.'''
    self.cursor_pos = [0, 0]
  
  def SetCursorAtEnd(self):
    '''Moves the cursor all the way to the end of the text.'''
    if len(self.text) != 0:
      self.cursor_pos = len(self.lines) - 1
    else:
      self.cursor_pos = 0
  
  def SetCursorAtLineStart(self):
    '''Sets the cursor at the start of the text.'''
    self.cursor_pos = 0
  
  def GetCursorIndex(self):
    '''Returns the index in the text that the cursor position corresponds to.'''
    return self.cursor_pos
  
  def GetCursorPosition(self):
    '''Returns the current position of the cursor. Same as GetCursorIndex().'''
    return self.GetCursorIndex()
  
  def BackspaceAtCursor(self):
    '''Deletes the character before the cursor position.'''
    if not self.cursor_pos == 0:
      if self.cursor_pos == 1:
        self.text = self.text[1:]
      elif self.cursor_pos == len(self.text) - 1:
        self.text = self.text[:-1]
      else:
        self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
      self.MoveCursorLeft()
  
  def DeleteAtCursor(self):
    '''Deletes the character at the cursor position.'''
    if self.cursor_pos == 0:
      self.text = self.text[1:]
    elif self.cursor_pos == len(self.text) - 1:
      self.text = self.text[:-1]
    else:
      self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
  
  def InsertCharAtCursor(self, character):
    '''Inserts the given character at the cursor position.'''
    if self.cursor_pos == 0:
      self.text = character + self.text
    elif self.cursor_pos == len(self.text):
      self.text = self.text + character
    else:
      self.text = self.text[:self.cursor_pos] + character + self.text[self.cursor_pos:]
    self.MoveCursorRight()
  
  def Render(self):
    '''Return a Surface with the EditorSingleline text and cursor properly rendered.'''
    # Render with proper spacing
    render_height = self.font.get_linesize()
    text_surface = self.font.render(self.text, True, glass.accent_color)
    render_surface = glass.MakeTransparentSurface(self.width, render_height)
    # Render the text surface onto the main surface
    render_surface.blit(text_surface, (0, 0))
    
    # Cursor rendering
    if self.text == "":
      cursor_x = 0
    else:
      cursor_x = self.font.size(self.text[:self.cursor_pos])[0] + self.scroll_amount
    cursor_y = self.font.get_linesize()
    try:
      cursor_w = self.font.size(self.text[self.cursor_pos])[0]
    except IndexError:
      cursor_w = self.font.size(" ")[0]
    cursor_h = self.font.get_linesize()
    cursor_rect = pygame.Rect(cursor_x, cursor_y, cursor_w, cursor_h)
    cursor_surface = glass.MakeTransparentSurface(cursor_w, cursor_h)
    cursor_color = glass.highlight_color
    cursor_color.a = 150
    cursor_surface.fill(cursor_color)
    render_surface.blit(cursor_surface, cursor_rect)
    
    return render_surface
