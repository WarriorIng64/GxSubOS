import pygame

glass_blur_amount = 5
glass_color = pygame.color.Color(5, 30, 30)
content_area_color = pygame.color.Color(20, 50, 50)
highlight_color = 0, 255, 255
glass_alpha = 200
accent_color = pygame.color.Color(0, 255, 255)
enable_blur = True
enable_transparency = True

def Blur(surface):
  if not enable_blur:
    return surface
  size = surface.get_size()
  for i in range(glass_blur_amount):
    surface2 = pygame.transform.smoothscale(surface,(size[0]/2,size[1]/2))
    surface2 = pygame.transform.smoothscale(surface2,size)
    surface2 = pygame.transform.average_surfaces([surface,surface2])
    surface = pygame.transform.smoothscale(surface2,size)
  return surface

def DrawBackground(screen, surface, rect):
  # Draws the screen onto the given surface with an offset
  offset_rect = screen.get_rect().move(-rect.x, -rect.y)
  surface.blit(screen, offset_rect)

def UpdateBlurredDesktopSurface(blurred_desktop_surface, desktop_surface):
  if enable_blur:
    blurred_desktop_surface = Blur(desktop_surface)
  else:
    blurred_desktop_surface = None
