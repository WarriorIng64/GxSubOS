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
import math

def DrawRoundRect(surface, color, rect, corner_radius, width=0):
  # Draws a rectangle with rounded corners on the given surface.
  # If width=0, draw filled; otherwise, draw just the border.
  cr = corner_radius
  tl_rect = pygame.Rect(0, 0, cr, cr)
  tr_rect = pygame.Rect(rect.width - cr, 0, cr, cr)
  bl_rect = pygame.Rect(0, rect.height - cr, cr, cr)
  br_rect = pygame.Rect(rect.width - cr, rect.height - cr, cr, cr)
  top_rect = pygame.Rect(cr, 0, rect.width - 2 * cr, cr)
  middle_rect = pygame.Rect(0, cr, rect.width, rect.height - 2 * cr)
  bottom_rect = pygame.Rect(cr, rect.height - cr, rect.width - 2 * cr, cr)
  pygame.draw.rect(surface, color, top_rect, width)
  pygame.draw.rect(surface, color, middle_rect, width)
  pygame.draw.rect(surface, color, bottom_rect, width)
  if width is 0:
    arc_width = cr / 2
  else:
    arc_width = width / 2
  pygame.draw.arc(surface, color, tl_rect, math.pi / 2, math.pi, arc_width)
  pygame.draw.arc(surface, color, tr_rect, math.pi / 2, 0, arc_width)
  pygame.draw.arc(surface, color, bl_rect, math.pi, 1.5 * math.pi, arc_width)
  pygame.draw.arc(surface, color, br_rect, 1.5 * math.pi, 0, arc_width)
