import pygame
from pygame.locals import *
from pygame.sprite import Group

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mario')

#define font + font colors
game_over_font = pygame.font.SysFont('Bauhaus 93', 80)
font_score = pygame.font.SysFont('Bauhaus 93', 40)
white = (255, 255, 255)
red = (255, 0, 0)

#define game variables
tile_size = 50
game_over = 0
main_menu = True
score = 0

#load images
bg_img = pygame.image.load('game/img/sky.png')
restart_img = pygame.image.load('game/img/restart.png')
start_img = pygame.image.load('game/img/start.png')
stop_img = pygame.image.load('game/img/stop.png')
game_over_img = pygame.image.load('game/img/game_over_alt.png')

## renders text on screen as image
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        #scaling the original images down to 1/4 size
        original_size = self.image.get_size()
        new_size = (original_size[0] // 2, original_size[1] // 2) 
        scaled_image = pygame.transform.scale(self.image, new_size)
        self.image = scaled_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    
    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        
        return action 

class Player():
    def __init__(self, x, y):
       self.reset(x, y)
       

    def update(self, game_over):
        dx = 0
        dy = 0

        if game_over == 0:
       
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -30
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            #check for collision
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check for collisions w/ enemies
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
            #check for collisions w/ spikes and lava
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            dead_image = pygame.image.load('game/img/ghost.png')
            self.image = pygame.transform.scale(dead_image, (65, 90))
            self.rect.y -= 5

        #draw player onto the screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

        return game_over

    def reset(self, x, y):
        img = pygame.image.load('game/img/panda.png')
        self.image = pygame.transform.scale(img, (65, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        grass_img = pygame.image.load('game/img/ground_grassy_1.png')
        brick_img = pygame.image.load('game/img/brick.png')
        cactus_img = pygame.image.load('game/img/cactus.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(brick_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(cactus_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size - 22)
                    enemy_group.add(enemy)
                if tile == 6:
                    spike = Spike(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    spike_group.add(spike)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    lava = Lava(col_count * tile_size, row_count * tile_size )
                    lava_group.add(lava)
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('game/img/enemy.png')
        scaled_image = pygame.transform.scale(self.image, (65, 85))
        self.image = scaled_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):

        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter)  > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Spike(pygame.sprite.Sprite):
   def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('game/img/spike_1.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lava(pygame.sprite.Sprite):
   def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('game/img/lava_1.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size ))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Coin(pygame.sprite.Sprite):
   def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('game/img/coin_gold.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

      
        

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 2, 0, 0, 1],
    [1, 0, 2, 2, 2, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 1, 1, 8, 8, 8, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

## player instance
player = Player(100, screen_height - 130)
## sprite groups
enemy_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
world = World(world_data)
## interface buttons
restart_button = Button(screen_width // 2 - 250, screen_height // 2 - 100, game_over_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2 - 100, start_img)
stop_button = Button(screen_width // 2 , screen_height // 2 - 100, stop_img)
score_count_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_count_coin)


### GAME LOOP
run = True
while run:

    clock.tick(fps)
    screen.blit(bg_img, (0, 0))
    
    if main_menu == True:
        if stop_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        
        if game_over == 0:
            enemy_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
            draw_text('X ' + str(score), font_score, white, ((tile_size // 2) + 15), ((tile_size // 2) - 10))
            
        enemy_group.update()
        enemy_group.draw(screen)
        spike_group.draw(screen)
        coin_group.draw(screen)
        lava_group.draw(screen)
        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                player.reset(100, screen_height - 130)
                game_over = 0
                score = 0

# draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()
