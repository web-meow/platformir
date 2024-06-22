import pygame.sprite
from classes import *


# необходимые переменные
display = (w, h)
BACKGROUND_COLOR = '#85CCEF'
all_sprites = pygame.sprite.Group()
menu = pygame.sprite.Group()
mouse = pygame.sprite.Group()
fish = pygame.sprite.Group()
dogs = pygame.sprite.Group()
platforms = []

# схема уровня
level = ['                                                                                                                            ',
         '                                                                                                                            ',
         '                                                                                                                            ',
         '                                         !                                                                                  ',
         '                                  m      -------------                                                                      ',
         '               !               ---------                                                                                     ',
         '               ------------                                                                                   !             ^',
         '     m                                                  !                  m          ---                    -------------------',
         '--------------***f*******f****---****f************f****---------------   ------*****-      -   -  -   -   -*****************']


# функции выигриша, проигрыша и камеры
def win(Backgr_col, sc):
    sc.fill(Backgr_col)
    all_sprites.empty()
    sc.blit(pygame.image.load('images/dog_dobry.png'), (615, 375))

def game_over(screen, g_o):
    screen.fill((0, 0, 0))
    screen.blit(g_o, (500, 350))

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, width, height = camera
    l, t = -l + w / 2, -t + h / 2

    l = min(0, l)
    l = max(-(camera.width - w), l)
    t = max(-(camera.height - h), t)
    t = min(0, t)

    return pygame.Rect(l, t, width, height)

total_level_width = len(level[0]) * 64
total_level_height = len(level) * 100

def run_game():

    pygame.init()

    # создание окна и фона
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption('platformer')
    bg = pygame.Surface(display)
    bg.fill(BACKGROUND_COLOR)
    timer = pygame.time.Clock()
    running = True

    # создание игрока
    player = Player(0, 100)
    all_sprites.add(player)
    left = right = False
    up = False

    # Генерация уровня
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                platforms.append(pf)
                all_sprites.add(pf)
            elif col == '*':
                wtr = Water(x, y)
                platforms.append(wtr)
                all_sprites.add(wtr)
            x += 63
        y += 100
        x = 0

    # Генерация предметов на уровне
    x = y = 0
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "m":
                m = Items('mouse', x, y-30)
                mouse.add(m)
                all_sprites.add(m)
            elif col == 'f':
                f = Items('fish', x-64, y-50)
                fish.add(f)
                all_sprites.add(f)
                wtr = Water(x, y)
                platforms.append(wtr)
                all_sprites.add(wtr)
            elif col == '^':
                flag = win_flag(x, y)
                all_sprites.add(flag)
            x += 63
        y += 100
        x = 0

    # Генерация псин
    x = y = 0
    for row in level:
        for col in row:
            if col == "!":
                d = Dog(x, y)
                dogs.add(d)
                all_sprites.add(d)
            x += 63
        y += 100
        x = 0


    camera = Camera(camera_configure, total_level_width, total_level_height)

    while running:
        timer.tick(60)
        screen.blit(bg, (0, 0))
        for s in all_sprites:
            screen.blit(s.image, camera.apply(s))

        # меню
        menu_font = pygame.font.Font('font/Nevduplenysh-Regular.otf', 46)
        pl_sp = menu_font.render(F'speed: {player.speed}', True, (0, 0, 0))
        pl_br = menu_font.render(F'breath: {player.breath}', True,  (0, 0, 0))
        win_t = menu_font.render('Вы выйграли! Скушайте торт.', True, (255, 255, 255))
        g_o = menu_font.render('Вы проиграли :(', True, (255, 255, 255))

        screen.blit(pl_sp, (10, 10))
        screen.blit(pl_br, (10, 50))

        h_x = 500
        for h in range(player.hp//100):
            heart = Health(h_x, 10)
            screen.blit(heart.image, (h_x, 10))
            h_x += 35

        # проверка столкновений с предметами
        for i_m in mouse:
            i_m.collision(player)
        for i_f in fish:
            i_f.collision(player)

        # ересечиение с финальным флажком
        if flag.collision(player):
            win(BACKGROUND_COLOR, screen)
            screen.blit(player.image, (425, 400))
            screen.blit(heart.image, (550, 400))
            screen.blit(win_t, (450, 250))

        # варианты конца игры
        if player.hp < 100 or player.rect.y > 900:
            game_over(screen, g_o)


        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True

            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up = False
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False

        # Обновление спрайтов и камеры
        camera.update(player)
        player.update(left, right, up, platforms)
        for i_d in dogs:
            i_d.update(player)

if __name__ == "__main__":
    run_game()