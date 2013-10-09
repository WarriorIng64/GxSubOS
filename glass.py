import pygame

glass_blur_amount = 2
glass_color = pygame.color.Color(10, 40, 40)
highlight_color = 0, 255, 255
glass_alpha = 200
accent_color = pygame.color.Color(0, 255, 255)
enable_blur = False
enable_transparency = False

def glass_blur(surface):
  if not enable_blur:
    return surface
  size = surface.get_size()
  for i in range(glass_blur_amount):
    surface2 = pygame.transform.smoothscale(surface,(size[0]/4,size[1]/4))
    surface2 = pygame.transform.smoothscale(surface2,size)
    surface2 = pygame.transform.average_surfaces([surface,surface2])
    surface = pygame.transform.smoothscale(surface2,size)
  return surface

def draw_background(screen, surface, rect):
  surface.blit(screen, screen.get_rect().move(-rect.x, -rect.y))
