import pygame
import random
pygame.init()
size = (700, 500)
fps = 60
white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("DVD")
clock = pygame.time.Clock()

running = True

x = 180
y = 70
dx = 2
dy = 2
color = white

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(black)
    clock.tick(fps)
    
    x += dx
    y += dy

    if x > 520 or x < 0:
        dx *= -1
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if y > 430 or y < 0:
        dy *= -1
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    pygame.draw.rect(screen, color, (x, y, 180, 70))
    font = pygame.font.SysFont('verdana', 58, True, True)
    text = font.render("DVD", True, black)
    screen.blit(text, (x+22, y))
    pygame.display.flip()

pygame.quit()