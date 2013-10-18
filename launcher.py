import sys, pygame
from launcherbutton import Launcherbutton
from startbutton import Startbutton
import glass

transparent = pygame.color.Color(0, 0, 0, 0)

class LauncherOrientation:
  TL_V, TL_H, TR_H, TR_V, BR_V, BR_H, BL_H, BL_V = range(8)

class Launcher:
  launcher_color = glass.glass_color
  launcher_color_opaque = glass.glass_color
  launcher_color.a = glass.glass_alpha
  launcher_orientation = LauncherOrientation.TL_V
  launcher_width = 48
  
  def __init__(self, screenw, screenh):
    lw = self.launcher_width
    self.launcher_list = []
    self.startbutton = Startbutton()
    self.rect = pygame.rect.Rect(0, 0, lw, screenh)
    self.surface = pygame.Surface((lw, screenh), pygame.SRCALPHA)
    if glass.enable_transparency:
      self.surface.fill(self.launcher_color)
      self.color_surface = pygame.Surface((lw, screenh), pygame.SRCALPHA)
      self.color_surface.fill(self.launcher_color)
    else:
      self.surface.fill(self.launcher_color_opaque)
  
  def Update(self, screen):
    # Redraw the launcher background
    lw = self.launcher_width
    if len(self.launcher_list) > 0:
      buttons_edge = self.launcher_list[-1].rect.bottom
    else:
      buttons_edge = lw
    if glass.enable_transparency:
      glass.DrawBackground(screen, self.surface, self.rect)
      self.surface = glass.Blur(self.surface)
      self.surface.blit(self.color_surface, [0, 0, 0, 0])
    else:
      self.surface.fill(self.launcher_color_opaque)
    mid = lw / 2
    tri_b = buttons_edge + mid
    triangle_points = [(lw, buttons_edge), (lw, tri_b), (mid, tri_b)]
    transparent_rect = [mid, tri_b, mid, self.surface.get_height() - buttons_edge]
    pygame.draw.polygon(self.surface, transparent, triangle_points)
    pygame.draw.rect(self.surface, transparent, transparent_rect)

  def UpdateWholeLauncher(self, screen):
    # Update all components of the launcher except start button
    for button in self.launcher_list:
      button.UpdatePosition()
    self.Update(screen)

  def UpdateLauncherButtons(self, mouse_event, mouse_button):
    # Update launcher buttons
    new_button_number = 0
    for button in self.launcher_list:
      new_button_number += 1
      button.Update(mouse_event, mouse_button, new_button_number)
      if button.WindowWasClosed():
        self.launcher_list.remove(button)

  def DrawLauncher(self, screen):
    # Draws the launcher onto the given surface
    screen.blit(self.surface, (0, 0))
    for button in self.launcher_list:
      screen.blit(button.image, button.rect)
    screen.blit(self.startbutton.image, self.startbutton.rect)

  def AddLauncherbutton(self, window):
    # Create a new launcherbutton for the given window
    lb = Launcherbutton(window, len(self.launcher_list) + 1)
    self.launcher_list.append(lb)

  def UpdateStartbutton(self, mouse_event, mouse_button):
    # Update the startbutton based on the provided event
    self.startbutton.Update(mouse_event, mouse_button)
