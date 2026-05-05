import pygame

pygame.init()

# Measurements
WIDTH, HEIGHT = 600, 400
PADH = 80
PADW = WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)

# Objects
clock = pygame.time.Clock()

floor = pygame.Rect(0, HEIGHT - PADH, PADW, PADH)
wall = pygame.Rect(90, 270, 30, 50)

ball = pygame.Rect(5, HEIGHT - PADH - 15, 15, 15)
ball_dx, ball_dy = 0, 0

friction = 0.7
gravity = 2

jump = False

# Game loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        ball_dx = -5
    elif keys[pygame.K_d]:
        ball_dx = 5
    else:
        ball_dx *= friction

    if keys[pygame.K_w] and not jump:
        ball_dy = -20
        jump = True

    # Apply gravity
    ball_dy += gravity

    # Horizontal movement
    ball.x += ball_dx
    if ball.colliderect(wall):
        if ball_dx > 0:
            ball.right = wall.left
        elif ball_dx < 0:
            ball.left = wall.right

    # Vertical movement
    ball.y += ball_dy
    if ball.colliderect(wall):
        if ball_dy > 0:  # falling
            ball.bottom = wall.top
            ball_dy = 0
            jump = False
        elif ball_dy < 0:  # jumping
            ball.top = wall.bottom
            ball_dy = 0

    # Floor collision
    if ball.colliderect(floor):
        if ball_dy > 0:
            ball.bottom = floor.top
            ball_dy = 0
            jump = False

    # Drawing
    screen.fill(LIGHT_BLUE)
    pygame.draw.ellipse(screen, ORANGE, ball)
    pygame.draw.rect(screen, GREEN, floor)
    pygame.draw.rect(screen, WHITE, wall)

    pygame.display.flip()

pygame.quit()