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


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    
    def damage(self, obj):
        return hit(self, obj)

class Ship: 

    COOLDOWN = 30

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0


    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.damage(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1  

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else: 
                for obj in objs:
                    if laser.damage(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))


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

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    

def hit(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None




def main():
    run = True
    FPS = 60
    level = 0
    lives = 5

    text_font = pygame.font.SysFont("sansserif", 40)
    title_font = pygame.font.SysFont("sansserif", 200)

    aliens = []
    wave_length = 5
    e_vel = 1

    l_vel = 5
    velocity = 7

    player = Player(300, 630)


    clock = pygame.time.Clock()

    lose = False
    lose_count = 0


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

        if lose:
            lose_msg = title_font.render("GAME OVER", 1, (255,0,0))
            WIN.blit(lose_msg, (WIDTH/2 - lose_msg.get_width()/2, 350))

        pygame.display.update()


    while run:
        clock.tick(FPS)

        redraw_window() 

        if lives <= 0 or player.health <= 0:
            lose = True
            lose_count += 1

        if lose:
            if lose_count > FPS * 3:
                run = False
            else:
                continue

        if len(aliens) == 0:
            level += 1
            wave_length += 5
            player.health = 100
            for i in range(wave_length):
                alien = Alien(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                aliens.append(alien)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + velocity > 0: #left
            player.x -= velocity    
        if keys[pygame.K_d] and player.x + velocity + player.get_width() < WIDTH: #right
            player.x += velocity  
        if keys[pygame.K_w]and player.y + velocity > 0: #up
            player.y -= velocity  
        if keys[pygame.K_s] and player.y + velocity + player.get_height() + 15 < HEIGHT: #down
            player.y += velocity  
        if keys[pygame.K_SPACE]: #shoot
            player.shoot() 

        
        for alien in aliens[:]:
            alien.move(e_vel)
            alien.move_lasers(l_vel, player)

            if random.randrange(0, 2*60) == 1:
                alien.shoot()

            if hit(alien, player):
                player.health -= 10
                aliens.remove(alien)
            elif alien.y + alien.get_height() > HEIGHT:
                lives -= 1
                aliens.remove(alien)

        player.move_lasers(-l_vel, aliens)


def menu():
    menu_font = pygame.font.SysFont("sansserif", 120)
    run = True
    while run:
        WIN.blit(BACKGROUND, (0,0))
        title_text = menu_font.render("Press mouse to start!", 1, (255,255,255))
        WIN.blit(title_text, (WIDTH / 2 - title_text.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

menu()

# 137:00