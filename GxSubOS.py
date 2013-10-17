import sys, pygame
from launcher import Launcher
from startbutton import Startbutton
from windowmanager import WindowManager
import shadow
from launcherbutton import Launcherbutton
import glass
pygame.init()

fpsClock = pygame.time.Clock()

size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
mouse_x, mouse_y = 0, 0

pygame.display.set_caption("GxSubOS 2.0 Garter Snake")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
desktop_surface = pygame.Surface((screen.get_width(), screen.get_height()))

system_font = pygame.font.Font(None, 12)

# Wallpaper setup
wallpaper = pygame.image.load("graphics/default_wallpaper.png")
wallpaper = pygame.transform.smoothscale(wallpaper, (width, height))
wallpaper = wallpaper.convert()
wallpaper_rect = wallpaper.get_rect()
wallpaper_rect.topleft = (0, 0)

def DrawLauncher(surface, launcher_list, startbutton):
  # Draws the launcher onto the given surface
  screen.blit(launcher.surface, (0, 0))
  for button in launcher_list:
    screen.blit(button.image, button.rect)
  screen.blit(startbutton.image, startbutton.rect)

def UpdateLauncherButtons(launcher_list, mouse_event, mouse_button):
  # Update launcher buttons
  new_button_number = 0
  for button in launcher_list:
    new_button_number += 1
    button.Update(mouse_event, mouse_button, new_button_number)
    if button.WindowWasClosed():
      launcher_list.remove(button)

def UpdateWholeLauncher(screen, launcher, launcher_list):
  # Update all components of the launcher except start button
  for button in launcher_list:
    button.UpdatePosition()
  launcher.Update(screen)

launcher = Launcher(width, height)
launcher_list = []
wm = WindowManager()
wm.CreateWindow(48, 0, 400, 300, launcher_list, "Window 1")
wm.CreateWindow(200, 200, 500, 250, launcher_list, "Window 2")
wm.CreateWindow(300, 100, 600, 400, launcher_list, "Window 3")
startbutton = Startbutton()

wm.DrawDesktopSurface(desktop_surface, wallpaper, wallpaper_rect)
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
          startbutton.Update(mouse_event, mouse_button)
    
    redraw_all_windows = wm.RemoveClosedWindows(mouse_event, mouse_button)
    UpdateLauncherButtons(launcher_list, mouse_event, mouse_button)
  
  redraw_all_windows = redraw_all_windows or wm.MaintainWindowOrder()
  
  # Drawing and game object updates
  if redraw_all_windows:
    wm.DrawDesktopSurface(desktop_surface, wallpaper, wallpaper_rect)
    if glass.enable_blur:
      blurred_desktop_surface = glass.Blur(desktop_surface)
  screen.blit(desktop_surface, desktop_surface.get_rect())
  wm.DrawTopWindow(screen, blurred_desktop_surface)
  UpdateWholeLauncher(screen, launcher, launcher_list)
  DrawLauncher(screen, launcher_list, startbutton)

  pygame.display.update()
  fpsClock.tick(60)
