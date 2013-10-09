import sys, pygame
import glass

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
    self.rect = pygame.rect.Rect(0, 0, lw, screenh)
    self.launcher_surface = pygame.Surface((lw, screenh), pygame.SRCALPHA)
    if glass.enable_transparency:
      self.launcher_surface.fill(self.launcher_color)
      self.color_surface = pygame.Surface((lw, screenh), pygame.SRCALPHA)
      self.color_surface.fill(self.launcher_color)
    else:
      self.launcher_surface.fill(self.launcher_color_opaque)
  
  def update(self, screen):
    # Blur effect
    if glass.enable_transparency:
      glass.draw_background(screen, self.launcher_surface, self.rect)
      self.launcher_surface = glass.glass_blur(self.launcher_surface)
      self.launcher_surface.blit(self.color_surface, [0, 0, 0, 0])
    else:
      self.launcher_surface.fill(self.launcher_color_opaque)
