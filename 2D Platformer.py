import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fil((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

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


platforms = pygame.sprite.Group()
platforms.add(Platform(0, HEIGHT, WIDTH, 50))
platforms.add(Platform(200, 4000, 100, 20))
platforms.add(Platform(400, 300, 100, 20))


hits= pygame.sprite.spritecollide(player, platforms, False)

if hits:
    for wall in hits:
        if ball.vel_y > 0:
            ball.rect.bottom = wall.rect.top
            ball.vel_y = 0
            ball.on_ground = True

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