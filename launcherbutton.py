import sys, pygame

image_normal = pygame.image.load("graphics/launcher_button.png")
image_active = pygame.image.load("graphics/launcher_button_active.png")

class Launcherbutton:
  image = None
  
  def __init__(self, window, number):
    self.image = image_normal
    self.rect = self.image.get_rect()
    self.window = window
    self.number = number
    self.rect.move_ip(0, 48 * number)
    self.new_y = 48 * number
  
  def Update(self, mouse_event, mouse_button, new_number):
    self.UpdateWindowStatus(mouse_event, mouse_button)
    self.UpdateImage()
    self.UpdateNumber(new_number)
  
  def UpdateImage(self):
    if self.window.has_focus:
      self.image = image_active
    else:
      self.image = image_normal
  
  def UpdatePosition(self):
    move_amount = -(self.rect.y - self.new_y) / 2
    if move_amount != 0:
      self.rect.move_ip(0, move_amount)

  def WindowWasClosed(self):
    # Return whether the associated window was closed
    return self.window == None or self.window.window_closed

  def UpdateNumber(self, new_number):
    self.number = new_number
    self.new_y = 48 * self.number

  def UpdateWindowStatus(self, mouse_event, mouse_button):
    if self.WindowWasClosed():
      return
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if mouse_button == 1 and self.rect.collidepoint(mouse_x, mouse_y):
        self.window.has_focus = True
    
