import sys, pygame

class Startbutton:
  image = None
  
  def __init__(self):
    self.image = pygame.image.load("graphics/start.png")
    self.rect = self.image.get_rect()
  
  def update(self, mouse_event, mouse_button):
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if mouse_button == 1 and self.rect.collidepoint(mouse_x, mouse_y):
        # Act as a quit button for now
        pygame.quit()
        sys.exit()
