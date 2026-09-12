import pygame

# COLORS
colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}

# IMAGES 
background = pygame.image.load('Data/background.png')
cube_image = pygame.image.load('Data/cube.png')
blade_image = pygame.image.load('Data/blades.png')
logo = pygame.image.load('Data/Logo_3.png')
heart = pygame.image.load('Data/heart.png')
half_portal = pygame.image.load('Data/half_portal.png')
logo_resized = pygame.transform.scale(logo, (426, 240))
heart_resized = pygame.transform.scale(heart, (64, 64))

# SCREEN
screen_width = 1280
screen_height = 720

# CLASSES
class Player():
    def __init__(self, x, y, player_width, player_height):
        self.x = x
        self.y = y
        self.player_width = player_width
        self.player_height = player_height
        self.velocity = 10
        self.right = True
        self.left = False
        self.jump = False
        self.jump_height = 10.5
        self.jump_temp = 10.5
        self.hitbox = (self.x, self.y, player_width, player_height)

    def draw(self, window, player_width, player_height):
        window.blit(cube_image, (self.x, self.y))
        self.hitbox = (self.x, self.y, player_width, player_height)
        #pygame.draw.rect(window, colors['red'], self.hitbox, 1)

    def get_hit(self, x, y):
        self.jump = False
        self.jump_height = 10.5
        self.x = x
        self.y = y
        window.blit(text_heart_lose, (440, 150))
        pygame.display.update()
        pygame.time.delay(1000)

class Enemy_Blade():
    def __init__(self, x, y, enemy_width, enemy_height):
        self.x = x
        self.y = y
        self.enemy_width = enemy_width
        self.enemy_height = enemy_height
        self.hitbox = (self.x, self.y, self.enemy_width, self.enemy_height)

    def draw(self, window):
        window.blit(blade_image, (self.x, self.y))
        #pygame.draw.rect(window, colors['red'], self.hitbox, 1)

def redraw_game_window(window):
    window.blit(background, (0, 0))
    window.blit(logo_resized, (420, -50))
    if heart_count > 0:
        window.blit(heart_resized, (-10, -10))
    if heart_count > 1:
        window.blit(heart_resized, (35, -10))
    if heart_count > 2:
        window.blit(heart_resized, (80, -10))
    if heart_count > 3:
        window.blit(heart_resized, (125, -10))
    if heart_count > 4:
        window.blit(heart_resized, (170, -10))
    if not is_lost and not is_win:
        BLADE_1.draw(window)
        BLADE_2.draw(window)
        BLADE_3.draw(window)
        BLADE_4.draw(window)
        CUBE.draw(window, 60, 60)
    window.blit(half_portal, (1148, 354))
    if is_lost:
        window.blit(text_lose, (280, 350))
    elif is_win:
        window.blit(text_win, (440, 350))
    pygame.display.update()

# PLAYER AND ENEMIES
CUBE = Player(60, 469, 60, 60)
BLADE_1 = Enemy_Blade(220, 496, 59, 34)
BLADE_2 = Enemy_Blade(450, 496, 59, 34)
BLADE_3 = Enemy_Blade(700, 496, 59, 34)
BLADE_4 = Enemy_Blade(763, 496, 59, 34)
blade_list = [BLADE_1, BLADE_2, BLADE_3, BLADE_4]

# STATUS
win_x = 1148
heart_count = 5
is_lost = False
is_win = False

# STARTER
pygame.init()
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CUBE CRAFT")

# MUSIC - SOUNDTRACKS
pygame.mixer.music.load('Data/epic-battle-153400.mp3')
pygame.mixer.music.play(-1)
lose_sound = pygame.mixer.Sound('Data/Fail Sound Effect.wav')

# TEXT
font_minecraft = pygame.font.SysFont('Minecraft', 72, False, False)
text_heart_lose = font_minecraft.render("-1 heart", 1, colors['red'])
text_lose = font_minecraft.render("YOU LOST! LOOSER!", 1, colors['red'])
text_win = font_minecraft.render("YOU WON!", 1, colors['green'])

# GAME LOOP
clock = pygame.time.Clock()
is_running = True
while is_running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    if CUBE.x > win_x:
        is_win = True

    if heart_count > 0 and not is_win:

        for blade in blade_list:
            if CUBE.hitbox[1] < blade.hitbox[1] + blade.hitbox[3] and CUBE.hitbox[1] + CUBE.hitbox[3] > blade.hitbox[1]:
                if CUBE.hitbox[0] + CUBE.hitbox[2] > blade.hitbox[0] and CUBE.hitbox[0] < blade.hitbox[0] + blade.hitbox[2]:
                    CUBE.get_hit(60, 469)
                    heart_count -= 1
                    print("hit")
                    break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and CUBE.x < screen_width - CUBE.player_width - CUBE.velocity:
            CUBE.x += CUBE.velocity
            CUBE.right = True
            CUBE.left = False

        elif keys[pygame.K_LEFT] and CUBE.x > CUBE.velocity:
            CUBE.x -= CUBE.velocity
            CUBE.right = False
            CUBE.left = True

        if not CUBE.jump:
            if keys[pygame.K_SPACE]:
                CUBE.jump = True
        else:
            if CUBE.jump_temp >= CUBE.jump_height * (-1):
                if CUBE.jump_temp > 0:
                    CUBE.y -= (CUBE.jump_temp ** 2) * 0.5
                    CUBE.jump_temp -= 1
                else:
                    CUBE.y += (CUBE.jump_temp ** 2) * 0.5
                    CUBE.jump_temp -= 1
            else:
                CUBE.jump = False
                CUBE.jump_temp = CUBE.jump_height
    
    elif heart_count == 0:
        is_lost = True
        pygame.mixer.music.stop()
        lose_sound.play()

    redraw_game_window(window)

pygame.quit()