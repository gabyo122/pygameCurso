import pygame

from .config import *

class Platform(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface((width,40))
    self.image.fill(green2)

    self.rect = self.image.get_rect()
    self.rect.x = 0
    self.rect.y = height - 40