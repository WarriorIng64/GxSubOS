import sys, pygame
from launcher import Launcher
from startbutton import Startbutton
from window import *
from launcherbutton import Launcherbutton
pygame.init()

fpsClock = pygame.time.Clock()

size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
mouse_x, mouse_y = 0, 0

pygame.display.set_caption("GxSubOS 2.0 Garter Snake")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

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

def DrawWindowShadow(screen, window_rect):
  # Draw a shadow around the given window area
  shadow_offset = titlebar_height / 2
  shadow_width = titlebar_height
  # Corners
  screen.blit(shadow_tl_image, [window_rect.left - shadow_offset, window_rect.top - shadow_offset, shadow_width, shadow_width])
  screen.blit(shadow_tr_image, [window_rect.right - shadow_offset, window_rect.top - shadow_offset, shadow_width, shadow_width])
  screen.blit(shadow_bl_image, [window_rect.left - shadow_offset, window_rect.bottom - shadow_offset, shadow_width, shadow_width])
  screen.blit(shadow_br_image, [window_rect.right - shadow_offset, window_rect.bottom - shadow_offset, shadow_width, shadow_width])
  # Edges
  screen.blit(pygame.transform.scale(shadow_t_image, (window_rect.width - shadow_width, shadow_width)), [window_rect.left + shadow_offset, window_rect.top - shadow_offset, window_rect.width - shadow_width, shadow_width])
  screen.blit(pygame.transform.scale(shadow_l_image, (shadow_width, window_rect.height - shadow_width)), [window_rect.left - shadow_offset, window_rect.top + shadow_offset, shadow_width, window_rect.height - shadow_width])
  screen.blit(pygame.transform.scale(shadow_r_image, (shadow_width, window_rect.height - shadow_width)), [window_rect.right - shadow_offset, window_rect.top + shadow_offset, shadow_width, window_rect.height - shadow_width])
  screen.blit(pygame.transform.scale(shadow_b_image, (window_rect.width - shadow_width, shadow_width)), [window_rect.left + shadow_offset, window_rect.bottom - shadow_offset, window_rect.width - shadow_width, shadow_width])

launcher = Launcher(width, height)
window_list = []
launcher_list = []
CreateWindow(48, 0, 400, 300, "Window 1")
CreateWindow(200, 200, 500, 250, "Window 2")
CreateWindow(300, 100, 600, 400, "Window 3")
startbutton = Startbutton()

# MAIN LOOP
while 1:
  # Check if we quit yet and handle events for windows
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
    # Determine which window gets focus
    if event.type == pygame.MOUSEBUTTONDOWN:
      focused_window_found = False
      for window in reversed(window_list):
        if window.window_clicked(mouse_x, mouse_y) and not focused_window_found:
          window.set_focus(True)
          focused_window_found = True
        else:
          window.set_focus(False)
    # Update launcher buttons
    new_button_number = 0
    for button in launcher_list:
      new_button_number += 1
      button.update(mouse_event, mouse_button, new_button_number)
      if button.window_closed:
        launcher_list.remove(button)
  
  # Maintain proper window order
  for window in window_list:
    if window.has_focus:
      # This is always last in the window_list so it's drawn on top
      focused_window = window
      window_list.remove(window)
      window_list.append(focused_window)
  # Update launcher button positions
  for button in launcher_list:
    button.update_position()
  
  # Drawing and game object updates
  screen.blit(wallpaper, wallpaper_rect)
  for window in window_list:
    window.redraw(screen)
    DrawWindowShadow(screen, window.rect)
    screen.blit(window.surface, window.rect)
  launcher.update(screen)
  startbutton.update(mouse_event, mouse_button)
  screen.blit(launcher.launcher_surface, (0, 0))
  for button in launcher_list:
    screen.blit(button.image, button.rect)
  screen.blit(startbutton.image, startbutton.rect)

  pygame.display.update()
  fpsClock.tick(60)
