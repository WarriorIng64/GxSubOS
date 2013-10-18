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

shadow_width = shadow_t_image.get_height()

class Corner():
  TL, TR, BL, BR = range(4)

class Edge():
  T, L, R, B = range(4)

def DrawWindowShadowCorner(screen, window_rect, corner):
  offset = window.titlebar_height
  if corner == Corner.TL:
    shadow_image = shadow_tl_image
    pos = (window_rect.left - shadow_width, window_rect.top - shadow_width)
  elif corner == Corner.TR:
    shadow_image = shadow_tr_image
    pos = (window_rect.right - offset, window_rect.top - shadow_width)
  elif corner == Corner.BL:
    shadow_image = shadow_bl_image
    pos = (window_rect.left - shadow_width, window_rect.bottom - offset)
  else:
    shadow_image = shadow_br_image
    pos = (window_rect.right - offset, window_rect.bottom - offset)
  size = shadow_image.get_size()
  screen.blit(shadow_image, (pos, size))

def DrawWindowShadowEdge(screen, window_rect, edge):
  offset = window.titlebar_height
  if edge == Edge.T:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.top - shadow_width)
    shadow_image = pygame.transform.scale(shadow_t_image, shadow_size)
  elif edge == Edge.L:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.left - shadow_width, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_l_image, shadow_size)
  elif edge == Edge.R:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.right, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_r_image, shadow_size)
  else:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.bottom)
    shadow_image = pygame.transform.scale(shadow_b_image, shadow_size)
  screen.blit(shadow_image, pygame.Rect(shadow_pos, shadow_size))

def DrawFocusedWindowShadowCorner(screen, window_rect, corner):
  offset = window.titlebar_height
  if corner == Corner.TL:
    shadow_image = shadow_focused_tl_image
    pos = (window_rect.left - shadow_width, window_rect.top - shadow_width)
  elif corner == Corner.TR:
    shadow_image = shadow_focused_tr_image
    pos = (window_rect.right - offset, window_rect.top - shadow_width)
  elif corner == Corner.BL:
    shadow_image = shadow_focused_bl_image
    pos = (window_rect.left - shadow_width, window_rect.bottom - offset)
  else:
    shadow_image = shadow_focused_br_image
    pos = (window_rect.right - offset, window_rect.bottom - offset)
  size = shadow_image.get_size()
  screen.blit(shadow_image, (pos, size))

def DrawFocusedWindowShadowEdge(screen, window_rect, edge):
  offset = window.titlebar_height
  if edge == Edge.T:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.top - shadow_width)
    shadow_image = pygame.transform.scale(shadow_focused_t_image, shadow_size)
  elif edge == Edge.L:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.left - shadow_width, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_focused_l_image, shadow_size)
  elif edge == Edge.R:
    shadow_size = (shadow_width, window_rect.height - offset * 2)
    shadow_pos = (window_rect.right, window_rect.top + offset)
    shadow_image = pygame.transform.scale(shadow_focused_r_image, shadow_size)
  else:
    shadow_size = (window_rect.width - offset * 2, shadow_width)
    shadow_pos = (window_rect.left + offset, window_rect.bottom)
    shadow_image = pygame.transform.scale(shadow_focused_b_image, shadow_size)
  screen.blit(shadow_image, pygame.Rect(shadow_pos, shadow_size))

def DrawWindowShadow(screen, window_rect):
  DrawWindowShadowCorner(screen, window_rect, Corner.TL)
  DrawWindowShadowCorner(screen, window_rect, Corner.TR)
  DrawWindowShadowCorner(screen, window_rect, Corner.BL)
  DrawWindowShadowCorner(screen, window_rect, Corner.BR)
  DrawWindowShadowEdge(screen, window_rect, Edge.T)
  DrawWindowShadowEdge(screen, window_rect, Edge.L)
  DrawWindowShadowEdge(screen, window_rect, Edge.R)
  DrawWindowShadowEdge(screen, window_rect, Edge.B)

def DrawFocusedWindowShadow(screen, window_rect):
  DrawFocusedWindowShadowCorner(screen, window_rect, Corner.TL)
  DrawFocusedWindowShadowCorner(screen, window_rect, Corner.TR)
  DrawFocusedWindowShadowCorner(screen, window_rect, Corner.BL)
  DrawFocusedWindowShadowCorner(screen, window_rect, Corner.BR)
  DrawFocusedWindowShadowEdge(screen, window_rect, Edge.T)
  DrawFocusedWindowShadowEdge(screen, window_rect, Edge.L)
  DrawFocusedWindowShadowEdge(screen, window_rect, Edge.R)
  DrawFocusedWindowShadowEdge(screen, window_rect, Edge.B)
