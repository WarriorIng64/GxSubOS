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
from widget import Widget
from multiline import Multiline, EditorMultiline
import glass, keyboardentry

textbox_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 16)
textbox_mono_font = pygame.font.Font("fonts/ubuntu-font-family-0.80/UbuntuMono-R.ttf", 16)

class TextBox(Widget):
  """A Widget subclass which represents a TextBox within a window."""
  def __init__(self, parent_widget=None, parent_window=None, initial_text=None):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.surface = None
    self.text = ""
    self.multiline = Multiline(self.text, textbox_font, pygame.Rect(0, 0, 1, 1))
    self.text_surface = None
    self.SetText(initial_text)
    self.hovered = False
    self.requested_width = 0
    self.requested_height = 0
  
  def SetText(self, text):
    """Sets the text displayed in the textbox."""
    self.text = text
    self.multiline.SetText(text)

  def GetText(self):
    """Returns a string for the text displayed in the textbox."""
    return self.multiline.GetText()

  def HandleMouseButtonDownEvent(self, mouse_x, mouse_y, mouse_button):
    """Handle a MOUSEDOWN event."""
    if self.PointInsideWidget(mouse_x, mouse_y):
      if mouse_button == 1:
        # Left-click
        self.SetAsFocusedWidget(self)
      elif mouse_button == 4:
        # Mouse wheel rolled up
        self.multiline.ScrollUp(16)
      elif mouse_button == 5:
        # Mouse wheel rolled down
        self.multiline.ScrollDown(16)

      # Update widget appearance
      if mouse_button in [1, 4, 5]:
        self.Redraw()
        self.RedrawParentWindow()
  
  def HandleMouseMotionEvent(self, mouse_x, mouse_y):
    """Handle a MOUSEMOTION event."""
    is_hovered = self.PointInsideWidget(mouse_x, mouse_y)
    if self.hovered != is_hovered:
      self.hovered = is_hovered
      self.Redraw()
      self.RedrawParentWindow()
  
  def Redraw(self):
    """Redraw this TextBox."""
    padding = 4
    textbox_color = pygame.color.Color(0, 0, 0)
    textbox_color.a = 100
    if self.rect == None:
      return;
    self.multiline.SetAreaRect(pygame.Rect(0, 0, self.rect.width - padding * 2, self.rect.height - padding * 2))
    self.text_surface = self.multiline.Render()
    self.surface = glass.MakeTransparentSurface(self.rect.width, self.rect.height)
    border_rect = self.surface.get_rect().inflate(-padding, -padding).move(padding / 2, padding / 2)
    pygame.draw.rect(self.surface, textbox_color, border_rect)
    if self.text_surface is not None:
      text_left_align = padding
      text_top_align = padding
      self.surface.blit(self.text_surface, (text_left_align, text_top_align))

class TextEntryBox(TextBox):
  """A TextBox subclass which permits the user to dynamically edit the text it
  contains."""
  def __init__(self, parent_widget=None, parent_window=None, initial_text=None):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.surface = None
    self.text = ""
    self.multiline = EditorMultiline(self.text, textbox_font, pygame.Rect(0, 0, 1, 1))
    self.text_surface = None
    self.SetText(initial_text)
    self.hovered = False
    self.requested_width = 0
    self.requested_height = 0
  
  def HandleKeyDownEvent(self, event):
    """Handles a KEYDOWN event, which is very important for this particular
    class since it handles text input from the keyboard."""
    if event.key == pygame.K_BACKSPACE:
      # Delete text.
      self.multiline.BackspaceAtCursor()
    elif event.key == pygame.K_UP:
      self.multiline.MoveCursorUp()
    elif event.key == pygame.K_DOWN:
      self.multiline.MoveCursorDown()
    elif event.key == pygame.K_LEFT:
      self.multiline.MoveCursorLeft()
    elif event.key == pygame.K_RIGHT:
      self.multiline.MoveCursorRight()
    else:
      self.multiline.InsertCharAtCursor(keyboardentry.GetCharFromKey(event))
    self.Redraw()
    self.RedrawParentWindow()

class TextEntryMonoBox(TextEntryBox):
  """A TextEntryBox subclass which uses a monospace font."""
  def __init__(self, parent_widget=None, parent_window=None, initial_text=None):
    self.parent_widget = parent_widget
    self.parent_window = parent_window
    self.rect = None
    self.surface = None
    self.text = ""
    self.multiline = EditorMultiline(self.text, textbox_mono_font, pygame.Rect(0, 0, 1, 1))
    self.text_surface = None
    self.SetText(initial_text)
    self.hovered = False
    self.requested_width = 0
    self.requested_height = 0
    
