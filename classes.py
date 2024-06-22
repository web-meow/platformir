import pygame

w = 1200
h = 800

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('images/player.png').convert_alpha()
        self.xvel = 0
        self.rectx = x
        self.recty = y
        self.yvel = 0
        self.onGround = False
        self.rect = self.image.get_rect(topleft=(self.rectx, self.recty))
        self.jump = False
        self.jump_count = 40
        self.speed = 5
        self.breath = 200
        self.hp=500
    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:
                self.yvel = -self.jump_count

        if left:
            self.xvel = -self.speed

        if right:
            self.xvel = self.speed

        if not (left or right):
            self.xvel = 0

        if not self.onGround:
            self.yvel += 3

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        if self.breath < 200:
            self.breath += 1
    def collide(self, xvel, yvel, ground):
        for g in ground:
            if pygame.sprite.collide_rect(self, g) and isinstance(g, Platform):
                if xvel > 0:
                    self.rect.right = g.rect.left
                if xvel < 0:
                    self.rect.left = g.rect.right

                if yvel > 0:
                    self.rect.bottom = g.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = g.rect.bottom + 5
                    self.yvel = 0
            if pygame.sprite.collide_rect(self, g) and isinstance(g, Water):
                if yvel > 0:
                    self.rect.centery = g.rect.centery
                    self.onGround = True
                    self.yvel = 0
                elif self.breath > -1:
                    g.in_water(self)
                elif self.hp > 0:
                    self.hp -= 1
            if self.hp < 100:
                self.kill()
    def collide_items(self, lst):
        return self.rect.collidelist(lst)



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if y != h and y < h:
            self.image = pygame.image.load('images/platform_sm.png').convert_alpha()
            self.rect = self.image.get_rect(center=(x, y-100))
        else:
            self.image = pygame.image.load('images/platform.png').convert_alpha()
            self.rect = self.image.get_rect(center=(x, y))



class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/water.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.image.set_alpha(180)
    def in_water(self, player):
        player.breath -= 1



class Items(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        if self.item_type == 'mouse':
            self.image = pygame.image.load('images/mouse.png')
        else:
            self.image = pygame.image.load('images/fish.png')
        self.rect = self.image.get_rect(center=(x, y))
    def collision(self, player):
        if self.rect.colliderect(player):
            if self.item_type == 'mouse':
                player.speed += 2
            else:
                player.breath += 50
            self.kill()



class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect((0, 0), (width, height))

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)



class Health(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/heart.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))



class Dog (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rectx = x
        self.recty = y
        self.onGround = False
        self.speed = 10
        self.image = pygame.image.load('images/dog.png')
        self.rect = self.image.get_rect(bottomleft=(self.rectx, self.recty-20))
        self.walk_count = -700
    def update(self, player):
        if self.walk_count >= -700 and self.walk_count < 0:
            self.image = pygame.image.load('images/dog_right.png')
            self.rect.x += self.speed
            self.walk_count += 10
        elif self.walk_count >= 0 and self.walk_count < 700:
            self.image = pygame.image.load('images/dog.png')
            self.rect.x -= self.speed
            self.walk_count += 10
        if self.walk_count == 700:
            self.walk_count = -700
        if self.rect.colliderect(player):
            player.hp -= 5



class win_flag (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/win_flag.png')
        self.rect = self.image.get_rect(bottomleft=(x, y))
    def collision(self, player):
        return self.rect.colliderect(player)