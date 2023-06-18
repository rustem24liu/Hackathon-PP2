import pygame
from pygame.locals import *
from constants import WIDTH, HEIGHT, ENEMY_FORCE
import random
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./images/player.png')
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
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,screen):
        super().__init__()
        self.image = pygame.image.load('./images/bullets/bullet4.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y-10
        self.screen = screen
        self.speed = 10
        self.shoot_sound = pygame.mixer.Sound('./game_sound/shooting/game_sounds_shooting_shoot.mp3')
        self.shoot_sound.play()
    def update(self):
        self.rect.move_ip(0, -self.speed)
    def blit_bullet(self):
        self.screen.blit(self.image,self.rect)
    
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
        elif self.rect.top > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5
            self.direction = random.choice([(1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)])
            # self.kill()

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
    def __init__(self,image):
        super().__init__()
        # self.image = pygame.image.load(r'C:\Users\Nurza\Documents\PP2\week9\game\images\hole\black_hole.png')
        self.image = image
        self.rect = self.image.get_rect()
        self.x, self.y = random.randint(30, 1150), random.randint(30, 760)
        self.rect.center = (self.x, self.y)
    
class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, explosion_images):
        super().__init__()
        self.explosion_images = explosion_images
        self.image = self.explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.explosion_sounds = [
            pygame.mixer.Sound(r'./game_sound/explosions/game_sounds_explosions_explosion1.wav'),
            pygame.mixer.Sound(r'./game_sound/explosions/game_sounds_explosions_explosion2.wav'),
            pygame.mixer.Sound(r'./game_sound/explosions/game_sounds_explosions_explosion3.wav')
        ]
        self.explosion_sound = random.choice(self.explosion_sounds)
        self.sound_played = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                if not self.sound_played:
                    self.explosion_sound.play()
                    self.sound_played = True    

class EnemyShipBullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./images/bullets/bullet4.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 8
        self.shoot_sound = pygame.mixer.Sound(r'./game_sound/explosions/game_sounds_explosions_explosion2.wav')
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.kill()

class Enemyships(pygame.sprite.Sprite):

    def __init__(self,x,y,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 4
        self.direction = random.choice([(-1,0),(1,0)])
        self.shoots_fired = 0
        self.shoot_timer = 0

    def update(self,enemy_bullets_group,player):
        if self.shoots_fired < 5:
            dx,dy = self.direction
            self.rect.x += dx * self.speed
            self.rect.y = max(self.rect.y, 5)

            if self.rect.left < 5:
                    self.rect.left = 5
                    self.direction = (1, 0)
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction = (-1, 0)

            self.shoot_timer += 1
            if self.shoot_timer >= 60:
                bullet = EnemyShipBullet(self.rect.centerx,self.rect.bottom)
                enemy_bullets_group.add(bullet)
                self.shoots_fired += 1
                self.shoot_timer = 0

        else:
            self.speed = 10
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

class Meteors(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_x = 1
        self.direction_y = 1
        self.angle = 0
        self.speed = 2

    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        if self.rect.bottom >= HEIGHT + 50 or self.rect.right >= WIDTH + 50:
            self.kill()

        self.angle = (self.angle - 1) % 360
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)