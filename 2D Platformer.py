import pygame

pygame.init()

# Measurements
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)
RED = (82, 37, 28)
TAN = (226, 207, 181)
DARK_BLUE = (90, 102, 171)

# Objects
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Physics
friction = 0.8
gravity = 1

# Win condition
won = False


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        self.image = pygame.Surface((15, 15))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.velx = 0
        self.vely = 0
        self.on_ground = False


# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect(topleft=(x, y))


# Sprite Groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Platforms
platforms.add(Platform(0, HEIGHT - 10, WIDTH, 10, GREEN))          # Floor
platforms.add(Platform(200, HEIGHT - 100, 100, 20, RED))         # Small ledge
platforms.add(Platform(275, HEIGHT - 200, 100, 20, TAN))         # Higher ledge
platforms.add(Platform(350, HEIGHT - 300, 100, 20, DARK_BLUE))         # Higher ledge
platforms.add(Platform(300, HEIGHT - 350, 100, 20, WHITE))         # Highest ledge

all_sprites.add(platforms)

# Player
ball = Player(50, HEIGHT - 50, ORANGE)
all_sprites.add(ball)

# Game Loop
running = True

while running:
    clock.tick(60)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # WIN CONDITION
    if ball.rect.y <= 35:
        won = True

    # GAME LOGIC
    if not won:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            ball.velx = 5

        elif keys[pygame.K_a]:
            ball.velx = -5

        else:
            ball.velx *= friction
            if abs(ball.velx) < 0.1:
                ball.velx = 0

        if keys[pygame.K_SPACE] and ball.on_ground:
            ball.vely = -15
            ball.on_ground = False

        ball.vely += gravity

        # Horizontal movement
        ball.rect.x += ball.velx

        hits = pygame.sprite.spritecollide(ball, platforms, False)
        for platform in hits:
            if ball.velx > 0:
                ball.rect.right = platform.rect.left
            elif ball.velx < 0:
                ball.rect.left = platform.rect.right

        # Vertical movement
        ball.rect.y += ball.vely

        hits = pygame.sprite.spritecollide(ball, platforms, False)

        if hits:
            for platform in hits:
                if ball.vely > 0:
                    ball.rect.bottom = platform.rect.top
                    ball.vely = 0
                    ball.on_ground = True
                elif ball.vely < 0:
                    ball.rect.top = platform.rect.bottom
                    ball.vely = 0
        else:
            ball.on_ground = False

    # DRAWING (ALWAYS RUNS)
    screen.fill(LIGHT_BLUE)

    if not won:

        all_sprites.draw(screen)

        # Flag pole
        pygame.draw.rect(screen, WHITE, (340, 20, 5, 40))

        # Checkered flag
        square_size = 10
        colors = [WHITE, (0, 0, 0)]

        for row in range(2):
            for col in range(2):
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    screen,
                    color,
                    (345 + col * square_size, 20 + row * square_size,
                     square_size, square_size)
                )

    else:
        text = font.render("CONGRATULATIONS!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()