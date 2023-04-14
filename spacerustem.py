import pygame,random, sys
from pygame.locals import *
from menu import show_menu, animate_screen

WIDTH = 1200
HEIGHT = 800
FPS = 60
ENEMY_ROW = 2
ENEMY_SUM = 6
ENEMY_FORCE = 4
size = [WIDTH, HEIGHT]
running = True
screen = pygame.display.set_mode(size)
background = pygame.image.load(r"./img/backgrounds/bg3.png")
FramePerSec = pygame.time.Clock()
pygame.init()

enemy1_img = [
    pygame.image.load('img/enemy/enemy1_1.png').convert_alpha(),
    pygame.image.load('img/enemy/enemy1_2.png').convert_alpha(),
    pygame.image.load('img/enemy/enemy1_3.png').convert_alpha()
]

def main():
    pass
    # pygame.mixer.music.stop()
    # pygame.mixer.music.load('game_sounds/game.mp3')
    # pygame.mixer.music.play(-1)
    # animate_screen()

# def music_background():
#     pygame.mixer.music.load(r'C:\Users\Nurza\Documents\PP2\week9\game\game_souds\game_sounds_background_music.mp3')
#     pygame.mixer.music.set_volume(0.5)
#     pygame.mixer.music.play(-1)

def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        bullet.update()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for bullet in bullets.sprites():
        bullet.blit_bullet()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'./img/player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (570, 750)
        self.speed = 10
    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if keys[K_a]:
                self.rect.move_ip(-self.speed, 0)
        if self.rect.right < WIDTH:        
            if keys[K_d]:
                self.rect.move_ip(self.speed, 0)
        if self.rect.top > 0:
            if keys[K_w]:
                self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < HEIGHT:
            if keys[K_s]:
                self.rect.move_ip(0, self.speed)
P1 = Player()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/bullet/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y-10
        self.speed = 10
        # self.shoot_sound = pygame.mixer.Sound(r'C:\Users\Nurza\Documents\PP2\week9\game\game_souds\shooting\game_sounds_shooting_shoot.mp3')
        # self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(0, -self.speed)
    def blit_bullet(self):
        screen.blit(self.image,self.rect)

class Enemy1(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.direction = random.choice([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def update(self, enemy_group):
        dx, dy = self.direction
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if self.rect.left < 5:
            self.rect.left = 5
            self.direction = random.choice([(1, 0), (0, -1), (0, 1), (1, -1), (1, 1)])
        elif self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH - 5
            self.direction = random.choice([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)])

        if self.rect.top < 5:
            self.rect.top = 5
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1)])
        elif self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5
            self.direction = random.choice([(1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)])

        collided_with = pygame.sprite.spritecollide(self, enemy_group, False)
        for other_enemy in collided_with:
            if other_enemy != self:
                distance_vec = pygame.math.Vector2(other_enemy.rect.center) - pygame.math.Vector2(self.rect.center)
                distance = distance_vec.length()
                angle = distance_vec.angle_to(pygame.math.Vector2(1, 0))

                repel_vec = pygame.math.Vector2(1, 0).rotate(angle)
                repel_vec *= (1 - (distance / (self.rect.width + other_enemy.rect.width)))
                repel_vec *= ENEMY_FORCE

                self_dir = pygame.math.Vector2(self.direction)
                other_dir = pygame.math.Vector2(other_enemy.direction)

                if distance != 0:
                    new_dir = self_dir.reflect(distance_vec).normalize()
                    other_new_dir = other_dir.reflect(-distance_vec).normalize()

                    self.direction = new_dir.x, new_dir.y
                    other_enemy.direction = other_new_dir.x, other_new_dir.y

                self.rect.move_ip(-repel_vec.x, -repel_vec.y)
                other_enemy.rect.move_ip(repel_vec.x, repel_vec.y)

class BlackHole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./img/black_hole.png')
        self.rect = self.image.get_rect()
        self.x, self.y = random.randint(30, 1150), random.randint(30, 760)
        self.rect.center = (self.x, self.y) 

class Point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./img/black_hole2.png')
        self.rect = self.image.get_rect()
        self.dx , self.dy = (B1.x, B1.y)
        self.rect.center = (self.dx, self.dy)



B1 = BlackHole()
P2 = Point()


bullets = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
hole = pygame.sprite.Group()
point = pygame.sprite.Group()
hole.add(B1)
point.add(P2)

if show_menu:
    import menu
    menu.main()

while running:

    screen.blit(background, (0, 0))
    # music_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_bullet = Bullet(P1.rect.centerx,P1.rect.top)
                bullets.add(new_bullet)
    
    screen.blit(P1.image,P1.rect)
    P1.move()
    
    if random.randint(0, 100) == 0:
        enemy_img = random.choice(enemy1_img)
        enemy_object = Enemy1(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50),
            enemy_img,
        )
        enemy1_group.add(enemy_object)

    for enemy_object in enemy1_group:
        enemy_object.update(enemy1_group)
        enemy1_group.draw(screen)
    
    
    for points in point:
        screen.blit(points.image, points.rect)
    for entity in hole:
        screen.blit(entity.image, entity.rect)
    
    if pygame.sprite.spritecollideany(P1, point):
        B1.x , B1.y = (random.randint(20, 1170), random.randint(20, 770))
        P1.rect.center = (random.randint(20, 1170), random.randint(20, 770))
        B1.rect.center = (B1.x, B1.y)
        P2.rect.center = (B1.x, B1.y)
    


    # B1.draw()
    

    
    update_bullets(bullets)
    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()    