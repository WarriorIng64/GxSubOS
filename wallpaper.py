import sys, pygame

default_path = "graphics/default_wallpaper.png"

class Wallpaper:
  def __init__(self, screen_size, path=default_path):
    self.image = pygame.image.load(path)
    self.image = pygame.transform.smoothscale(self.image, screen_size)
    self.image = self.image.convert()
    self.rect = self.image.get_rect()
    self.rect.topleft = (0, 0)
