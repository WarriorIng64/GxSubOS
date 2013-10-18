import sys, pygame
from launcherbutton import Launcherbutton
from startbutton import Startbutton
import glass

transparent = pygame.color.Color(0, 0, 0, 0)
shadow_path = "graphics/shadows/launcher/"
launcher_shadow = pygame.image.load(shadow_path + "vertical_left.png")
launcher_shadow_middle = pygame.image.load(shadow_path + "vertical_left_middle.png")

class LauncherOrientation:
  TL_V, TL_H, TR_H, TR_V, BR_V, BR_H, BL_H, BL_V = range(8)

class Launcher:
  launcher_color = glass.glass_color
  launcher_color_opaque = glass.glass_color
  launcher_color.a = glass.glass_alpha
  launcher_orientation = LauncherOrientation.TL_V
  launcher_width = 48
  shadow_width = launcher_shadow.get_width()
  
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
    self.max_exists = False
    self.buttons_edge = self.surface.get_height()
    self.wm = None
  
  def SetWindowManager(self, windowmanager):
    self.wm = windowmanager
  
  def Update(self, screen, wm):
    # Redraw the launcher background
    lw = self.launcher_width
    self.max_exists = wm.MaximizedWindowExists()
    if len(self.launcher_list) > 0 and not self.max_exists:
      self.buttons_edge = self.launcher_list[-1].rect.bottom
    else:
      self.buttons_edge = lw
    if glass.enable_transparency:
      glass.DrawBackground(screen, self.surface, self.rect)
      self.surface = glass.Blur(self.surface)
      self.surface.blit(self.color_surface, [0, 0, 0, 0])
    else:
      self.surface.fill(self.launcher_color_opaque)
    if not self.max_exists:
      mid = lw / 2
      tri_b = self.buttons_edge + mid
      triangle_points = [(lw, self.buttons_edge), (lw, tri_b), (mid, tri_b)]
      transparent_rect = [mid, tri_b, mid, self.surface.get_height() - self.buttons_edge]
      pygame.draw.polygon(self.surface, transparent, triangle_points)
      pygame.draw.rect(self.surface, transparent, transparent_rect)
      

  def UpdateWholeLauncher(self, screen, window_manager):
    # Update all components of the launcher except start button
    for button in self.launcher_list:
      button.UpdatePosition()
    self.Update(screen, window_manager)

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
    self.DrawLauncherShadow(screen)
  
  def DrawLauncherShadow(self, screen):
    # Draws the launcher shadow on the given surface
    if self.max_exists:
      return
    mid = self.launcher_width / 2
    top_pos = (self.launcher_width, 0)
    top_size = (self.shadow_width, self.buttons_edge)
    top_shadow = pygame.transform.scale(launcher_shadow, top_size)
    bottom_pos = (mid, self.buttons_edge + mid)
    bottom_size = (self.shadow_width, self.surface.get_height() - self.buttons_edge - mid)
    bottom_shadow = pygame.transform.scale(launcher_shadow, bottom_size)
    screen.blit(top_shadow, (top_pos, top_size))
    screen.blit(launcher_shadow_middle, ((mid, self.buttons_edge), launcher_shadow_middle.get_size()))
    screen.blit(bottom_shadow, (bottom_pos, bottom_size))

  def AddLauncherbutton(self, window):
    # Create a new launcherbutton for the given window
    lb = Launcherbutton(window, len(self.launcher_list) + 1, self)
    self.launcher_list.append(lb)

  def UpdateStartbutton(self, mouse_event, mouse_button):
    # Update the startbutton based on the provided event
    self.startbutton.Update(mouse_event, mouse_button)
