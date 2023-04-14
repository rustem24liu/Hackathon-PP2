import pygame
import sys
import random
import pygame.mixer

WIDTH, HEIGHT = 1200, 800
FPS = 60
WHITE = (154, 164, 166)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def animate_screen():
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)


pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load(r'img/xxx.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

logo_img = pygame.image.load('img/ch.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)

# pygame.mixer.music.load(r'C:\Users\Nurza\Documents\PP2\week9\game\game_souds\game_sounds_menu.mp3')
# pygame.mixer.music.play(-1)
# explosion_sound = pygame.mixer.Sound(r'C:\Users\Nurza\Documents\PP2\week9\game\game_souds\explosions\game_sounds_explosions_explosion1.wav')

selected_button = 0
show_menu = True
joystick = None
# if pygame.joystick.get_count() > 0:
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                # explosion_sound.play()
                animate_screen()
                show_menu = False
                import spacerustem
                spacerustem.main()
                break
            elif quit_button_rect.collidepoint(x, y):
                pygame.quit()
                sys.exit()
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_button = 0
            elif event.key == pygame.K_DOWN:
                selected_button = 1
            elif event.key == pygame.K_RETURN:
                if selected_button == 0:
                    # explosion_sound.play()
                    animate_screen()
                    show_menu = False
                    screen.fill(BLACK)
                    import spacerustem
                    spacerustem.main()
                    break
                elif selected_button == 1:
                    pygame.quit()
                    sys.exit()
                
    screen.blit(mainmenu_img, (0, 0))

    screen.blit(logo_img, (logo_x, logo_y))

    font = pygame.font.Font(None, 42)
    text = font.render("Play", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)

    text = font.render("Exit", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = quit_button_rect.center
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()