import pygame

from pygame.locals import *
from array import *
from abc import ABC, abstractmethod
#Mason Armstrong Assignment 8 - Python Mario Game


class Sprite(ABC):
    def __init__(self, x, y, image) -> None:
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.px = 0
        self.py = 0
        self.timeInAir = 0
        self.time = None
        self.vertVelocity = 3.2
        self.onPipeTop = False
        self.onGround = False
        self.bounceCount = 0

    def isPipe():
        return False

    def isFireball():
        return False

    def isMario():
        return False

    def isGoomba():
        return False
    def isGround():
        return False

    def setPreviousPosition(self):
        self.px = self.rect.x
        self.py = self.rect.y

    def gravity(self):
        if self.onPipeTop:
            self.vertVelocity = 0
        if self.onGround:
            self.vertVelocity = 0
        self.vertVelocity += 3.2
        self.rect.y += self.vertVelocity
        self.timeInAir += 1  

    @abstractmethod
    def update(self):
      pass
  
    def draw(self, screen, scrollX):
        screen.blit(
                    self.image, (self.rect.left - scrollX, self.rect.top)
                )

    def collisionHandler(self, sprite):
        if not isinstance(sprite, (Ground, Pipe, Mushroom, Goomba)):
            if pygame.Rect.colliderect(self.rect, sprite.rect):
                sprite.rect.y = self.rect.top - sprite.rect.height
                sprite.timeInAir = 0
                sprite.vertVelocity = 0      

class Pipe(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def isPipe():
        return 1

    def update(self):
        pass
    
    def collisionHandler(self, sprite):
        pass

class Mario(Sprite):
    def __init__(self, x, y, image) -> None:
        super().__init__(x, y, image)
        self.currentImage = 0
        self.mario_images = [
            pygame.image.load("mario1.png"),
            pygame.image.load("mario2.png"),
            pygame.image.load("mario3.png"),
            pygame.image.load("mario4.png"),
            pygame.image.load("mario5.png"),
        ]
        self.onPipeTop = False
        self.canShootBall = True
        self.timeInAir = 0
        self.isDead = False
        self.movingRight = True

    def isMario():
        return 1
#wfeef
    def jump(self):
        self.timeInAir += 1
        if self.timeInAir < 50:
            self.rect.y -= 30
        if self.onPipeTop and self.timeInAir < 50:
            self.rect.y -= 30

    def changeImage(self, movingRight):
        self.movingRight = movingRight
        self.currentImage += 1
        if self.currentImage > 4:
            self.currentImage = 0
        if movingRight == False:
            self.image = self.mario_images[self.currentImage]
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.mario_images[self.currentImage]
            
    def update(self):
        self.gravity()        
        pass
    def collisionHandler(self, sprite):
        self.onPipeTop = False
        self.onGround = False

        if self.py >= sprite.rect.top + sprite.rect.y:
            self.rect.top = sprite.rect.top - sprite.rect.y
            
        if self.py + self.rect.height <= sprite.rect.top:
            self.rect.top = sprite.rect.top - self.rect.height
            self.onPipeTop = True
            self.timeInAir = 0
            return
            
        if (self.px + self.rect.width <= sprite.rect.left) and (
            self.rect.right > sprite.rect.left
        ):
            self.rect.left = sprite.rect.left - self.rect.width
            return
        if (self.px >= sprite.rect.left + sprite.rect.width) and (
            self.rect.left < sprite.rect.left + sprite.rect.width
        ):
            self.rect.left = sprite.rect.left + sprite.rect.width
            return
    
class Goomba(Sprite):
    def __init__(self, x, y, image) -> None:
        super().__init__(x, y, image)
        self.currentImage = 0
        self.goomba_images = [
            pygame.image.load("goomba.png"),
            pygame.image.load("goomba_fire.png"),
        ]
        self.image = self.goomba_images[self.currentImage]
        self.Alive = True
        self.moveRight = False

    def isGoomba():
        return 1

    def goombaDie(self):
        self.currentImage = 1
        self.Alive = False

    def collisionHandler(self, sprite):            
        if self.py >= sprite.rect.top + sprite.rect.y:
            self.rect.top = sprite.rect.top - sprite.rect.y                  
            
        if self.py + self.rect.height <= sprite.rect.top:
            self.rect.top = sprite.rect.top - self.rect.height
            self.onPipeTop = True
            self.timeInAir = 0
            return
                   
        if (self.px + self.rect.width <= sprite.rect.left) and (
            self.rect.right > sprite.rect.left
        ):
            if sprite.isFireball == 1:
                self.Alive = False
                self.image = self.goomba_images[1]
                self.time = pygame.time.get_ticks()

            self.rect.left = sprite.rect.left - self.rect.width
            self.moveRight = False
            return

        if (self.px >= sprite.rect.left + sprite.rect.width) and (
            self.rect.left < sprite.rect.left + sprite.rect.width
        ):
            self.rect.left = sprite.rect.left + sprite.rect.width
            self.moveRight = True
            
            if sprite.isFireball == 1:
                self.Alive = False
                self.image = self.goomba_images[1]
                self.time = pygame.time.get_ticks()
            return

        if sprite.rect.top <= self.rect.bottom:
            self.timeInAir = 0
            if sprite.isFireball == 1:
                self.Alive = False
                self.image = self.goomba_images[1]
                self.time = pygame.time.get_ticks()         

    def update(self):
        self.setPreviousPosition()
        if self.Alive:
            if self.moveRight:
                self.rect.x += 3
            else:
                self.rect.x -= 3
        self.gravity()
       
    def goombaDie(self):
        self.Alive = False
        self.currentImage = 1


class Fireball(Sprite):
    def __init__(self, x, y, image) -> None:
        super().__init__(x, y, image)
        self.rightFacing = True
        self.bounceCount = 0
        self.time = pygame.time.get_ticks()
        self.Alive = True
        self.isFireball = True

    def isFireball():
        return True
    
    def update(self):
        self.setPreviousPosition()
        self.gravity()
        self.timeInAir += 1
        if self.rightFacing:
            self.rect.x += 5
        else:
            self.rect.x -= 5
        if self.timeInAir < 10:
            self.rect.y -= 10
        if self.vertVelocity == 0:
            self.rect.y -= 10
            self.bounceCount += 1
        self.vertVelocity -= 2.5
        
    def collisionHandler(self, sprite):
        pass   
        
class Ground(Sprite):
    def __init__(self, x, y, image) -> None:
        super().__init__(x, y, image)        
      #  pygame.transform.scale(image,(0,20))
        self.rect.x = self.rect.centerx - 200 
        self.rect.top = self.rect.centery + 575     
        self.groundBlock = pygame.image.load("Groundblock.png")
        self.groundRect = self.groundBlock.get_rect()
        self.surface = pygame.Surface((self.groundRect.width, self.groundRect.height))
        self.surface.fill((255,0,0))
        self.groundArr = []
        
    def update(self):
        pass 
    def isGround():
        return True    
    
    #def draw(self, screen, scrollX):


       # screen.blit(self.image, (self.rect.x - scrollX, self.rect.y))     

        
    
class Mushroom(Sprite):
    def __init__(self, x, y, image) -> None:
        super().__init__(x, y, image)
        self.rect.y = self.rect.centery + 50
        self.yDir = 1 
    def update(self):
        self.rect.y += 2 * self.yDir
        if self.rect.y + self.rect.h > 700:
            self.yDir *= -1
        if self.rect.y  < 10:
            self.yDir *= -1

    def isGround():
         return True    
     
class Model:
    def __init__(self):
        self.spriteList = []
        self.mario = Mario(50, 10, "mario1.png")
        self.p1 = Pipe(350, 350, "pipe.png")
        self.p2 = Pipe(250, 400, "pipe.png")
        self.p3 = Pipe(450, 300, "pipe.png")
        self.p4 = Pipe(740, 350, "pipe.png")
        self.p5 = Pipe(740, 350, "pipe.png")
        self.p6 = Pipe(900, 450, "pipe.png")

        self.g1 = Goomba(550, 50, "goomba.png")
        self.g2 = Goomba(850, 50, "goomba.png")
        self.g3 = Goomba(900, 0, "goomba.png")
        
        self.ground = Ground(0, 0, "ground.png")
        self.mushroom = Mushroom(-5, 50, "mushroom_platform.png")
        
        self.spriteList = [self.mario, self.g1, self.g2, self.g3 ]
        self.pipeList = [ self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ground, self.mushroom]
        for pipe in self.pipeList:
            self.spriteList.append(pipe)
            
        self.playerDead = self.mario.isDead

    def shootFireball(self):
        ball = Fireball(self.mario.rect.x, self.mario.rect.y, "fireball.png")
        self.spriteList.append(ball)
        
    def generateGround(self):
        pass

    def update(self):    
        if self.mario.rect.y > 1500:
            self.playerDead = True    
        for sprite in self.spriteList:
            sprite.update()
            if(pygame.Rect.colliderect(sprite.rect, self.ground.rect)):
                self.ground.collisionHandler(sprite)
            
            marioPipeCheck = self.mario.rect.colliderect(sprite.rect)
            if marioPipeCheck:
                self.mario.collisionHandler(sprite)
            if sprite.isGoomba:
                g = sprite
                for pipe in self.spriteList:
                    goombaPipeCheck = g.rect.colliderect(pipe.rect)
                    if goombaPipeCheck:
                        
                        g.collisionHandler(pipe)
                #Check goomba death time
                if g.time is not None:
                    if pygame.time.get_ticks() - g.time >= 500:
                        self.spriteList.remove(g)
                
class View:
    def __init__(self, model):
        global SCREEN_WIDTH
        SCREEN_WIDTH = 1280
        global SCREEN_HEIGHT
        SCREEN_HEIGHT = 720 
        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size, 32)
        self.model = model
        self.viewScroll = 0
        self.backgroundImage = pygame.image.load("backgroundImage.png")
        self.death_screen = pygame.image.load("death_screen.png")
        self.scrollX = 0
        self.backgroundImage =  pygame.transform.scale(self.backgroundImage, (self.screen_size))     

    def update(self):
        if self.model.playerDead == True:
             self.screen.blit(self.backgroundImage, (self.screen_size))
             self.screen.blit(self.death_screen, (100,80) )
             pygame.display.flip()
        else:
            self.scrollX = self.model.mario.rect.x - 50
            self.screen.fill([9, 155, 196,1])
            self.screen.blit(self.backgroundImage, (0, 20))
          #  for sprite in self.model.spriteList:
            #    self.screen.blit(
            #       sprite.image, (sprite.rect.left - self.scrollX, sprite.rect.top)
             #   )
            for sprite in self.model.spriteList:
                sprite.draw(self.screen, self.scrollX)  
        pygame.display.flip()

class Controller:
    def __init__(self, model):
        self.model = model
        self.keep_going = True
        
    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
            elif event.type == KEYUP:
                if event.key == K_LCTRL:
                    self.model.mario.canShootBall = True
        self.model.mario.setPreviousPosition()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.model.mario.rect.x -= 5
            self.model.mario.changeImage(False)
        if keys[K_RIGHT]:
            self.model.mario.rect.x += 5
            self.model.mario.changeImage(True)
        if keys[K_SPACE]:
            self.model.mario.timeInAir += 1
            self.model.mario.jump()
        if keys[K_LCTRL] and self.model.mario.canShootBall:
            self.model.shootFireball()
            self.model.mario.canShootBall = False

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
clock = pygame.time.Clock()
m = Model()
v = View(m)
c = Controller(m)

while c.keep_going:
    c.update()
    m.update()
    v.update()
    clock.tick(60)
print("Goodbye")
