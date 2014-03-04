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

import sys, subprocess, pygame, setup, pygame.mixer
from pygame.locals import *
from appdb import AppDB
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
loading_font = pygame.font.Font("fonts/Roboto/Roboto-Regular.ttf", 32)

# First-time setup of database and settings, and loading
loading_spinner = pygame.image.load("graphics/progress_spinner_256.png")
loading_message = loading_font.render("GxSubOS is starting up, please wait...", True, glass.accent_color)
screen_center_x, screen_center_y = screen.get_width() / 2, screen.get_height() / 2
text_left_align = screen_center_x - loading_message.get_width() / 2
text_top_align = screen_center_y - loading_message.get_height() / 2
screen.fill((0, 0, 0))
screen.blit(loading_spinner, (screen_center_x - loading_spinner.get_width() / 2, screen_center_y - loading_spinner.get_height() / 2))
screen.blit(loading_message, (text_left_align, text_top_align))
pygame.display.update(screen.get_rect())
degrees = 0

loading_subprocesses = setup.Setup()
print "Num of subprocesses: " + str(len(loading_subprocesses))
while len(loading_subprocesses) != 0:
  # Display an animated loading screen
  screen.fill((0, 0, 0))
  degrees -= 5
  if degrees <= -360:
    degrees = 0
  loading_spins = pygame.transform.rotate(loading_spinner, degrees)
  screen.blit(loading_spins, (screen_center_x - loading_spins.get_width() / 2, screen_center_y - loading_spins.get_height() / 2))
  screen.blit(loading_message, (text_left_align, text_top_align))
  pygame.display.flip()
  for sp in loading_subprocesses:
    if sp.poll() != None:
      loading_subprocesses.remove(sp)
  fpsClock.tick(60)
screen.fill((0, 0, 0))
loading_message = loading_font.render("GxSubOS will start in a moment...", True, glass.accent_color)
text_left_align = screen.get_width() / 2 - loading_message.get_width() / 2
text_top_align = screen.get_height() / 2 - loading_message.get_height() / 2
screen.blit(loading_message, (text_left_align, text_top_align))
pygame.display.flip()

# Desktop shell setup
wallpaper = Wallpaper(size)
launcher = Launcher(width, height)
wm = WindowManager(launcher, wallpaper)
launcher.SetWindowManager(wm)
pygame.key.set_repeat(500, 50)

wm.DrawDesktopSurface(desktop_surface, wallpaper)
blurred_desktop_surface = None
glass.UpdateBlurredDesktopSurface(blurred_desktop_surface, desktop_surface)

mouse_list = [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]
mouse_button_list = [MOUSEBUTTONDOWN, MOUSEBUTTONUP]
pygame.event.set_allowed([QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

update_rects = [screen.get_rect()]

pygame.mixer.init()
startup_sound = pygame.mixer.Sound("sounds/startup.ogg")
startup_sound.play()

# Fade in from black
fadein_black_surface = pygame.Surface((screen.get_width(), screen.get_height())).convert()
fadein_black_surface.fill((0, 0, 0))
fadein_alpha = 255
fadein_black_surface.set_alpha(fadein_alpha)
while fadein_alpha > 0:
  screen.blit(wallpaper.image, wallpaper.rect)
  fadein_black_surface.set_alpha(fadein_alpha)
  screen.blit(fadein_black_surface, fadein_black_surface.get_rect())
  pygame.display.flip()
  fadein_alpha -= 5
  fpsClock.tick(60)
del fadein_black_surface

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
  update_rects.append(wm.DrawPopupMessage(screen))

  pygame.display.update(update_rects)
  wm.ResetUpdateRect()
  launcher.ResetUpdateRect()
  update_rects = []
  fpsClock.tick(60)
