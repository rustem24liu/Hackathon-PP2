import pygame , sys , random , time , os
from pygame.locals import *
pygame.init()

size = [1200, 800]
cnt = 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cosmic Attack")

icon = pygame.image.load("./img/icon/universe.png") #
pygame.display.set_icon(icon)

background = pygame.image.load("./img/backgrounds/bg2.png")

FPS = 60
FramePerSec = pygame.time.Clock()

running = True

coinFont = pygame.font.SysFont("childer", 40)
coinFont2 = pygame.font.SysFont("childer", 25)
sosFont = pygame.font.SysFont('Game Over Regular', 78)
bonus2pointFont = pygame.font.SysFont('Game Over Regular', 70)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./img/player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (570, 750)
        self.speed = 10
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 1200:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(self.speed, 0)
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < 800:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, self.speed)
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./img/bullet/bullet1.png')
        self.rect1 = self.image.get_rect()
        self.rect1.center = (P1.rect.center)
    def fire(self):
        pressedkey = pygame.key.get_pressed()
        if pressedkey[K_f]:        
            self.rect1.move_ip(0, -P1.speed)
        
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        self.rand = random.randint(1, 6)
        self.image = pygame.image.load(f'./img/enemy/enemy2_1.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, 1200), 40)
        self.speed2 = 7
    def move(self):
        self.rect.move_ip(self.speed2, 0) 
        self.speed2 += 0.001
        if (self.rect.right > 800): 
            self.rect.right = 0                
            self.E = random.randint(1, 6)
            self.image = pygame.image.load(f'./img/enemy/enemy2_1.png' )
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(20, 1200), 40) 



P1 = Player()
E1 = Enemy()
B1 = Bullet()
# C1 = Coins()
# B1 = Bonuscoin()
# Q1 = Beer()

# enemies = pygame.sprite.Group() 
# enemies.add(E1)
bullet= pygame.sprite.Group()
bullet.add(B1)
# coins = pygame.sprite.Group()
# coins.add(C1)
# beer = pygame.sprite.Group()
# beer.add(Q1)

all_sprites = pygame.sprite.Group()

# new_sprites = pygame.sprite.Group()
# beer_sprites = pygame.sprite.Group()


all_sprites.add(P1)
# all_sprites.add(E1)
# all_sprites.add(C1)

# new_sprites.add(B1)
# beer_sprites.add(Q1)

# show_bonus = False
# show_sos = False
# bonus_timer = 0

while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
    screen.blit(background, (0, 0))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
    
    pressedkey = pygame.key.get_pressed()
    
    for x in bullet:
        screen.blit(x.image,x.rect1 )
        x.fire()



    # if B1.ayou >= 10:
    #     for things in new_sprites:
    #         screen.blit(things.image, things.rect)
    #         things.move()

    # if Q1.arus >= 15:
    #     for x in beer_sprites:
    #         screen.blit(x.image, x.rect)
    #         x.move()


    # if pygame.sprite.spritecollideany(P1, enemies):
    #     pygame.mixer.Sound('crash.mp3').play()
    #     photo = pygame.image.load("images/gameover.jpg")   
    #     screen.blit(photo, (30, 60))
        
    #     print("You lose dumb!")
    #     print(f"Your score is:{cnt}")

    #     pygame.display.update()

    #     time.sleep(2)
    #     pygame.quit()
    #     sys.exit()
    
    # if pygame.sprite.spritecollideany(P1, coins):
    #     P1.BEER = True
    #     pygame.mixer.Sound('coin.mp3').play()
    #     cnt+=1
    #     B1.ayou +=1
    #     Q1.arus +=1
    #     C1.rect.top = 600
    


    # if pygame.sprite.spritecollideany(P1, beer):
    #     pygame.mixer.Sound('beer-fridge.mp3').play()
    #     sos_timer = pygame.time.get_ticks()
    #     show_sos = True
    #     P1.BEER = False
    #     Q1.arus =0
    #     Q1.rect.top = 0
    # if show_sos:
    #     beersos = coinFont2.render('You are drunk, stop or just slow down!', True, RED)
    #     SOS = sosFont.render('SOS!! BEER', True, BLACK) 
    #     screen.blit(beersos, (10, 10))
    #     screen.blit(SOS, (140, 230))
    #     if pygame.time.get_ticks() - sos_timer >= 5000:
    #         show_sos = False

    # if pygame.sprite.spritecollideany(P1, bonus):  
    #     B1.ayou = 0
    #     cnt+=2
    #     Q1.arus +=1
    #     B1.rect.top = 0
    #     show_bonus = True
    #     bonus_timer = pygame.time.get_ticks()
    #     pygame.mixer.Sound('coin.mp3').play()
    # if show_bonus:
    #     bonuss = coinFont.render('+2$', True, RED)
    #     screen.blit(bonuss, (350, 60))
    #     image = pygame.image.load(f'images/Coin/maintenance.png')
    #     screen.blit(image, (10, 10))
    #     bonus_2point = bonus2pointFont.render("BONUS +2", True, BLACK)
    #     screen.blit(bonus_2point, (50, 10))
    #     if pygame.time.get_ticks() - bonus_timer >=1000:
    #         show_bonus = False
    pygame.display.update()
    pygame.display.flip()
    FramePerSec.tick(FPS)
    