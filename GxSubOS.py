import sys, pygame
from pygame.locals import *
from wallpaper import Wallpaper
from launcher import Launcher
from windowmanager import WindowManager
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
wm = WindowManager(launcher)
launcher.SetWindowManager(wm)
wm.CreateWindow(48, 0, 400, 300, "Window 1")
wm.CreateWindow(200, 200, 500, 250, "Window 2")
wm.CreateWindow(300, 100, 600, 400, "Window 3")

wm.DrawDesktopSurface(desktop_surface, wallpaper)
blurred_desktop_surface = None
glass.UpdateBlurredDesktopSurface(blurred_desktop_surface, desktop_surface)

mouse_list = [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]
mouse_button_list = [MOUSEBUTTONDOWN, MOUSEBUTTONUP]
pygame.event.set_allowed([QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

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
          launcher.UpdateStartbutton(mouse_event, mouse_button)
        else:
          wm.HandleMouseButtonUpEvent(mouse_x, mouse_y, mouse_button)
      else:
        wm.HandleMouseMotionEvent(mouse_x, mouse_y)
    
    launcher.UpdateLauncherButtons(mouse_event, mouse_button)
  
  # Drawing and game object updates
  update_rects = []
  if wm.RedrawNeeded():
    wm.DrawDesktopSurface(desktop_surface, wallpaper)
    glass.UpdateBlurredDesktopSurface(blurred_desktop_surface, desktop_surface)
    update_rects.append(desktop_surface.get_rect())
  screen.blit(desktop_surface, desktop_surface.get_rect())
  update_rects.append(wm.DrawTopWindow(screen, blurred_desktop_surface))
  launcher.UpdateWholeLauncher(screen, wm)
  update_rects.append(launcher.DrawLauncher(screen))

  pygame.display.update(update_rects)
  wm.ResetUpdateRect()
  fpsClock.tick(60)
