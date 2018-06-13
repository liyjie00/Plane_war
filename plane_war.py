import pygame
from pygame.locals import *
import time
x = 480
y = 852
timer = 0


class BasePlane:
    def __init__(self, screen, pos_x, pos_y, imagePos):
        self.x = pos_x
        self.y = pos_y
        self.screen = screen
        self.image = pygame.image.load(imagePos)
        self.image_x, self.image_y = self.image.get_size()
        self.bullet_list = []

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

        for bullet in self.bullet_list:
            bullet.display()

            if bullet.judge():
                bullet.move()
            else:
                self.bullet_list.remove(bullet)
        # print(self.bullet) # for test


class Plane(BasePlane):
    def __init__(self, screen):
        BasePlane.__init__(self, screen, 210, 700, './feiji/hero1.png')

    # keyboard control
    # def move(self, direction):
        # global x, y
        # if direction == 0 and self.x > 5:
        #     self.x -= 5
        # elif direction == 1 and self.x < x - self.image_x - 5:
        #     self.x += 5
        # elif direction == 2 and self.y > 5:
        #     self.y -= 5
        # elif direction == 3 and self.y < y - self.image_y - 5:
        #     self.y += 5

    # mouse control
    def move(self):
        self.x, self.y = pygame.mouse.get_pos()
        # 获取鼠标位置
        self.x -= self.image.get_width() / 2
        self.y -= self.image.get_height() / 2

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x + 8, self.y + 10, './feiji/bullet.png'))
        self.bullet_list.append(Bullet(self.screen, self.x + 72, self.y + 10, './feiji/bullet.png'))


class Enemy(BasePlane):
    def __init__(self, screen):
        BasePlane.__init__(self, screen, 0, 0, './feiji/enemy0.png')
        self.move_direction = True

    def move(self):
        global x, y

        if self.move_direction:
            self.x += 3
        else:
            self.x -= 3

        if self.x > x - self.image_x - 3:
            self.move_direction = False
        elif self.x < 0:
            self.move_direction = True

    def fire(self):
        if timer % 31 == 0:
            self.bullet_list.append(EnemyBullet(self.screen, self.x + 15, self.y + 36, './feiji/bullet1.png'))


class Bullet:
    def __init__(self, screen, x, y, bullet_image):
        self.x = x
        self.y = y
        self.screen = screen
        self.image = pygame.image.load(bullet_image)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 20

    def judge(self):
        if self.y > 0:
            return True
        else:
            return False


class EnemyBullet(Bullet):
    def move(self):
        self.y += 10

    def judge(self):
        if self.y < y:
            return True
        else:
            return False


def key_control(hero, key_state):
    # get event
    for event in pygame.event.get():

        # check if quit is clicked
        if event.type == QUIT:
            print("exit")
            exit()
        # check if it is keyboard event
        elif event.type == KEYDOWN:
            # check if the key is a or left
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                key_state[0] = 1
            # check if the key is d or right
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                key_state[1] = 1
            elif event.key == K_w or event.key == K_UP:
                print('right')
                key_state[2] = 1
            elif event.key == K_s or event.key == K_DOWN:
                print('right')
                key_state[3] = 1
            # check if the key is space
            elif event.key == K_SPACE:
                print('space')
                key_state[4] = 1
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_LEFT:
                key_state[0] = 0
            # check if the key is d or right
            elif event.key == K_d or event.key == K_RIGHT:
                key_state[1] = 0
            elif event.key == K_w or event.key == K_UP:
                key_state[2] = 0
            elif event.key == K_s or event.key == K_DOWN:
                key_state[3] = 0
            elif event.key == K_SPACE:
                key_state[4] = 0


def main():
    global timer
    # 1. create a window
    screen = pygame.display.set_mode((x, y), 0, 32)
    pygame.display.set_caption('Plane War ver1.0')

    # 2. get the background image
    background = pygame.image.load('./feiji/background.png')

    # 3. create a plane object
    enemy_list = []
    hero = Plane(screen)

    key_state = [0,0, 0, 0, 0]

    while True:
        if timer % 119 == 0 and len(enemy_list) < 5:
            enemy_list.append(Enemy(screen))
            print(enemy_list)

        screen.blit(background, (0, 0))

        hero.display()
        for enemy in enemy_list:
            enemy.display()
            enemy.fire()
            enemy.move()

        pygame.display.update()

        key_control(hero, key_state)

        # keyboard control
        # for direction in range(4):
        #     if key_state[direction] == 1:
        #         hero.move(direction)

        # mouse control
        if key_state[4] == 1:
            hero.move()

        if timer % 9 == 0:
            hero.fire()
        time.sleep(0.01)
        timer += 1


if __name__ == "__main__":
    main()


