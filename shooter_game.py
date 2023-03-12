# Створи власний Шутер!

from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < w - 85:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx,
                        self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global score
        if self.rect.y > h:
            self.rect.y = -50
            self.rect.x = randint(20, w-100)
            score = score + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


w, h = 700, 500
mw = display.set_mode((w, h))
display.set_caption("Shooter")
background = transform.scale(image.load('galaxy.jpg'), (w, h))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


font.init()
text1 = font.Font(None, 36)
text2 = font.Font(None, 80)

win = text2.render("YOU WIN!", True, (138, 65, 5), (43, 240, 195))
lose = text2.render("ENEMY WIN!", True, (199, 60, 128), (249, 100, 30))
#!
text_name = text2.render("SHOOTER", True, (57, 190, 173), (40, 16, 70))
text_play = text2.render("PLAY - press 's'", True,
                         (57, 190, 173), (40, 16, 70))
text_exit = text2.render("EXIT - press 'e'", True,
                         (57, 190, 173), (40, 16, 70))
#!

player = Player("rocket.png", 200, h-100, 80, 100, 5)
monsters = sprite.Group()
bullets = sprite.Group()

score = 0
killed = 0
goal = 10
max_lost = 3


def respawn_enemy():
    monster = Enemy("ufo.png", randint(
        20, w-100), -50, 80, 50, randint(1, 4))
    monsters.add(monster)


def menu():
    global w, h
    background_menu = transform.scale(image.load('menu.jpg'), (w, h))
    menu = True
    while menu:
        mw.blit(background_menu, (0, 0))
        for e in event.get():
            if e.type == QUIT:
                menu = False
            if e.type == KEYDOWN:
                if e.key == K_s:
                    menu = False
                    game()
                if e.key == K_e:
                    menu = False

        mw.blit(text_name, ((w/2)-100, 70))
        mw.blit(text_play, ((w/2)-150, 150))
        mw.blit(text_exit, ((w/2)-150, 210))

        display.update()


def game():
    global score, killed, goal, max_lost

    for i in range(1, 6):
        respawn_enemy()

    clock = time.Clock()
    finish = True
    game = True
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()
                    fire_sound.play()

        if not finish:
            mw.blit(background, (0, 0))
            player.update()
            bullets.update()  # !
            player.reset()
            monsters.draw(mw)
            bullets.draw(mw)  # !
            monsters.update()

            text_killed = text1.render(
                "Рахунок " + str(killed), 1, (255, 0, 0), (255, 255, 255))
            mw.blit(text_killed, (20, 20))

            text_lost = text1.render(
                "Пропущено "+str(score), 1, (135, 145, 240), (255, 255, 255))
            mw.blit(text_lost, (20, 50))

            if sprite.spritecollide(player, monsters, False) or score >= max_lost:
                mw.blit(lose, (150, 200))
                display.update()
                time.delay(3000)
                finish = True
                game = False
                menu()

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for collide in collides:
                killed += 1
                respawn_enemy()

            if killed >= goal:
                finish = True
                mw.blit(win, (150, 200))
                display.update()
                time.delay(3000)
        else:
            #!time.delay(3000)
            finish = False
            killed = 0
            score = 0
            for bullet in bullets:
                bullet.kill()
            for monster in monsters:
                monster.kill()
            for i in range(1, 6):
                respawn_enemy()

        display.update()
        clock.tick(30)


menu()
