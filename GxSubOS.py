import sys, pygame
from launcher import Launcher
from startbutton import Startbutton
from window import Window
import shadow
from launcherbutton import Launcherbutton
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

def CreateWindow(x, y, width, height, titlebar_text=''):
  # Properly create a new application window that the launcher knows about
  for window in window_list:
    window.set_focus(False)
  window_list.append(Window(x, y, width, height, titlebar_text))
  launcher_list.append(Launcherbutton(window_list[-1], len(window_list)))
  return window_list[-1]

def FindFocusedWindow(window_list, mouse_x, mouse_y):
  # Set the correct focused window for a MOUSEBUTTONDOWN event
  focused_window_found = False
  for window in reversed(window_list):
    if window.window_clicked(mouse_x, mouse_y) and not focused_window_found:
      window.set_focus(True)
      focused_window_found = True
    else:
      window.set_focus(False)

def DrawDesktopSurface(window_list):
  # Update the surface behind the focused window
  desktop_surface.blit(wallpaper, wallpaper_rect)
  for window in window_list[:-1]:
    window.redraw(desktop_surface)
    if not window.is_maximized:
      shadow.DrawWindowShadow(desktop_surface, window.rect)
    desktop_surface.blit(window.surface, window.rect)
  desktop_surface.convert()

def DrawTopWindow(surface, window_list):
  # Draws the top window onto the given surface
  if len(window_list) < 1:
    return
  window = window_list[-1]
  window.redraw(surface)
  if not window.is_maximized:
    if window.has_focus:
      shadow.DrawFocusedWindowShadow(surface, window.rect)
    else:
      shadow.DrawWindowShadow(surface, window.rect)
  surface.blit(window.surface, window.rect)

def DrawLauncher(surface, launcher_list, startbutton):
  # Draws the launcher onto the given surface
  screen.blit(launcher.launcher_surface, (0, 0))
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

launcher = Launcher(width, height)
window_list = []
launcher_list = []
CreateWindow(48, 0, 400, 300, "Window 1")
CreateWindow(200, 200, 500, 250, "Window 2")
CreateWindow(300, 100, 600, 400, "Window 3")
startbutton = Startbutton()

DrawDesktopSurface(window_list)

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
    elif event.type == pygame.MOUSEMOTION:
      mouse_x, mouse_y = event.pos
      mouse_event = event
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = event.pos
      mouse_button = event.button
      mouse_event = event
    elif event.type == pygame.MOUSEBUTTONUP:
      mouse_x, mouse_y = event.pos
      mouse_button = event.button
      mouse_event = event
    # Manage window events
    for window in window_list:
      window.update(mouse_event, mouse_button)
      if window.window_closed:
        window_list.remove(window)
        redraw_all_windows = True
    # Determine which window gets focus
    if event.type == pygame.MOUSEBUTTONDOWN:
      FindFocusedWindow(window_list, mouse_x, mouse_y)
    UpdateLauncherButtons(launcher_list, mouse_event, mouse_button)
  
  # Maintain proper window order
  for window in window_list[:-1]:
    if window.has_focus:
      # This is always last in the window_list so it's drawn on top
      focused_window = window
      window_list.remove(window)
      window_list.append(focused_window)
      redraw_all_windows = True
  # Update launcher button positions
  for button in launcher_list:
    button.UpdatePosition()
  
  # Drawing and game object updates
  if redraw_all_windows:
    DrawDesktopSurface(window_list)
  screen.blit(desktop_surface, desktop_surface.get_rect())
  DrawTopWindow(screen, window_list)
  launcher.update(screen)
  startbutton.update(mouse_event, mouse_button)
  DrawLauncher(screen, launcher_list, startbutton)

  pygame.display.update()
  fpsClock.tick(60)
