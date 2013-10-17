import sys, pygame
from wallpaper import Wallpaper
from launcher import Launcher
from windowmanager import WindowManager
import glass
pygame.init()

fpsClock = pygame.time.Clock()

size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
mouse_x, mouse_y = 0, 0

pygame.display.set_caption("GxSubOS 2.0 Garter Snake")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
desktop_surface = pygame.Surface((screen.get_width(), screen.get_height()))

system_font = pygame.font.Font(None, 12)

# Desktop shell setup
wallpaper = Wallpaper(size)
launcher = Launcher(width, height)
wm = WindowManager(launcher)
wm.CreateWindow(48, 0, 400, 300, "Window 1")
wm.CreateWindow(200, 200, 500, 250, "Window 2")
wm.CreateWindow(300, 100, 600, 400, "Window 3")

wm.DrawDesktopSurface(desktop_surface, wallpaper)
if glass.enable_blur:
  blurred_desktop_surface = glass.Blur(desktop_surface)
else:
  blurred_desktop_surface = None

# MAIN LOOP
while 1:
  # Check if we quit yet and handle events for windows
  redraw_all_windows = False
  mouse_button = 0
  mouse_event = None;
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
      mouse_x, mouse_y = event.pos
      mouse_event = event
      if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
        mouse_button = event.button
        if event.type == pygame.MOUSEBUTTONDOWN:
          wm.FindFocusedWindow(mouse_x, mouse_y)
          launcher.UpdateStartbutton(mouse_event, mouse_button)
    
    redraw_all_windows = wm.UpdateWindows(mouse_event, mouse_button)
    launcher.UpdateLauncherButtons(mouse_event, mouse_button)
  
  # Drawing and game object updates
  if redraw_all_windows:
    wm.DrawDesktopSurface(desktop_surface, wallpaper)
    if glass.enable_blur:
      blurred_desktop_surface = glass.Blur(desktop_surface)
  screen.blit(desktop_surface, desktop_surface.get_rect())
  wm.DrawTopWindow(screen, blurred_desktop_surface)
  launcher.UpdateWholeLauncher(screen)
  launcher.DrawLauncher(screen)

  pygame.display.update()
  fpsClock.tick(60)
