import pygame,random,sys
from pygame.locals import *
from menu import show_menu
from objects import Player,Enemy1,BlackHole,Bullet,Explosion,Enemyships,Meteors
from constants import WIDTH, HEIGHT,FPS
from game_functions import music_background,show_game_over,update_bullets,score_w
pygame.init()

size = [WIDTH, HEIGHT]
running = True
paused = False
score = 0
level = 1
player_life = 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Last Star Battle!")
FramePerSec = pygame.time.Clock()

explosion_images = [pygame.image.load(f"./images/explosion/explosion{i}.png") for i in range(18)]
enemyships_imgs = [
    pygame.image.load('./images/enemy/enemy2_1.png').convert_alpha(),
    pygame.image.load('./images/enemy/enemy2_2.png').convert_alpha()
]
enemy1_img = [
    pygame.image.load('./images/enemy/enemy1_1.png').convert_alpha(),
    pygame.image.load('./images/enemy/enemy1_2.png').convert_alpha(),
    pygame.image.load('./images/enemy/enemy1_3.png').convert_alpha()
]
black_hole_imgs = [
    pygame.image.load('./images/hole/black_hole.png').convert_alpha(),
    pygame.image.load('./images/hole/black_hole2.png').convert_alpha()
]
meteor_imgs = [
    pygame.image.load('./images/meteors/meteor_1.png').convert_alpha(),
    pygame.image.load('./images/meteors/meteor_2.png').convert_alpha(),
    pygame.image.load('./images/meteors/meteor_3.png').convert_alpha(),
    pygame.image.load('./images/meteors/meteor_4.png').convert_alpha()
]
small_hole = pygame.image.load('./images/smallhole.png').convert_alpha()

class Point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        black_hole_img = random.choice(black_hole_imgs)
        self.image = pygame.image.load(r'./images/hole/black_hole.png')
        self.rect = self.image.get_rect()
        self.dx , self.dy = (BlackHole(black_hole_img).x, BlackHole(black_hole_img).y)
        self.rect.center = (self.dx, self.dy)

P1 = Player()
P2 = Point()
# B1 = BlackHole()
bullets = pygame.sprite.Group()
enemyship_group = pygame.sprite.Group()
EnemyShipBullets = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
holes = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
points = pygame.sprite.Group()
explosions = pygame.sprite.Group()
points.add(P2)

if show_menu:
    import menu
    menu.main()
else:
    music_background()

while running:
    background = pygame.image.load(f"./images/bg/background{level}.png")
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_bullet = Bullet(P1.rect.centerx,P1.rect.top,screen)
                bullets.add(new_bullet)
            elif event.key == pygame.K_p or event.key == pygame.K_PAUSE:
                paused = not paused
    
    if score > 2000:
        level = 2
    if score > 4000:
        level = 3
    if score > 6000:
        level = 4
    if score > 8000:
        level = 5

    screen.blit(P1.image,P1.rect)
    P1.move()
    if not paused:
        if random.randint(0, 40) == 0:
            enemy_img = random.choice(enemy1_img)
            enemy_object = Enemy1(
                random.randint(100, WIDTH - 50),
                random.randint(-HEIGHT, -50),
                enemy_img,
            )
            enemy1_group.add(enemy_object)
        
        if score > 3000 and random.randint(0, 40) == 0:
            meteor_img = random.choice(meteor_imgs)
            meteor_object = Meteors(
                random.randint(0, 50),
                random.randint(0, 50),
                meteor_img,
            )
            meteor_group.add(meteor_object)

        if score >= 5000 and random.randint(0, 40) == 0 and len(enemyship_group) < 2:
            enemy_img = random.choice(enemyships_imgs)
            ship = Enemyships(
                random.randint(200, WIDTH - 100),
                random.randint(-HEIGHT, -100),
                enemy_img,
            )
            enemyship_group.add(ship)

        #check collition with player and enemy1
        for enemy_object in enemy1_group:
            enemy_object.update(enemy1_group)
            enemy1_group.draw(screen)

            if enemy_object.rect.colliderect(P1.rect):
                player_life -= 10
                explosion = Explosion(enemy_object.rect.center, explosion_images)
                explosions.add(explosion)
                enemy_object.kill()
                score += 25
            
            bullet_collisions = pygame.sprite.spritecollide(enemy_object, bullets, True)
            for bullet_collision in bullet_collisions:
                explosion = Explosion(enemy_object.rect.center, explosion_images)
                explosions.add(explosion)
                enemy_object.kill()
                score += 50

        #check collition with player and enemyship
        for ship in enemyship_group:
            ship.update(EnemyShipBullets,P1)
            enemyship_group.draw(screen)
            EnemyShipBullets.update()
            EnemyShipBullets.draw(screen)

            if ship.rect.colliderect(P1.rect):
                player_life -= 10
                explosion = Explosion(ship.rect.center,explosion_images)
                explosions.add(explosion)
                ship.kill()
                score += 20
            bullet_collisions = pygame.sprite.spritecollide(ship, bullets, True)
            for bullet_collision in bullet_collisions:
                explosion = Explosion(ship.rect.center, explosion_images)
                explosions.add(explosion)
                ship.kill()
                score += 50

            for enemy_bullet in EnemyShipBullets:
                if enemy_bullet.rect.colliderect(P1.rect):
                    player_life -= 10
                    explosion = Explosion(enemy_bullet.rect.center, explosion_images)
                    explosions.add(explosion)
                    enemy_bullet.kill()

        #check collition with palyer and meteors
        for meteor_object in meteor_group:
            meteor_object.update()
            meteor_object.draw(screen)

            if meteor_object.rect.colliderect(P1.rect):
                player_life -= 10
                explosion = Explosion(meteor_object.rect.center, explosion_images)
                explosions.add(explosion)
                meteor_object.kill()
                score += 30

            bullet_collisions = pygame.sprite.spritecollide(meteor_object, bullets, True)
            for bullet_collision in bullet_collisions:
                explosion = Explosion(meteor_object.rect.center, explosion_images)
                explosions.add(explosion)
                meteor_object.kill()
                score += 60
            if score >= 4000:
                meteor_object.speed = 4
            if score >= 6000:
                meteor_object.speed = 6
            if score >= 8000:
                meteor_object.speed = 8
            if score >= 18000:
                meteor_object.speed = 10

        for explosion in explosions:
            explosion.update()
            screen.blit(explosion.image, explosion.rect)
        
        #black hole
        if score >= 4000:
            black_hole_img = random.choice(black_hole_imgs)
            for point in points:
                screen.blit(point.image, point.rect)
            for entity in holes:
                holes.add(BlackHole(black_hole_img))
                holes.draw(screen)
                screen.blit(entity.image, entity.rect)
            if pygame.sprite.spritecollideany(P1, points):
                BlackHole(black_hole_img).x , BlackHole(black_hole_img).y = (random.randint(20, 1150), random.randint(400, 750))
                P1.rect.center = (random.randint(20, 1150), random.randint(400, 750))
                BlackHole(black_hole_img).rect.center = (BlackHole(black_hole_img).x, BlackHole(black_hole_img).y)
                P2.rect.center = (BlackHole(black_hole_img).x, BlackHole(black_hole_img).y)

        if player_life <= 0:
            show_game_over(score)
            player_life = 500
            score = 0
            level = 1
            bullets.empty()
            points.empty()
            enemy1_group.empty()
            holes.empty()
            explosions.empty()
            enemyship_group.empty()
            EnemyShipBullets.empty()
        player_life_surface = pygame.Surface((player_life, 25), pygame.SRCALPHA, 32)
        player_life_surface.set_alpha(216)
        player_life_bar = pygame.Surface(((player_life / 100) * 200, 30), pygame.SRCALPHA, 32)
        player_life_bar.set_alpha(216)
        life_bar_image = pygame.image.load("./images/life_bar.png").convert_alpha()
        if player_life > 50:
            player_life_bar.fill((152, 251, 152))
        else:
            player_life_bar.fill((0, 0, 0))
        player_life_surface.blit(life_bar_image, (0, 0))
        player_life_surface.blit(player_life_bar, (35, 0))
        screen.blit(player_life_surface, (10, 10))
        update_bullets(bullets)
        
    if paused:
        font = pygame.font.SysFont('Impact', 40)
        text = font.render("PAUSE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        # continue
    score_w(score,level)
    pygame.display.update()
    FramePerSec.tick(FPS)
pygame.mixer.music.stop()
pygame.quit()
sys.exit()