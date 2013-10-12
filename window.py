import sys, pygame
import glass

pygame.font.init()

titlebar_height = 24
titlebar_font = pygame.font.SysFont("Droid Sans", 20)

class Window:
  window_color = glass.glass_color
  window_color_opaque = glass.glass_color
  window_color.a = glass.glass_alpha
  
  def __init__(self, x, y, width, height, titlebar_text=''):
    self.width = width
    self.height = height
    
    self.rect = pygame.rect.Rect(x, y, x + width, y + height)
    self.close_image = pygame.image.load("graphics/close.png")
    self.close_rect = self.close_image.get_rect()
    
    self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
    self.window_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    self.background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    self.titlebar_text = titlebar_text
    self.being_dragged = False
    self.has_focus = True
    self.draw_window_surface()
    self.click_x, self.click_y = 0, 0
    self.window_closed = False
  
  def update(self, mouse_event, mouse_button):
    # Process mouse events first
    if mouse_event != None:
      mouse_x, mouse_y = mouse_event.pos
      if mouse_button == 1:
        if mouse_event.type == pygame.MOUSEBUTTONDOWN:
          if self.window_clicked(mouse_x, mouse_y):
            if self.titlebar_clicked(mouse_x, mouse_y):
              self.being_dragged = True
              self.click_x, self.click_y = mouse_x, mouse_y
          if self.close_button_clicked(mouse_x, mouse_y):
            self.window_closed = True
        elif mouse_event.type == pygame.MOUSEBUTTONUP:
          self.being_dragged = False
      
      # Window dragging
      if mouse_event.type == pygame.MOUSEMOTION and self.being_dragged:
        if self.has_focus:
          offset_x, offset_y = mouse_x - self.click_x, mouse_y - self.click_y
          self.move_by_amount(offset_x, offset_y)
          # Dragging limits
          if self.rect.y < 0:
            self.rect.y = 0
          if self.rect.y + titlebar_height > pygame.display.Info().current_h:
            self.rect.y = pygame.display.Info().current_h - titlebar_height
          self.click_x = mouse_x
          self.click_y = mouse_y
        else:
          self.being_dragged = False
  
  def redraw(self, screen):
    if glass.enable_transparency:
      glass.draw_background(screen, self.background_surface, self.rect)
      self.background_surface = glass.glass_blur(self.background_surface)
    else:
      self.background_surface.fill(self.window_color_opaque)
    self.surface.blit(self.background_surface, [0, 0, 0, 0])
    self.surface.blit(self.window_surface, [0, 0, 0, 0])
  
  def draw_titlebar(self):
    start_top = [0, titlebar_height]
    end_top = [self.width, titlebar_height]
    start_bottom = [0, self.height - titlebar_height]
    end_bottom = [self.width, self.height - titlebar_height]
    sep_color = glass.accent_color
    # Draw separator
    pygame.draw.line(self.window_surface, sep_color, start_top, end_top, 1)
    pygame.draw.line(self.window_surface, sep_color, start_bottom, end_bottom, 1)
    # Draw titlebar text
    text_surf = titlebar_font.render(self.titlebar_text, True, sep_color)
    text_surf.get_rect().x = self.rect.x + titlebar_height
    text_surf.get_rect().y = self.rect.y
    self.window_surface.blit(text_surf, [titlebar_height, 1, 0, 0])
  
  def move_by_amount(self, x, y):
    self.rect.move_ip(x, y)
  
  def close_button_clicked(self, x, y):
    close_x1, close_x2 = self.rect.x, self.rect.x + titlebar_height
    close_y1, close_y2 = self.rect.y, self.rect.y + titlebar_height
    return x > close_x1 and x < close_x2 and y > close_y1 and y < close_y2
  
  def titlebar_clicked(self, x, y):
    x1, x2 = self.rect.x, self.rect.x + self.width
    y1, y2 = self.rect.y, self.rect.y + titlebar_height
    top_titlebar_clicked = x1 < x < x2 and y1 < y < y2
    y1, y2 = self.rect.y + self.height - titlebar_height, self.rect.y + self.height
    bottom_titlebar_clicked = x1 < x < x2 and y1 < y < y2
    return top_titlebar_clicked or bottom_titlebar_clicked
  
  def window_clicked(self, x, y):
    x1, x2 = self.rect.x, self.rect.x + self.width
    y1, y2 = self.rect.y, self.rect.y + self.height
    return x > x1 and x < x2 and y > y1 and y < y2
  
  def draw_window_surface(self):
    # Draw the window chrome and prepare the window_surface for blitting
    w, h = self.width, self.height
    window_rect = self.window_surface.get_rect()
    self.window_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    if glass.enable_transparency:
      self.window_surface.fill(self.window_color)
    self.draw_titlebar()
    # Draw focus outline
    if self.has_focus:
      pygame.draw.rect(self.window_surface, glass.accent_color, window_rect, 1)
    self.window_surface.blit(self.close_image, self.close_rect)
  
  def set_focus(self, focus):
    if self.has_focus != focus:
      self.has_focus = focus
      self.draw_window_surface()
    else:
      self.has_focus = focus
