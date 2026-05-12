import pygame



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

ball_dx, ball_dy = 0, 0

friction = 0.7
gravity = 2

jump = False

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
        self.on_ground = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
platforms.add(Platform(0, HEIGHT, WIDTH, 10, GREEN)) #Floor
platforms.add(Platform(200, HEIGHT-100, 100, 20, GREEN)) #Small ledge
platforms.add(Platform(275, HEIGHT-200, 100, 20, GREEN)) #Higher ledge
platforms.add(Platform(350, HEIGHT-300, 100, 20, GREEN)) #Higher ledge
platforms.add(Platform(300, HEIGHT-350, 100, 20, GREEN)) #Higher ledge
all_sprites.add(platforms)

ball = Player(0, HEIGHT-15, ORANGE)
all_sprites.add(ball)

pygame.init()
'''
platforms = pygame.sprite.Group()
platforms.add(Platform(0, HEIGHT, WIDTH, 50, ))
platforms.add(Platform(200, 4000, 100, 20))
platforms.add(Platform(400, 300, 100, 20))
'''


# Game loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and player.on_ground:
        ball.on_ground = False
        ball.vely = -15
    if keys[pygame.K_d]:
        ball.velx = 5
    if keys[pygame.K_a]:
        player.velx = -5
    else:
        ball_dx *= friction

    if keys[pygame.K_w] and not jump:
        ball_dy = -20
        jump = True

    # Apply gravity
    ball_dy += gravity

    # Horizontal movement
    ball.velx *= friction
    ball.rect.x += ball.velx
    hits = pygame.sprite.spritecollide(ball, platforms, False)
    if hits:
        for platform in hits:
            if ball_velx > 0: # right
                ball.rect.right = platform.rect.left
            elif ball_velx < 0: # left
                ball.rect.left = platform.rect.right

    # Vertical movement
    ball.vely += gravity
    ball.rect.y += ball.vely
    hits = pygame.sprite.spritecollide(ball, platforms, False)
    if hits:
        for platform in hits:
            if ball.vely > 0:  # landing
                ball.rect.bottom = platform.rect.top
                ball.vely = 0
                ball.on_ground = True
            elif ball.vely < 0:  # hitting head
                ball.rect.top = platform.rect.bottom
                ball.vely = 0
    '''
    # Floor collision
    if ball.colliderect(floor):
        if ball_dy > 0:
            ball.bottom = floor.top
            ball_dy = 0
            jump = False
    '''
    # Drawing
    all_sprites.draw(screen)
    '''
    screen.fill(LIGHT_BLUE)
    pygame.draw.ellipse(screen, ORANGE, ball)
    pygame.draw.rect(screen, GREEN, floor)
    pygame.draw.rect(screen, WHITE, wall)
    '''
    pygame.display.flip()

pygame.quit()