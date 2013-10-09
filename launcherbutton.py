import sys, pygame

class Launcherbutton:
  image = None
  
  def __init__(self, window, number):
    self.image_normal = pygame.image.load("graphics/launcher_button.png")
    self.image_active = pygame.image.load("graphics/launcher_button_active.png")
    self.image = self.image_normal
    self.rect = self.image.get_rect()
    self.window = window
    self.window_closed = False
    self.number = number
    self.rect.move_ip(0, 48 * number)
    self.new_y = 48 * number
  
  def update(self, mouse_event, mouse_button, new_number):
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if mouse_button == 1 and self.rect.collidepoint(mouse_x, mouse_y):
        # Bring focus to this window
        self.window.has_focus = True
    self.update_image()
    # Check if the window was closed
    if self.window == None or self.window.window_closed:
      self.window_closed = True
    # Update number
    self.number = new_number
    self.new_y = 48 * self.number
  
  def update_image(self):
    if self.window.has_focus:
      self.image = self.image_active
    else:
      self.image = self.image_normal
  
  def update_position(self):
    move_amount = -(self.rect.y - self.new_y) / 2
    if move_amount != 0:
      self.rect.move_ip(0, move_amount)
