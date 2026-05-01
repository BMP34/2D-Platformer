import pygame

# Measurements
WIDTH, HEIGHT = 600, 400
PADH = 80
PADW = WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)

# Objects
clock = pygame.time.Clock()

left = pygame.Rect(0,0,1,HEIGHT)
right = pygame.Rect(600,0,1,HEIGHT)

floor = pygame.Rect(0, (HEIGHT)-(PADH), PADW, PADH)
#wall = pygame.Rect(30, 

ball = pygame.Rect(5, (HEIGHT)-(PADH), 15, 15)
ball_dx, ball_dy = 5, -5

jump = False

# Display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if ball.left <= 0:
        ball.left = 0
    elif ball.right >= WIDTH:
        ball.right = WIDTH
    if ball.bottom >= (HEIGHT)-(PADH):
        ball.bottom = (HEIGHT)-(PADH)
        ball_dy = 0
        jump = False
        
    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        ball.x -= ball_dx
    if keys[pygame.K_d]:
        ball.x += ball_dx
    if keys[pygame.K_LEFT]:
        ball.x -= ball_dx
    if keys[pygame.K_RIGHT]:
        ball.x += ball_dx
    if keys[pygame.K_w] and jump == False:
        ball_dy = -20
        jump = True

    screen.fill(LIGHT_BLUE)
    pygame.draw.ellipse(screen, ORANGE, ball)
    pygame.draw.rect(screen, GREEN, floor)
    pygame.display.flip()
    clock.tick(60)
    ball.y += ball_dy
    ball_dy += 2

pygame.quit()