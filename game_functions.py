import pygame
from constants import WIDTH, HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
def music_background():
    pygame.mixer.music.load('./game_sound/fight.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def show_game_over(score):
    font = pygame.font.SysFont('Impact', 50)
    font_small = pygame.font.SysFont('Impact', 30)
    text = font.render("GAME OVER", True, (139, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.mixer.music.load('./game_sound/gameover.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(4000)
    music_background()

def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        bullet.update()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for bullet in bullets.sprites():
        bullet.blit_bullet()

def score_w(score,level):
    font = pygame.font.SysFont('Game Over Regular', 60)
    text = font.render(f"| Score: {score} || Level: {level} |",True, (0,0,0))
    text_rect = text.get_rect(center=(WIDTH - 150, 30))
    screen.blit(text,text_rect)