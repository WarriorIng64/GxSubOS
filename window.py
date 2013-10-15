import sys, pygame
import glass

pygame.font.init()

titlebar_height = 24
titlebar_font = pygame.font.SysFont("Droid Sans", 20)

class Window:
  window_color = glass.glass_color
  window_color_opaque = glass.glass_color
  window_color.a = glass.glass_alpha
  content_color = glass.content_area_color
  content_color_opaque = glass.content_area_color
  content_color.a = glass.glass_alpha
  
  def __init__(self, x, y, width, height, titlebar_text=''):
    self.rect = pygame.rect.Rect(x, y, width, height)
    self.close_image = pygame.image.load("graphics/close.png")
    self.resize_image = pygame.image.load("graphics/resize.png")
    self.close_rect = self.close_image.get_rect()
    self.resize_rect = self.resize_image.get_rect()
    self.resize_rect.move_ip(width - titlebar_height, height - titlebar_height)
    
    self.create_surfaces(width, height)
    self.titlebar_text = titlebar_text
    self.being_dragged = False
    self.being_resized = False
    self.is_maximized = False
    self.restore_rect = self.rect
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
          if self.close_button_clicked(mouse_x, mouse_y):
            self.window_closed = True
          elif self.resize_button_clicked(mouse_x, mouse_y):
            self.being_resized = True
            self.click_x, self.click_y = mouse_x, mouse_y
          elif self.titlebar_clicked(mouse_x, mouse_y):
            self.being_dragged = True
            self.click_x, self.click_y = mouse_x, mouse_y
        elif mouse_event.type == pygame.MOUSEBUTTONUP:
          if self.being_dragged:
            if mouse_y <= 5 and not self.is_maximized:
              self.maximize()
            else:
              self.unmaximize()
          self.being_dragged = False
          self.being_resized = False
      
      # Window dragging and resizing
      if mouse_event.type == pygame.MOUSEMOTION:
        if self.being_dragged:
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
        elif self.being_resized:
          if self.has_focus:
            offset_x, offset_y = mouse_x - self.click_x, mouse_y - self.click_y
            self.resize(self.rect.width + offset_x, self.rect.height + offset_y)
            self.click_x = mouse_x
            self.click_y = mouse_y
          else:
            self.being_resized = False
  
  def redraw(self, screen):
    if glass.enable_transparency:
      glass.draw_background(screen, self.background_surface, self.rect)
      self.background_surface = glass.glass_blur(self.background_surface)
    else:
      self.background_surface.fill(self.window_color_opaque)
    self.surface.blit(self.background_surface, [0, 0, 0, 0])
    self.surface.blit(self.window_surface, [0, 0, 0, 0])
  
  def draw_titlebar_separator(self, surface, upper):
    if upper:
      height = titlebar_height
    else:
      height = self.rect.height - titlebar_height
    sep_color_top = pygame.Color(0, 0, 0, 20)
    sep_color_bottom = pygame.Color(255, 255, 255, 20)
    start_top, end_top = [0, height], [self.rect.width, height]
    start_bottom, end_bottom = [0, height + 1], [self.rect.width, height + 1]
    
    pygame.draw.line(surface, sep_color_top, start_top, end_top, 1)
    pygame.draw.line(surface, sep_color_bottom, start_bottom, end_bottom, 1)
  
  def draw_titlebar_separators(self):
    separator_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    self.draw_titlebar_separator(separator_surface, True)
    self.draw_titlebar_separator(separator_surface, False)
    self.window_surface.blit(separator_surface, [0, 0, 0, 0])
  
  def draw_titlebar(self):
    # Draw titlebar background
    pygame.draw.rect(self.window_surface, glass.glass_color, [0, 0, self.rect.width, titlebar_height])
    pygame.draw.rect(self.window_surface, glass.glass_color, [0, self.rect.height - titlebar_height, self.rect.width, titlebar_height])
    # Draw separators
    self.draw_titlebar_separators()
    # Draw titlebar text
    text_surf = titlebar_font.render(self.titlebar_text, True, glass.accent_color)
    text_surf.get_rect().x = self.rect.x + titlebar_height
    text_surf.get_rect().y = self.rect.y
    self.window_surface.blit(text_surf, [titlebar_height, 1, 0, 0])
  
  def move_by_amount(self, x, y):
    self.rect.move_ip(x, y)
  
  def close_button_clicked(self, x, y):
    close_x1, close_x2 = self.rect.left, self.rect.left + titlebar_height
    close_y1, close_y2 = self.rect.top, self.rect.top + titlebar_height
    return close_x1 < x < close_x2 and close_y1 < y < close_y2
  
  def resize_button_clicked(self, x, y):
    # Do not resize maximized windows
    if self.is_maximized:
      return False
    resize_x1 = self.rect.x + self.rect.width - titlebar_height
    resize_x2 = self.rect.x + self.rect.width
    resize_y1 = self.rect.y + self.rect.height - titlebar_height
    resize_y2 = self.rect.y + self.rect.height
    return resize_x1 < x < resize_x2 and resize_y1 < y < resize_y2
  
  def titlebar_clicked(self, x, y):
    x1, x2 = self.rect.left, self.rect.right
    y1, y2 = self.rect.top, self.rect.top + titlebar_height
    top_titlebar_clicked = x1 < x < x2 and y1 < y < y2
    y1, y2 = self.rect.bottom - titlebar_height, self.rect.bottom
    bottom_titlebar_clicked = x1 < x < x2 and y1 < y < y2
    return top_titlebar_clicked or bottom_titlebar_clicked
  
  def window_clicked(self, x, y):
    x1, x2 = self.rect.left, self.rect.right
    y1, y2 = self.rect.top, self.rect.bottom
    return x1 < x < x2 and y1 < y < y2
  
  def draw_window_surface(self):
    # Draw the window chrome and prepare the window_surface for blitting
    w, h = self.rect.width, self.rect.height
    window_rect = self.window_surface.get_rect()
    self.window_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(self.window_surface, glass.content_area_color, [0, titlebar_height, self.rect.width, self.rect.height - 2 * titlebar_height])
    self.draw_titlebar()
    self.window_surface.blit(self.close_image, self.close_rect)
    if not self.is_maximized:
      self.window_surface.blit(self.resize_image, self.resize_rect)
    self.window_surface.convert_alpha()
  
  def set_focus(self, focus):
    if self.has_focus != focus:
      self.has_focus = focus
      self.draw_window_surface()
    else:
      self.has_focus = focus
  
  def resize(self, new_width, new_height):
    correct_width = max(new_width, titlebar_height * 2)
    correct_height = max(new_height, titlebar_height * 2)
    x, y = self.rect.x, self.rect.y
    self.rect = pygame.rect.Rect(x, y, correct_width, correct_height)
    self.create_surfaces(correct_width, correct_height)
    self.draw_window_surface()
    self.resize_rect = self.resize_image.get_rect()
    self.resize_rect.move_ip(correct_width - titlebar_height, correct_height - titlebar_height)
  
  def create_surfaces(self, w, h):
    self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
    self.window_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    self.background_surface = pygame.Surface((w, h), pygame.SRCALPHA)
  
  def maximize(self):
    self.restore_rect = self.rect
    maximized_width = pygame.display.Info().current_w - 48
    maximized_height = pygame.display.Info().current_h
    self.rect.x = 48 # Replace this later with a variable for desktop size
    self.rect.y = 0
    self.resize(maximized_width, maximized_height)
    self.draw_window_surface()
    self.is_maximized = True
  
  def unmaximize(self):
    if self.is_maximized:
      self.rect.x = self.restore_rect.x
      self.rect.y = self.restore_rect.y
      self.resize(self.restore_rect.width, self.restore_rect.height)
      self.draw_window_surface()
      self.is_maximized = False
