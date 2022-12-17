import pygame

from pygame.locals import *
from abc import ABC, abstractmethod


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
        
        if self.rect.y >= 600 - self.rect.height:        
            self.rect.bottom = 600 - self.rect.height
            self.vertVelocity = 0
            self.timeInAir = 0

    @abstractmethod
    def update(self):
        pass

    def collisionHandler(self, sprite):
        pass


class Pipe(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def isPipe():
        return 1

    def update(self):
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

    def isMario():
        return 1

    def jump(self):
        self.timeInAir += 1
        if self.timeInAir < 50:
            self.rect.y -= 30
        if self.onPipeTop and self.timeInAir < 50:
            self.rect.y -= 30

    def changeImage(self):
        self.currentImage += 1
        if self.currentImage > 4:
            self.currentImage = 0
        self.image = self.mario_images[self.currentImage]

    def update(self):
        self.gravity()

    def collisionHandler(self, sprite):
        self.onPipeTop = False
        self.onGround = False
     #   if sprite.isGround == 1:
     #       self.onGround = True
      #      return
            
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
        if sprite.rect.top <= self.rect.bottom:
            self.timeInAir = 0
        if self.py + self.rect.height <= sprite.rect.top:
            self.rect.top = sprite.rect.top - self.rect.height
            self.onPipeTop = True
            if(sprite.isGround == True):
                self.onGround = True
            self.timeInAir = 0
            return
        if self.py >= sprite.rect.top + sprite.rect.height:
            self.rect.top = sprite.rect.top + sprite.rect.height
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

        if self.py + self.rect.height <= sprite.rect.top:
            if(sprite.isGround == True):
                self.onGround = True
            self.timeInAir = 0
            self.rect.top = sprite.rect.top - self.rect.height

            return
            
        if self.py >= sprite.rect.top + sprite.rect.height:
            self.rect.top = sprite.rect.top + sprite.rect.height
            
            return

    def update(self):
        self.gravity()
        self.setPreviousPosition()
       # print(self.rect)
        if self.Alive:
            if self.moveRight:
                self.rect.x += 3
            else:
                self.rect.x -= 3
        
       
       
    def goombaDie(self):
        self.Alive = False
        self.currentImage = 1


class Fireball(Sprite):
    def __init__(self, x, y, image) -> None:
        super().__init__(x, y, image)

        self.rightFacing = True
        self.bounceCount = 0
        self.isFireball = 1
        self.time = pygame.time.get_ticks()
        self.Alive = True

    def update(self):
        self.setPreviousPosition()
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
        self.gravity()
        
class Ground(Sprite):
    def __init__(self, x, y, image) -> None:
        super().__init__(x, y, image)
        
        self.currentImage = 0
        self.ground_images = [
            pygame.image.load("1280ground.png"),
            pygame.image.load("ground3.png"),
        ]
        self.image = self.ground_images[self.currentImage]
        
        self.outline = pygame.transform.laplacian(self.ground_images[self.currentImage])
        self.rect = self.outline.get_rect()
        self.rect.x = self.rect.centerx - 844 
        self.rect.y = self.rect.centery + 499
        
        
        
    def update(self):
        print(self.rect)
        pass
       
    def isGround():
        return True
    
    def collisionHandler(self, sprite):
        return super().collisionHandler(sprite)
    
    
    
    

class Model:
    def __init__(self):
        self.spriteList = []
        self.mario = Mario(0, 0, "mario1.png")

        self.p1 = Pipe(120, 500, "pipe.png")
        self.p2 = Pipe(270, 400, "pipe.png")
        self.p3 = Pipe(400, 300, "pipe.png")
        self.p4 = Pipe(520, 380, "pipe.png")
        self.p5 = Pipe(690, 480, "pipe.png")
        self.p6 = Pipe(800, 450, "pipe.png")

        self.g1 = Goomba(250, 250, "goomba.png")
        self.g2 = Goomba(800, 15, "goomba.png")
        self.ground = Ground(0, 0, "1280ground.png")
        
        self.spriteList = [  self.mario, self.g1, self.g2 ]
        self.pipeList = [ self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ground]
        for pipe in self.pipeList:
            self.spriteList.append(pipe)


    def shootFireball(self):
        ball = Fireball(self.mario.rect.x, self.mario.rect.y, "fireball.png")
        self.spriteList.append(ball)

    def update(self):

        for sprite in self.spriteList:
            sprite.update()
            marioPipeCheck = self.mario.rect.colliderect(sprite.rect)
            if marioPipeCheck:
                self.mario.collisionHandler(sprite)
            if sprite.isGoomba:
                g = sprite
                for pipe in self.spriteList:
                    goombaPipeCheck = g.rect.colliderect(pipe.rect)
                    if goombaPipeCheck:
                        print(goombaPipeCheck)
                        g.collisionHandler(pipe)
                #Check goomba death time
                if g.time is not None:
                    if pygame.time.get_ticks() - g.time >= 500:
                        self.spriteList.remove(g)
            if sprite.isFireball:
                b = sprite
                if b.time is not None:
                    if pygame.time.get_ticks() - g.time >= 1500:
                        self.spriteList.remove(b)


class View:
    def __init__(self, model):

        global SCREEN_WIDTH
        SCREEN_WIDTH = 1280
        global SCREEN_HEIGHT
        SCREEN_HEIGHT = 720
        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size, 32)
        self.model = model
     #   self.currentGroundImage = 0
        self.viewScroll = 0

     #   self.ground_images = [
      #      pygame.image.load("1280ground.png"),
     #       pygame.image.load("ground3.png"),
     #   ]
      #  self.ground_image = self.ground_images[0]
        self.backgroundImage = pygame.image.load("backgroundImage.png")
    #    self.ground_rect = self.ground_image.get_rect()
        self.mapWidth = 0
        self.scrollX = 0
    #    self.ground_rect.x = self.ground_rect.centerx - 844
    #    self.ground_rect.y = self.ground_rect.centery + 499
        self.backgroundImage =  pygame.transform.scale(self.backgroundImage, (self.screen_size))
    ##    self.groundOutline = pygame.transform.laplacian(self.ground_image)
     #   self.groundOutlineRect = self.ground_rect
       
       
    @staticmethod
    def getGroundOutline(self):
        return self.groundOutline
        

    def update(self):
        self.scrollX = self.model.mario.rect.x - 50
     #   self.model.groundRect = self.ground_rect
        self.screen.fill([0, 181, 226])
        self.screen.blit(self.backgroundImage, (0, 20))
       

        for sprite in self.model.spriteList:
            self.screen.blit(
                sprite.image, (sprite.rect.left - self.scrollX, sprite.rect.top)
            )
   #     self.screen.blit(
   #         self.ground_image, ((self.ground_rect.x - self.scrollX), self.ground_rect.y)
    #    )
     #   self.screen.blit(
     #       self.groundOutline, ((self.groundOutlineRect.x - self.scrollX), self.groundOutlineRect.y)
      #  )

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
            self.model.mario.changeImage()
        if keys[K_RIGHT]:
            self.model.mario.rect.x += 5
            self.model.mario.changeImage()
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
