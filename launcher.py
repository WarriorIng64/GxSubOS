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
    self.surface = pygame.Surface((lw, screenh), pygame.SRCALPHA)
    if glass.enable_transparency:
      self.surface.fill(self.launcher_color)
      self.color_surface = pygame.Surface((lw, screenh), pygame.SRCALPHA)
      self.color_surface.fill(self.launcher_color)
    else:
      self.surface.fill(self.launcher_color_opaque)
  
  def Update(self, screen):
    # Blur effect
    if glass.enable_transparency:
      glass.DrawBackground(screen, self.surface, self.rect)
      self.surface = glass.Blur(self.surface)
      self.surface.blit(self.color_surface, [0, 0, 0, 0])
    else:
      self.surface.fill(self.launcher_color_opaque)
