import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 920, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("COSMIC DEFENDER")

# load image files
RED_SPACE_SHIP = pygame.image.load(os.path.join("resources", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("resources", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("resources", "pixel_ship_blue_small.png"))

# player controlled ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("resources", "pixel_ship_yellow.png"))

# load laser images
RED_LASER = pygame.image.load(os.path.join("resources", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("resources", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("resources", "pixel_laser_blue.png"))

# player ship laser
YELLOW_LASER = pygame.image.load(os.path.join("resources", "pixel_laser_yellow.png"))

# background image
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("resources", "background-black.png")), (WIDTH, HEIGHT))

class Ship: 
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down = 0


    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Alien(Ship):
    COLOUR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)}
    
    def __init__(self, x, y, colour, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOUR_MAP[colour]
        self.mask = pygame.mask.from_surface(self.ship_img)


    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5

    text_font = pygame.font.SysFont("sansserif", 40)

    aliens = []
    wave_length = 5
    e_vel = 1


    velocity = 7

    player = Player(300, 650)


    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BACKGROUND, (0,0))

        # create text
        life_label = text_font.render(f"Lives: {lives}", 1, (0, 0, 255))
        level_label = text_font.render(f"Level: {level}", 1, (0, 0, 255))

        WIN.blit(life_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for alien in aliens:
            alien.draw(WIN)

        player.draw(WIN)

        pygame.display.update()


    while run:
        clock.tick(FPS)

        if len(aliens) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                alien = Alien(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                aliens.append(alien)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + velocity > 0: #left
            player.x -= velocity    
        if keys[pygame.K_d] and player.x + velocity + player.get_width() < WIDTH: #right
            player.x += velocity  
        if keys[pygame.K_w]and player.y + velocity > 0: #up
            player.y -= velocity  
        if keys[pygame.K_s] and player.y + velocity + player.get_height() < HEIGHT: #down
            player.y += velocity  
        
        for alien in aliens:
            alien.move(e_vel)


        redraw_window() 

main()

# 10437