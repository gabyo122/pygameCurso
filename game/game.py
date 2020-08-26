import sys
import pygame
import random
import os 

from .config import *
from .platform import Platform
from .player import Player
from .wall import Wall
from .coin import Coin

clock = pygame.time.Clock()

class Game:
  def __init__(self):
    pygame.init()

    self.surface = pygame.display.set_mode((width,height))
    pygame.display.set_caption(title)

    self.running = True
    
    self.clock = pygame.time.Clock()

    self.font = pygame.font.match_font(font)

    self.dir = os.path.dirname(__file__)
    self.dir_sounds = os.path.join(self.dir, "source/sounds")
    self.dir_images = os.path.join(self.dir, "source/sprites")

  #iniciar juego
  def start(self):
    self.menu()
    self.new()

  #generar un nuevo juego
  def new(self):
    self.score = 0
    self.level = 0
    self.playing = True
    self.background = pygame.image.load(os.path.join(self.dir_images, "background.png"))

    self.generate_elements()
    self.run()

  def generate_elements(self):
    self.platform = Platform()
    self.player = Player(100, self.platform.rect.top, self.dir_images)

    self.sprites = pygame.sprite.Group()
    self.walls = pygame.sprite.Group()
    self.coins = pygame.sprite.Group()
    
    self.sprites.add(self.platform)
    self.sprites.add(self.player)

    self.generate_walls()

  def generate_walls(self):

    last_position = width + 100

    if not len(self.walls) > 0:
      for w in range(0, max_walls):

        left = random.randrange(last_position + 200, last_position + 400)
        wall = Wall(left, self.platform.rect.top, self.dir_images)

        last_position = wall.rect.right

        self.sprites.add(wall)
        self.walls.add(wall)

      self.level += 1
      self.generate_coins()

  def generate_coins(self):
    last_position = width + 100

    for c in range(0, max_coins):
      pos_x = random.randrange(last_position + 180, last_position + 300)

      coin = Coin(pos_x, 100, self.dir_images)

      last_position = coin.rect.right

      self.sprites.add(coin)
      self.coins.add(coin)

  #ejecutar el juego
  def run(self):
    while self.running:
      self.clock.tick(fps)
      self.events()
      self.update()
      self.draw()
  
  def events(self):
    clock.tick(fps)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
        pygame.quit()
        sys.exit()

    key = pygame.key.get_pressed()
    
    if key[pygame.K_SPACE]:
      self.player.jump() 

    if key[pygame.K_r]:
      self.new()  

  #pintar elementos del juego
  def draw(self):
    self.surface.blit(self.background, (0,0))
    self.sprites.draw(self.surface)
    self.draw_text()
    pygame.display.flip()

  #actualizar pantalla
  def update(self):
    if not self.playing:
      return      
     
    wall = self.player.collide_with(self.walls)
    if wall:
      if self.player.collide_bottom(wall):
        self.player.skid(wall)
      else:
        self.stop()

    coin = self.player.collide_with(self.coins)
    if coin:
      self.score += 1
      coin.kill()

      #sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, "coin.wav"))
      #sound.play()

    self.sprites.update()

    self.player.validate_platform(self.platform)

    self.update_elements(self.walls)

    self.generate_walls()

  def update_elements(self, elements):
    for element in elements:
      if not element.rect.right > 0:
        element.kill()

  #detener juego
  def stop(self):
    #sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, "lose.wav"))
    #sound.play()

    self.player.stop()
    self.stop_elements(self.walls)
    self.playing = False

  def stop_elements(self, elements):
    for element in elements:
      element.stop()

  def score_format(self):
    return 'Score : {}'.format(self.score)

  def level_format(self):
    return 'level : {}'.format(self.level)


  def draw_text(self):
    self.display_text(self.score_format(), 30, black, 700, text_posy)
    self.display_text(self.level_format(), 30, black, 100, text_posy)

    if not self.playing:
      self.display_text("perdiste", 60, black, width // 2, height // 2)
      self.display_text("presiona r para comenzar de nuevo", 20, black, width // 2, 100)
  
  def display_text(self, text, size,color, pos_x, pos_y):
    font = pygame.font.Font(self.font, size)

    text = font.render(text, True, color)
    rect = text.get_rect()
    rect.midtop = (pos_x, pos_y)

    self.surface.blit(text, rect)

  def menu(self):
    self.surface.fill(black)
    self.display_text("presiona una tecla para comenzar", 40, pink, width // 2, 100)

    pygame.display.flip()
    self.wait()

  def wait(self):
    wait = True

    while wait:
      self.clock.tick(fps)
    
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          wait = False
          self.running = False
          pygame.quit()
          sys.exit()

        if event.type == pygame.KEYUP:
          wait = False