from pygame import *

#parent class for sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#child class for the player
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

#child class for the enemy
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

#child class for the walls
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1 #color_1, color_2, color_3 refers to the RGB color
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width 
        self.height = wall_height

        self.image = Surface((self.width, self.height)) #Surface will draw a rectangle for you
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect() #get_rect is how we get the small rect positions (x,y)
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        # window.blit(self.image, (self.rect.x, self.rect.y))
        draw.rect(window, (self.color_1, self.color_2, self.color_3), 
                  (self.rect.x, self.rect.y, self.width, self.height))


#Game scene:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

#Game characters:
packman = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

# Words
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

#Wall
w1 = Wall (232, 235, 52, 100, 20, 450, 10)
w2 = Wall (232, 235, 52, 100, 20, 10, 330)
w3 = Wall (232, 235, 52, 210, 130, 10, 350)
w4 = Wall (232, 235, 52, 315, 20, 10, 330)
w5 = Wall (232, 235, 52, 450, 130, 10, 350)
w6 = Wall (232, 235, 52, 100, 470, 350, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

#music
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background,(0, 0))
        packman.update()
        monster.update()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()

        # losing condition
        if sprite.collide_rect(packman, monster):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        # Checking if the player touched the wall
        if (sprite.collide_rect(packman, w1) or sprite.collide_rect(packman, w2) or 
            sprite.collide_rect(packman, w3) or sprite.collide_rect(packman, w4) or 
            sprite.collide_rect(packman, w5) or sprite.collide_rect(packman, w6)):
            packman.rect.x = 5
            packman.rect.y = win_height - 80
    
        # winning condition
        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()


        packman.reset()
        monster.reset()
        final.reset()

    display.update()
    clock.tick(FPS)
