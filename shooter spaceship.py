

from typing import Any
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
        def __init__(self,player_image,player_speed,player_x,player_y, size_x, size_y):
                super().__init__()
                self.image = transform.scale(image.load(player_image), (size_x, size_y))
                self.speed = player_speed
                self.rect = self.image.get_rect()
                self.rect.x = player_x
                self.rect.y = player_y
                self.size_x = size_x
                self.size_y = size_y
        def reset(self):
                window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
        def update(self):
                keys_pressed = key.get_pressed()
                if keys_pressed[K_LEFT]:
                        self.rect.x -= self.speed
                if keys_pressed[K_RIGHT]:
                        self.rect.x += self.speed
                if keys_pressed[K_SPACE]:
                        ship.fire()
                        shot.play()            
        def fire(self):
                bullet = Bullet("bullet.png", -15, self.rect.centerx, self.rect.top, 15, 20)
                bullets.add(bullet)
lost = 0
score = 0
maxlost = 3
goal = 10
class enemy(GameSprite):
        def update(self):
                self.rect.y += self.speed
                global lost
                if self.rect.y > win_height:
                        self.rect.x = randint(80,win_width - 80)     
                        self.rect.y = 0
                        lost = lost + 1



class Bullet(GameSprite):
        def update(self):
                self.rect.y += self.speed
                if self.rect.y < 0:
                        self.kill()




font.init()
style = font.Font(None, 36)

win = style.render('Wygrana.', True, (255,255,255))
przegrana = style.render('Przegrana', True, (255,0,0))



win_width = 700
win_height = 500
window = display.set_mode(
    (win_width, win_height)
)
display.set_caption("The Shooter")
background = transform.scale(
    image.load("galaxy.jpg"),
    (win_width, win_height)
)
monsters = sprite.Group()
for a in range(1,6):
        monster = enemy('ufo.png', randint(1,5) ,randint(80, win_width - 80), -40, 80, 50 )
        monsters.add(monster)
bullets = sprite.Group()

ship = Player("rocket.png",10,5, win_height - 100, 80, 100)







mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shot = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
finish = False
game = True
while game:
        window.blit(background,(0,0))
        text_lose = style.render(
        "Missed:" + str(lost), 1, (255,255,255)
        )
        window.blit(text_lose, (10,20))
        
        for e in event.get():
                if e.type == QUIT:
                        game = False
                elif e.type == KEYDOWN:
                        if e.type == K_SPACE:
                                ship.fire()
                                shot.play()

        if finish != True:
                
                ship.update()
                monsters.update()
                bullets.update()
                ship.reset()
                bullets.draw(window)
                monsters.draw(window)
                collisions = sprite.groupcollide(monsters, bullets, True, True)
                for i in collisions:
                        score += 1
                        monster = enemy('ufo.png', randint(1,5) ,randint(80, win_width - 80), -40, 80, 50 )
                        monsters.add(monster)
                if sprite.spritecollide(ship, monsters, False) or lost >= maxlost:
                        finish = True
                        window.blit(przegrana, (200, 200))
                if score >= goal:
                        finish = True
                        window.blit(win, (200, 200))

                display.update()
                
        


        
                
        

        clock.tick(FPS)








