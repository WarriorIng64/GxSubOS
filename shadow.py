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
import window

def LoadShadowImage(filename):
  shadow_path = "graphics/shadows/"
  return pygame.image.load(shadow_path + filename)

def LoadFocusedShadowImage(filename):
  shadow_path = "graphics/shadows/focused/"
  return pygame.image.load(shadow_path + filename)

def LoadLauncherShadow(filename):
  # Loads the given shadow from file and returns the surface
  shadow_path = "graphics/shadows/launcher/"
  return pygame.image.load(shadow_path + filename)

shadow_tl_image = LoadShadowImage("topleft.png")
shadow_t_image = LoadShadowImage("top.png")
shadow_tr_image = LoadShadowImage("topright.png")
shadow_r_image = LoadShadowImage("right.png")
shadow_br_image = LoadShadowImage("bottomright.png")
shadow_b_image = LoadShadowImage("bottom.png")
shadow_bl_image = LoadShadowImage("bottomleft.png")
shadow_l_image = LoadShadowImage("left.png")

shadow_focused_tl_image = LoadFocusedShadowImage("topleft.png")
shadow_focused_t_image = LoadFocusedShadowImage("top.png")
shadow_focused_tr_image = LoadFocusedShadowImage("topright.png")
shadow_focused_r_image = LoadFocusedShadowImage("right.png")
shadow_focused_br_image = LoadFocusedShadowImage("bottomright.png")
shadow_focused_b_image = LoadFocusedShadowImage("bottom.png")
shadow_focused_bl_image = LoadFocusedShadowImage("bottomleft.png")
shadow_focused_l_image = LoadFocusedShadowImage("left.png")

launcher_shadow = LoadLauncherShadow("vertical_left.png")
launcher_shadow_middle = LoadLauncherShadow("vertical_left_middle.png")

shadow_width = shadow_t_image.get_height()

class Corner():
  TL, TR, BL, BR = range(4)

class Edge():
  T, L, R, B = range(4)

def DrawWindowShadowCorner(screen, window_rect, corner):
  # Draws the corner of the shadow for a non-focused window.
  # Returns a Rect for the drawn area.
  offset = window.titlebar_height
  if corner == Corner.TL:
    shadow_image = shadow_tl_image
    pos = (window_rect.left - shadow_width, window_rect.top - shadow_width)
  elif corner == Corner.TR:
    shadow_image = shadow_tr_image
    pos = (window_rect.right - offset, window_rect.top - shadow_width)
  elif corner == Corner.BL:
    shadow_image = shadow_bl_image
    pos = (window_rect.left - shadow_width, window_rect.bottom - offset)
  else:
    shadow_image = shadow_br_image
    pos = (window_rect.right - offset, window_rect.bottom - offset)
  size = shadow_image.get_size()
  screen.blit(shadow_image, (pos, size))
  return pygame.Rect(pos, size)

def DrawWindowShadowEdge(screen, window_rect, edge):
  # Draws the edge of the shadow for a non-focused window.
  # Returns a Rect for the drawn area.
  offset = window.titlebar_height
  if edge == Edge.T:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.top - shadow_width)
    shadow_image = pygame.transform.scale(shadow_t_image, shadow_size)
  elif edge == Edge.L:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.left - shadow_width, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_l_image, shadow_size)
  elif edge == Edge.R:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.right, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_r_image, shadow_size)
  else:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.bottom)
    shadow_image = pygame.transform.scale(shadow_b_image, shadow_size)
  screen.blit(shadow_image, pygame.Rect(shadow_pos, shadow_size))
  return pygame.Rect(shadow_pos, shadow_size)

def DrawFocusedWindowShadowCorner(screen, window_rect, corner):
  # Draws the corner of the shadow for a focused window.
  # Returns a Rect for the drawn area.
  offset = window.titlebar_height
  if corner == Corner.TL:
    shadow_image = shadow_focused_tl_image
    pos = (window_rect.left - shadow_width, window_rect.top - shadow_width)
  elif corner == Corner.TR:
    shadow_image = shadow_focused_tr_image
    pos = (window_rect.right - offset, window_rect.top - shadow_width)
  elif corner == Corner.BL:
    shadow_image = shadow_focused_bl_image
    pos = (window_rect.left - shadow_width, window_rect.bottom - offset)
  else:
    shadow_image = shadow_focused_br_image
    pos = (window_rect.right - offset, window_rect.bottom - offset)
  size = shadow_image.get_size()
  screen.blit(shadow_image, (pos, size))
  return pygame.Rect(pos, size)

def DrawFocusedWindowShadowEdge(screen, window_rect, edge):
  # Draws the edge of the shadow for a focused window.
  # Returns a Rect for the drawn area.
  offset = window.titlebar_height
  if edge == Edge.T:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.top - shadow_width)
    shadow_image = pygame.transform.scale(shadow_focused_t_image, shadow_size)
  elif edge == Edge.L:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.left - shadow_width, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_focused_l_image, shadow_size)
  elif edge == Edge.R:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.right, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_focused_r_image, shadow_size)
  else:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.bottom)
    shadow_image = pygame.transform.scale(shadow_focused_b_image, shadow_size)
  screen.blit(shadow_image, pygame.Rect(shadow_pos, shadow_size))
  return pygame.Rect(shadow_pos, shadow_size)

def DrawWindowShadow(screen, window_rect):
  # Draws the shadow for a non-focused window.
  # Returns a Rect containing the whole area drawn.
  rect_list = []
  rect_list.append(DrawWindowShadowCorner(screen, window_rect, Corner.TL))
  rect_list.append(DrawWindowShadowCorner(screen, window_rect, Corner.TR))
  rect_list.append(DrawWindowShadowCorner(screen, window_rect, Corner.BL))
  rect_list.append(DrawWindowShadowCorner(screen, window_rect, Corner.BR))
  rect_list.append(DrawWindowShadowEdge(screen, window_rect, Edge.T))
  rect_list.append(DrawWindowShadowEdge(screen, window_rect, Edge.L))
  rect_list.append(DrawWindowShadowEdge(screen, window_rect, Edge.R))
  rect_list.append(DrawWindowShadowEdge(screen, window_rect, Edge.B))
  return rect_list[0].unionall(rect_list[1:])

def DrawFocusedWindowShadow(screen, window_rect):
  # Draws the shadow for a non-focused window.
  # Returns a Rect containing the whole area drawn.
  rect_list = []
  rect_list.append(DrawFocusedWindowShadowCorner(screen, window_rect, Corner.TL))
  rect_list.append(DrawFocusedWindowShadowCorner(screen, window_rect, Corner.TR))
  rect_list.append(DrawFocusedWindowShadowCorner(screen, window_rect, Corner.BL))
  rect_list.append(DrawFocusedWindowShadowCorner(screen, window_rect, Corner.BR))
  rect_list.append(DrawFocusedWindowShadowEdge(screen, window_rect, Edge.T))
  rect_list.append(DrawFocusedWindowShadowEdge(screen, window_rect, Edge.L))
  rect_list.append(DrawFocusedWindowShadowEdge(screen, window_rect, Edge.R))
  rect_list.append(DrawFocusedWindowShadowEdge(screen, window_rect, Edge.B))
  return rect_list[0].unionall(rect_list[1:])

def DrawLauncherShadow(launcher):
  # Draws the launcher shadow on the launcher's surface
  if launcher.max_exists:
    return
  mid = launcher.launcher_width / 2
  top_pos = (launcher.launcher_width, 0)
  top_size = (shadow_width, launcher.buttons_edge)
  top_shadow = pygame.transform.scale(launcher_shadow, top_size)
  bottom_pos = (mid, launcher.buttons_edge + mid)
  bottom_size = (shadow_width, launcher.surface.get_height() - launcher.buttons_edge - mid)
  bottom_shadow = pygame.transform.scale(launcher_shadow, bottom_size)
  
  top_rect = pygame.Rect(top_pos, top_size)
  middle_rect = pygame.Rect((mid, launcher.buttons_edge), launcher_shadow_middle.get_size())
  bottom_rect = bottom_pos, bottom_size
  
  launcher.surface.blit(top_shadow, top_rect)
  launcher.surface.blit(launcher_shadow_middle, middle_rect)
  launcher.surface.blit(bottom_shadow, bottom_rect)
