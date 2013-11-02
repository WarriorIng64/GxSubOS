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
from pygame.locals import *
from wallpaper import Wallpaper
from launcher import Launcher
from windowmanager import WindowManager
from menu import Menu
import glass
pygame.init()

fpsClock = pygame.time.Clock()

size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
mouse_x, mouse_y = 0, 0

pygame.display.set_caption("GxSubOS 2.0 Garter Snake")
flags = FULLSCREEN | DOUBLEBUF | HWSURFACE
screen = pygame.display.set_mode((0, 0), flags)
screen.set_alpha(None)
desktop_surface = pygame.Surface((screen.get_width(), screen.get_height()))

system_font = pygame.font.Font(None, 12)

# Desktop shell setup
wallpaper = Wallpaper(size)
launcher = Launcher(width, height)
wm = WindowManager(launcher, wallpaper)
launcher.SetWindowManager(wm)

wm.DrawDesktopSurface(desktop_surface, wallpaper)
blurred_desktop_surface = None
glass.UpdateBlurredDesktopSurface(blurred_desktop_surface, desktop_surface)

mouse_list = [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]
mouse_button_list = [MOUSEBUTTONDOWN, MOUSEBUTTONUP]
pygame.event.set_allowed([QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

update_rects = [screen.get_rect()]

# MAIN LOOP
while 1:
  # Check if we quit yet and handle events for windows
  redraw_all_windows = False
  mouse_button = 0
  mouse_event = None;
  for event in pygame.event.get():
    if event.type is QUIT:
      pygame.quit()
      sys.exit()
    elif event.type in mouse_list:
      mouse_x, mouse_y = event.pos
      mouse_event = event
      if event.type in mouse_button_list:
        mouse_button = event.button
        if event.type is MOUSEBUTTONDOWN:
          wm.HandleMouseButtonDownEvent(mouse_x, mouse_y, mouse_button)
          launcher.HandleMouseButtonDownEvent(mouse_event, mouse_button)
        else:
          wm.HandleMouseButtonUpEvent(mouse_x, mouse_y, mouse_button)
      else:
        wm.HandleMouseMotionEvent(mouse_x, mouse_y)
        launcher.HandleMouseMotionEvent(mouse_event)
    elif event.type is KEYDOWN:
      wm.HandleKeyDownEvent(event)
  
  # Drawing and game object updates
  if wm.RedrawNeeded():
    wm.DrawDesktopSurface(desktop_surface, wallpaper)
    glass.UpdateBlurredDesktopSurface(blurred_desktop_surface, desktop_surface)
    update_rects.append(desktop_surface.get_rect())
  screen.blit(desktop_surface, desktop_surface.get_rect())
  update_rects.append(wm.DrawTopWindow(screen, blurred_desktop_surface))
  launcher.UpdateWholeLauncher(screen, wm)
  update_rects.append(launcher.DrawLauncher(screen))
  update_rects.append(wm.DrawWallpaperSwitcher(screen))

  pygame.display.update(update_rects)
  wm.ResetUpdateRect()
  launcher.ResetUpdateRect()
  update_rects = []
  fpsClock.tick(60)
