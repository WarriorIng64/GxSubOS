import pygame
import window

def LoadShadowImage(filename):
  shadow_path = "graphics/shadows/"
  return pygame.image.load(shadow_path + filename)

def LoadFocusedShadowImage(filename):
  shadow_path = "graphics/shadows/focused/"
  return pygame.image.load(shadow_path + filename)

shadow_tl_image = LoadShadowImage("topleft.png")
shadow_t_image = LoadShadowImage("top.png")
shadow_tr_image = LoadShadowImage("topright.png")
shadow_r_image = LoadShadowImage("right.png")
shadow_br_image = LoadShadowImage("bottomright.png")
shadow_b_image = LoadShadowImage("bottom.png")
shadow_bl_image = LoadShadowImage("bottomleft.png")
shadow_l_image = LoadShadowImage("left.png")

shadow_focused_tl_image = LoadFocusedShadowImage("topleft.png")
shadow_focused_t_image = LoadFocusedShadowImage("top.png")
shadow_focused_tr_image = LoadFocusedShadowImage("topright.png")
shadow_focused_r_image = LoadFocusedShadowImage("right.png")
shadow_focused_br_image = LoadFocusedShadowImage("bottomright.png")
shadow_focused_b_image = LoadFocusedShadowImage("bottom.png")
shadow_focused_bl_image = LoadFocusedShadowImage("bottomleft.png")
shadow_focused_l_image = LoadFocusedShadowImage("left.png")

class Corner():
  TL, TR, BL, BR = range(4)

class Edge():
  T, L, R, B = range(4)

def DrawWindowShadowCorner(screen, window_rect, corner):
  shadow_offset = window.titlebar_height / 2
  shadow_width = window.titlebar_height
  if corner == Corner.TL:
    screen.blit(shadow_tl_image, [window_rect.left - shadow_offset, window_rect.top - shadow_offset, shadow_width, shadow_width])
  elif corner == Corner.TR:
    screen.blit(shadow_tr_image, [window_rect.right - shadow_offset, window_rect.top - shadow_offset, shadow_width, shadow_width])
  elif corner == Corner.BL:
    screen.blit(shadow_bl_image, [window_rect.left - shadow_offset, window_rect.bottom - shadow_offset, shadow_width, shadow_width])
  else:
    screen.blit(shadow_br_image, [window_rect.right - shadow_offset, window_rect.bottom - shadow_offset, shadow_width, shadow_width])

def DrawWindowShadowEdge(screen, window_rect, edge):
  shadow_offset = window.titlebar_height / 2
  shadow_width = window.titlebar_height
  if edge == Edge.T:
    screen.blit(pygame.transform.scale(shadow_t_image, (window_rect.width - shadow_width, shadow_width)), [window_rect.left + shadow_offset, window_rect.top - shadow_offset, window_rect.width - shadow_width, shadow_width])
  elif edge == Edge.L:
    screen.blit(pygame.transform.scale(shadow_l_image, (shadow_width, window_rect.height - shadow_width)), [window_rect.left - shadow_offset, window_rect.top + shadow_offset, shadow_width, window_rect.height - shadow_width])
  elif edge == Edge.R:
    screen.blit(pygame.transform.scale(shadow_r_image, (shadow_width, window_rect.height - shadow_width)), [window_rect.right - shadow_offset, window_rect.top + shadow_offset, shadow_width, window_rect.height - shadow_width])
  else:
    screen.blit(pygame.transform.scale(shadow_b_image, (window_rect.width - shadow_width, shadow_width)), [window_rect.left + shadow_offset, window_rect.bottom - shadow_offset, window_rect.width - shadow_width, shadow_width])

def DrawWindowShadow(screen, window_rect):
  # Draw a shadow around the given window area
  
  # Corners
  DrawWindowShadowCorner(screen, window_rect, Corner.TL)
  DrawWindowShadowCorner(screen, window_rect, Corner.TR)
  DrawWindowShadowCorner(screen, window_rect, Corner.BL)
  DrawWindowShadowCorner(screen, window_rect, Corner.BR)
  # Edges
  DrawWindowShadowEdge(screen, window_rect, Edge.T)
  DrawWindowShadowEdge(screen, window_rect, Edge.L)
  DrawWindowShadowEdge(screen, window_rect, Edge.R)
  DrawWindowShadowEdge(screen, window_rect, Edge.B)

def DrawFocusedWindowShadow(screen, window_rect):
  # Draw a shadow around the given window area for a focused window
  shadow_offset = window.titlebar_height / 2
  shadow_width = window.titlebar_height
  # Corners
  screen.blit(shadow_focused_tl_image, [window_rect.left - shadow_offset, window_rect.top - shadow_offset, shadow_width, shadow_width])
  screen.blit(shadow_focused_tr_image, [window_rect.right - shadow_offset, window_rect.top - shadow_offset, shadow_width, shadow_width])
  screen.blit(shadow_focused_bl_image, [window_rect.left - shadow_offset, window_rect.bottom - shadow_offset, shadow_width, shadow_width])
  screen.blit(shadow_focused_br_image, [window_rect.right - shadow_offset, window_rect.bottom - shadow_offset, shadow_width, shadow_width])
  # Edges
  screen.blit(pygame.transform.scale(shadow_focused_t_image, (window_rect.width - shadow_width, shadow_width)), [window_rect.left + shadow_offset, window_rect.top - shadow_offset, window_rect.width - shadow_width, shadow_width])
  screen.blit(pygame.transform.scale(shadow_focused_l_image, (shadow_width, window_rect.height - shadow_width)), [window_rect.left - shadow_offset, window_rect.top + shadow_offset, shadow_width, window_rect.height - shadow_width])
  screen.blit(pygame.transform.scale(shadow_focused_r_image, (shadow_width, window_rect.height - shadow_width)), [window_rect.right - shadow_offset, window_rect.top + shadow_offset, shadow_width, window_rect.height - shadow_width])
  screen.blit(pygame.transform.scale(shadow_focused_b_image, (window_rect.width - shadow_width, shadow_width)), [window_rect.left + shadow_offset, window_rect.bottom - shadow_offset, window_rect.width - shadow_width, shadow_width])