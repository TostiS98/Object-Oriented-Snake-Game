import pygame
import random
from os import path

pygame.mixer.init()

# ========================================== COLOUR DEFINITIONS =======================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 145, 0)
BLUE = (0, 0, 255)
GRAY = (36, 36, 36)
# ========================================== END OF - COLOUR DEFINITIONS ==============================================

# ======================================== INITIALIZE PYGAME AND CREATE WINDOW ========================================

# Create the width and height of the screen, as well as the fps that the game will run at
WIDTH = 800
HEIGHT = 600
FPS = 30

# Set the width and height of each snake segment, and set the space in between each segment
snake_segment_width = 13
snake_segment_height = 13
snake_segment_space = 2

# Set the players default score, and set the boundaries for which the apples can spawn
score = 0
high_score = 0
apple_boundary_x = WIDTH - 40
apple_boundary_y = HEIGHT - 40
screen_midpoint = WIDTH/2
screen_midpoint_y = HEIGHT/2
apples_spawned = 1

# Predefine game_over to true in order to load into the waiting screen, and rules_waiting to false for the rules screen
game_over = True
rules_waiting = False
font_name = pygame.font.match_font("source code pro")

# Set initial speed that the snake will move at (note these are global as we need them in the main loop)
speed_x = snake_segment_width + snake_segment_space
speed_y = 0
direction = "right"


# Setup directory for sounds (music, eating and game over), adjust volume and play background music
sounds_dir = path.join(path.dirname("__file__"), "sounds")

eating_sound = pygame.mixer.Sound(path.join(sounds_dir, 'SFX_Powerup_01.wav'))
pygame.mixer.Sound.set_volume(eating_sound, 0.3)

death_sound = pygame.mixer.Sound(path.join(sounds_dir, 'SFX_Powerup_03.wav'))
pygame.mixer.Sound.set_volume(death_sound, 0.3)

powerup_sound = pygame.mixer.Sound(path.join(sounds_dir, 'SFX_Powerup_17.wav'))
pygame.mixer.Sound.set_volume(powerup_sound, 0.3)

pygame.mixer.music.load(path.join(sounds_dir, 'retro.wav'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

# load the directory for the images used in the game and the images themselves
images_dir = path.join(path.dirname("__file__"), "images")


# Create a function to draw text to the screen
def draw_text(surf, text, size, x, y, colour):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Create a function for the loading screen that displays the games title and how to navigate the UI
def game_over_screen():

    global event

    screen.blit(background, background_rect)
    draw_text(screen, "SNAKE 2.0 - PYTHON EDITION", 70, int(WIDTH/2), int(HEIGHT/4) - 50, BLACK)
    draw_text(screen, "----------------------------------------------", 70, int(WIDTH / 2), int(HEIGHT / 4) - 20, BLACK)
    draw_text(screen, "----------------------------------------------", 70, int(WIDTH / 2), int(HEIGHT / 4) - 90, BLACK)
    draw_text(screen, "=-= TostiS98 =-=", 50, int(WIDTH / 2), int(HEIGHT / 4) + 100, BLACK)
    draw_text(screen, "=-=-=-=-=-=-=-=-=", 50, int(WIDTH / 2), int(HEIGHT / 4) + 65, BLACK)
    draw_text(screen, "=-=-=-=-=-=-=-=-=", 50, int(WIDTH / 2), int(HEIGHT / 4) + 135, BLACK)
    draw_text(screen, ("=== Session High score: " + str(high_score)) + " ===", 45, int(WIDTH / 2), 400, BLACK)
    draw_text(screen, "=-= PRESS ANY KEY TO BEGIN YOUR ADVENTURE OR 'R' TO VIEW RULES =-=", 25, int(WIDTH/2), int(HEIGHT * 3 / 4) + 30, BLACK)
    pygame.display.flip()

    waiting = True

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    rules_screen()
                    waiting = False
                else:
                    waiting = False


def rules_screen():

    global event, rules_waiting

    screen.blit(background, background_rect)
    draw_text(screen, "=-= RULES =-=", 70, int(WIDTH / 2), int(HEIGHT / 4) - 90, BLACK)
    draw_text(screen, "---------------------", 70, int(WIDTH / 2), int(HEIGHT / 4) - 65, BLACK)
    draw_text(screen, "== PRESS ANY KEY AT ANYTIME TO FINISH VIEWING THE RULES SCREEN ==", 25, int(WIDTH / 2), int(HEIGHT / 4) - 20, BLACK)
    draw_text(screen, "== PRESS THE ARROW KEYS TO MOVE YOUR SNAKE AROUND THE SCREEN ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 10, BLACK)
    draw_text(screen, "== YOUR GOAL IS TO COLLECT AS MANY APPLES AS POSSIBLE ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 40, BLACK)
    draw_text(screen, "== AS YOU COLLECT APPLES YOUR SNAKE GROWS, AND YOUR SPEED INCREASES ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 70, BLACK)
    draw_text(screen, "== EVERY APPLE YOU COLLECT WILL ADD ONE TO YOUR SCORE ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 100, BLACK)
    draw_text(screen, "== THE GAME WILL GO ON FOR AS LONG AS YOU LAST OR UNTIL YOUR SNAKE DIES ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 130, BLACK)
    draw_text(screen, "== THE GAME WILL END IF YOU HIT YOUR OWN TAIL, OR GO OFF SCREEN ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 160, BLACK)
    draw_text(screen, "== BLUE POWERUPS HAVE A 10% CHANCE OF SPAWING & WILL DECREASE YOUR SPEED ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 190, BLACK)
    draw_text(screen, "== POWERUPS WILL DESPAWN AFTER 3 SECOND ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 220, BLACK)
    draw_text(screen, "== YOU CAN VIEW THE RULES ANYTIME WHEN PLAYING & CAN EASILY RESUME ==", 25, int(WIDTH / 2), int(HEIGHT / 4) + 250, BLACK)
    draw_text(screen, "=-= PRESS ANY KEY TO BEGIN/RESUME YOUR GAME =-=", 25, int(WIDTH / 2), int(HEIGHT / 4) + 300, BLACK)
    draw_text(screen, "------------------------------------", 70, int(WIDTH / 2), int(HEIGHT / 4) + 260, BLACK)
    pygame.display.flip()

    rules_waiting = True

    while rules_waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    continue
                else:
                    rules_waiting = False


# Create a snake class, it has a x and y location, as well as a movement in the update function.
# hit_tail method determines if the snake has run into its own tail
class Snake(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = player_img
        self.image = pygame.transform.scale(player_img, (snake_segment_width, snake_segment_height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        global speed_x, speed_y, done, snake_segments, direction

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "right":
                speed_x = (snake_segment_width + snake_segment_space) * -1
                speed_y = 0
                direction = "left"
            if event.key == pygame.K_RIGHT and direction != "left":
                speed_x = (snake_segment_width + snake_segment_space)
                speed_y = 0
                direction = "right"
            if event.key == pygame.K_UP and direction != "down":
                speed_x = 0
                speed_y = (snake_segment_height + snake_segment_space) * -1
                direction = "up"
            if event.key == pygame.K_DOWN and direction != "up":
                speed_x = 0
                speed_y = (snake_segment_height + snake_segment_space)
                direction = "down"

    def hit_tail(self):
        snake_hit_tail = pygame.sprite.spritecollide(self, snake_segments, False)

        if snake_hit_tail:
            return True
        else:
            return False


# Create a class for the apple, it has a randomized x and y location based on the last spawn point of the apple
class Apple(pygame.sprite.Sprite):

    def __init__(self):

        global apples_spawned

        apples_spawned += 1
        pygame.sprite.Sprite.__init__(self)
        self.image = apple_img
        self.image = pygame.transform.scale(apple_img, (13, 13))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        if apples_spawned % 2 == 0:
            self.rect.x = random.randrange(screen_midpoint + 40, apple_boundary_x)
            self.rect.y = random.randrange(40, apple_boundary_y)
        else:
            self.rect.x = random.randrange(40, screen_midpoint - 40)
            self.rect.y = random.randrange(40, apple_boundary_y)


class Powerup(pygame.sprite.Sprite):

    def __init__(self):

        global apples_spawned

        pygame.sprite.Sprite.__init__(self)
        self.image = powerup_img
        self.image = pygame.transform.scale(powerup_img, (13, 13))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.last_spawn = pygame.time.get_ticks()

        if apples_spawned % 2 == 0:
            self.rect.x = random.randrange(40, screen_midpoint - 40)
            self.rect.y = random.randrange(40, HEIGHT/2 - 40)

        else:
            self.rect.x = random.randrange(screen_midpoint + 40, apple_boundary_x)
            self.rect.y = random.randrange(HEIGHT/2 + 40, HEIGHT - 40)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn >= 3000:
            self.last_spawn = now
            all_sprites.remove(self)
            powerups.remove(self)


pygame.init()

# Create a screen of size WIDTH by HEIGHT
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('==== TostiS98 - Basic OOP Pygame Snake ====')

# Create the the groups for all sprites, as well as the apples
all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player_img = pygame.image.load(path.join(images_dir, "Green_Snake.png")).convert()
# Create an initial snake of length 5 segments, add to all sprites group, and snake segments list
snake_segments = []
for i in range(5):
    x = 250 - (snake_segment_width + snake_segment_space) * i
    y = 300
    segment = Snake(x, y)
    snake_segments.append(segment)
    all_sprites.add(segment)

# Load all of the images for the game
apple_img = pygame.image.load(path.join(images_dir, "Red_Apple.png")).convert()
powerup_img = pygame.image.load(path.join(images_dir, "Blue_Powerup.png")).convert()
background = pygame.image.load(path.join(images_dir, "Background.png")).convert()
background_rect = background.get_rect()

# Create the first apple and add it to the all sprites and apple groups
apple = Apple()
all_sprites.add(apple)
apples.add(apple)

if random.random() > 0.9:
    powerup = Powerup()
    all_sprites.add(powerup)
    powerups.add(powerup)

clock = pygame.time.Clock()


# ======================================== END OF - INITIALIZE PYGAME AND CREATE ======================================

# ===================================================== GAME LOOP =====================================================

done = False

while not done:

    # keep loop running at the right speed
    clock.tick(FPS)

    # If the game has just started, or the player has died go to the starting screen
    if game_over:
        game_over_screen()
        game_over = False
        snake_hit_tail = False
        all_sprites = pygame.sprite.Group()
        apples = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        speed_x = (snake_segment_width + snake_segment_space)
        speed_y = 0
        direction = "right"
        apples_spawned = 1
        FPS = 30
        snake_segments = []
        pygame.mixer.music.rewind()

        for i in range(5):
            x = 250 - (snake_segment_width + snake_segment_space) * i
            y = 300
            segment = Snake(x, y)
            snake_segments.append(segment)
            all_sprites.add(segment)

        if random.random() > 0.9:
            powerup = Powerup()
            all_sprites.add(powerup)
            powerups.add(powerup)

        apple = Apple()
        all_sprites.add(apple)
        apples.add(apple)
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rules_screen()

    # --------------------------------------------------- UPDATE --------------------------------------------------

    all_sprites.update()

    # Remove the last segment of the snake from the snake_segments list and from all_sprites group
    remove_snake_segment = snake_segments.pop()
    all_sprites.remove(remove_snake_segment)

    # Determine where the new segment of the snake will be based on the snakes speed, and create one at that spot
    x = snake_segments[0].rect.x + speed_x
    y = snake_segments[0].rect.y + speed_y
    segment = Snake(x, y)

    # Determine if any of the snake has gone off screen. If so, end and reset movement direction
    if x <= 0 or x >= WIDTH - snake_segment_width or y <= 0 or y >= HEIGHT - snake_segment_height:
        death_sound.play()
        game_over = True
        speed_x = (snake_segment_width + snake_segment_space)
        speed_y = 0

    # Check if the snake has hit itself, if so, reset snake_hit_tail and end the game
    if segment.hit_tail():
        death_sound.play()
        snake_hit_tail = False
        game_over = True

    # Insert new segment into the list as well as the all sprites group
    snake_segments.insert(0, segment)
    all_sprites.add(segment)

    # Check collision between snake segments and the apples, if so, add a segment and create a new apple
    hits = pygame.sprite.groupcollide(snake_segments, apples, False, True)

    if hits:

        eating_sound.play()

        x = 250 - (snake_segment_width + snake_segment_space) * i
        y = -30
        segment = Snake(x, y)
        snake_segments.append(segment)
        all_sprites.add(segment)

        new_apple = Apple()
        all_sprites.add(new_apple)
        apples.add(new_apple)

        score += 1
        FPS += 1

        if random.random() > 0.9:
            new_powerup = Powerup()
            all_sprites.add(new_powerup)
            powerups.add(new_powerup)

    hits = pygame.sprite.groupcollide(snake_segments, powerups, False, True)

    if hits:
        FPS -= 2
        powerup_sound.play()

    if score > high_score:
        high_score += 1

    # --------------------------------------------------- DRAW ----------------------------------------------------

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, ("=== Current Score: " + str(score)) + " ===", 22, int(WIDTH / 2) - 125, 5, WHITE)
    draw_text(screen, ("=== Session High score: " + str(high_score)) + " ===", 22, int(WIDTH / 2) + 125, 5, WHITE)

    # ---------------------------------------------- REFRESH THE SCREEN -------------------------------------------

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
