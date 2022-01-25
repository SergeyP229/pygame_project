import pygame
from screeninfo import get_monitors
import random


class Background(pygame.sprite.Sprite):
    def __init__(self, layer):
        super().__init__(background_sprite)
        self.x = -200
        self.y = 0
        if layer == 1:
            self.y -= HEIGHT
        self.image = BACKGROUND_IMAGE
        self.image = pygame.transform.scale(self.image, (WIDTH + 400, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.add(background_sprite)

    def update(self):
        self.rect = self.rect.move(0, 1)
        self.y = self.rect.y
        if self.rect.y == HEIGHT:
            background_sprite.remove(self)
            Background(1)
                        

class Bonus(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__(bonus_sprite)
        self.x = random.randint(40, WIDTH - 40)
        self.y = 0
        self.object_type = bonus_dict[number]
        self.image = BONUS_IMAGES[number - 1]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.mask = pygame.mask.from_surface(self.image)
        self.add(bonus_sprite)

    def update(self):
        self.rect = self.rect.move(0, 2)
        self.y = self.rect.y
        if pygame.sprite.collide_mask(self, player):
            if self.object_type == 'triple_shoot':
                player.triple_shoot = True
            elif self.object_type == 'shield':
                player.shield = True
            elif self.object_type == 'speed_boost':
                player.speed_boost = True
            elif self.object_type == 'hp_bonus':
                player.hits += round(player.max_hits * 0.3)
            elif self.object_type == 'super_shoot':
                player.super_shoot = 5
            if GAME_MODE not in ('over', 'win'):
                bonus_sound.play()
            bonus = None
            bonus_sprite.remove(self)   


class Meteor(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, speed_x=None, speed_y=None):
        super().__init__(meteors_sprite)
        if x or y or speed_x or speed_y:
            self.start_x = x
            self.start_y = y
            self.x = x
            self.y = y
            self.speed_x = speed_x
            self.speed_y = speed_y
        else:
            self.x = random.randint(40, WIDTH - 40)
            self.y = 0
            self.speed_x = random.choice([-2, -1, 1, 2])
            self.speed_y = random.randint(1, 4)
        type_prefab = random.randint(0, 9)
        self.image = METEOR_IMAGES[type_prefab]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.mask = pygame.mask.from_surface(self.image)
        self.add(meteors_sprite)


    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)
        self.y = self.rect.y
        if self.rect.y > HEIGHT or self.rect.x > WIDTH:
            if GAME_MODE == 'draw_level':
                self.rect.x = self.start_x
                self.rect.y = self.start_y
            else:
                meteors_sprite.remove(self)
        if pygame.sprite.collide_mask(self, player):
            player.get_damage(50)
            meteors_sprite.remove(self)
            Animation(self.rect.x, self.rect.y, player.rect.x, player.rect.y)
            if GAME_MODE == 'draw_level':
                Meteor(self.start_x, self.start_y, self.speed_x, self.speed_y)
        for i in enemies_sprite:
            if pygame.sprite.collide_mask(self, i):
                meteors_sprite.remove(self)
                self.kill()
                enemies_sprite.remove(i)
                i.kill()
                Animation(i.rect.x, i.rect.y, self.rect.x, self.rect.y)
        for i in meteors_sprite:
            if i is not self and pygame.sprite.collide_mask(self, i):
                Animation(self.rect.x, self.rect.y, i.rect.x, i.rect.y)
                self.kill()
                i.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = WIDTH // 20
        self.hits = 200
        self.max_hits = self.hits
        self.speed = 3
        image = pygame.image.load("other/player.png")
        image = pygame.transform.scale(image, (self.size, self.size))
        self.image_shield = pygame.image.load("other/shield_effect.png")
        self.image_shield = pygame.transform.scale(self.image_shield, (self.size, self.size))
        self.image_default = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.add(players)
        self.triple_shoot = False
        self.speed_boost = False
        self.shield = False
        self.super_shoot = 0
        self.can_moves = {'w': True, 'a': True, 's': True, 'd': True}

    def move(self, x, y):
        for i in obst_sprite:
            if pygame.sprite.collide_mask(self, i):
                if i.rect.x >= self.rect.x:
                    self.can_moves['d'] = False
                else:
                    self.can_moves['d'] = True
                if i.rect.x <= self.rect.x:
                    self.can_moves['a'] = False
                else:
                    self.can_moves['a'] = True
                if i.rect.y >= self.rect.y:
                    self.can_moves['s'] = False
                else:
                    self.can_moves['s'] = True
                if i.rect.y <= self.rect.y:
                    self.can_moves['w'] = False
                else:
                    self.can_moves['w'] = True
                break
        else:
            for i in self.can_moves:
                self.can_moves[i] = True
        can_move = True
        if y < 0 and not self.can_moves['w']:
            can_move = False
        if y > 0 and not self.can_moves['s']:
            can_move = False              
        if x < 0 and not self.can_moves['a']:
            can_move = False
        if x > 0 and not self.can_moves['d']:
            can_move = False
        if can_move:
            if self.speed_boost:
                x *= 2
                y *= 2
            self.x += x
            self.y += y
            if self.x > WIDTH - self.size:
                self.x = WIDTH - self.size
            elif self.x < 0:
                self.x = 0
            elif self.y > HEIGHT - self.size:
                self.y = HEIGHT - self.size
            elif self.y < 0:
                self.y = 0
            self.rect.x = self.x
            self.rect.y = self.y

    def shoot(self, bulllet_type):
        global can_shoot
        if can_shoot:
            if GAME_MODE not in ('over', 'win'):
                player_shoot_sound.play()
            can_shoot = False
            if self.triple_shoot:
                Bullet(bulllet_type, self.x + self.size / 2 - 5, self.y)
                Bullet(bulllet_type, self.x + self.size / 2 - 35, self.y + 15)
                Bullet(bulllet_type, self.x + self.size / 2 + 25, self.y + 15)
            else:
                Bullet(bulllet_type, self.x + self.size / 2 - 5, self.y)
            
    def get_damage(self, damage):
        if GAME_MODE not in ('over', 'win'):
            damage_sound.play()
        if self.shield:
            self.shield = False
        else:
            if self.hits >= damage:
                self.hits -= damage
            else:
                self.hits = 0

    def update(self):
        if self.shield:
            self.image = self.image_shield
        else:
            self.image = self.image_default

            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type, x, y):
        super().__init__(bullets_sprite)
        self.x = x
        self.y = y
        if bullet_type == 'default':
            self.image = PLAYER_BULLET_SHOOT
            self.image = pygame.transform.scale(self.image, (20, 20))
        else:
            self.image = pygame.image.load('bullets/super.png')
            self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)
        self.add(bullets_sprite)
        self.bullet_type = bullet_type

    def update(self):
        self.rect = self.rect.move(0, -6)
        self.y = self.rect.y
        if self.y < 0:
            bullets_sprite.remove(self)
        for i in meteors_sprite:
            if pygame.sprite.collide_mask(self, i):
                Animation(self.rect.x, self.rect.y, i.rect.x, i.rect.y)
                if GAME_MODE == 'draw_level':
                    i.rect.x = i.start_x
                    i.rect.y = i.start_y
                else:
                    meteors_sprite.remove(i)
                if self.bullet_type == 'default':
                    bullets_sprite.remove(self)
        for i in obst_sprite:
            if pygame.sprite.collide_mask(self, i):
                obst_sprite.remove(self)
                self.kill()
           

class Enemy_shoot(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        super().__init__(enemy_bullets)
        self.x = x + player.size // 2
        self.y = y + player.size // 2
        self.damage = level * 20
        self.image = ENEMIES_SHOOT[level - 1]
        self.image = pygame.transform.scale(self.image, (10, 40))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)
        self.add(enemy_bullets)
        
    def update(self):
        self.rect = self.rect.move(0, 6)
        self.y = self.rect.y
        if self.y > HEIGHT:
            enemy_bullets.remove(self)
        if pygame.sprite.collide_mask(self, player):
            enemy_bullets.remove(self)
            player.get_damage(self.damage)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, moving=True, x=None, y=None, level=None):
        super().__init__(enemies_sprite)
        self.moving = moving
        self.size = WIDTH // 20
        if x and y:
            self.x = x
            self.y = y
            self.level = level
        else:
            self.x = random.randint(self.size + 10, WIDTH - self.size - 10)
            self.y = random.randint(10, HEIGHT // 5)
            self.level = random.randint(1, 5)
        self.image = ENEMY_IMAGES[self.level - 1]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)
        self.add(enemies_sprite)
        self.moving_x = random.choice([-1, 1])
        self.moving_y = random.choice([-1, 1])

    def update(self):
        global points
        if self.moving:
            if self.rect.x < 40 or self.rect.x > WIDTH - 40 - self.size:
                self.moving_x *= -1
            if self.rect.y < 40 or self.rect.y > HEIGHT - 40 - self.size:
                self.moving_y *= -1
            if random.choice([False] * 200 + [True]):
                self.moving_x *= -1
            if random.choice([False] * 200 + [True]):
                self.moving_y *= -1
            self.rect = self.rect.move(self.level * self.moving_x, -1 * self.level * self.moving_y)
            self.y = self.rect.y
        for i in bullets_sprite:
            if pygame.sprite.collide_mask(self, i):
                player.super_shoot += 1
                self.kill()
                if i.bullet_type == 'default':
                    i.kill()
                Animation(self.rect.x, self.rect.y, i.rect.x, i.rect.y)
                enemies_sprite.remove(i)
                bullets_sprite.remove(self)
                points += 5 * self.level
        for i in enemies_sprite:
            if i is not self and pygame.sprite.collide_mask(self, i):
                self.kill()
                Animation(self.rect.x, self.rect.y, i.rect.x, i.rect.y)
        if random.choice([False] * 200 + [True]):
            self.shoot()
        if pygame.sprite.collide_mask(self, player):
            Animation(self.rect.x, self.rect.y, player.rect.x, player.rect.y)
            player.get_damage(100)
            enemies_sprite.remove(self)
            self.kill()
            
    def shoot(self):
        if GAME_MODE != 'over':
            Enemy_shoot(self.rect.x, self.y, self.level)
            if GAME_MODE not in ('over', 'win'):
                enemy_shoot_sound.play()
        
        
class Animation(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(anim_sprite)
        if GAME_MODE not in ('over', 'win'):
            exp_sound.play()
        self.x = max([x1, x2]) - 50
        self.y = max([y1, y2]) - 50
        self.image = ANIM_IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.add(anim_sprite)
        self.timer = 0

    def update(self):
        if self.timer == 50:
            anim_sprite.remove(self)
        else:
            self.image = ANIM_IMAGES[self.timer // 10]
            self.timer += 1
            
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(obst_sprite)
        self.x = x
        self.y = y
        self.image = OBST_IMAGES[random.randint(0, 3)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.add(obst_sprite)
        
        
class Over(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(over_sprite)
        self.x = x
        self.y = y
        self.image = OVER_IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.add(over_sprite)
        self.timer = 0
        
    def update(self):
        global GAME_MODE
        self.timer += 1
        if self.timer == 540:
            self.timer = 0
        self.image = OVER_IMAGES[int(self.timer // 1.5 % 10)]
        if pygame.sprite.collide_mask(self, player):
            player.kill()
            draw_win_window(LEVEL)
            GAME_MODE = 'win'         
        

def drawing():
    pygame.mouse.set_visible(False)
    draw_background()
    enemies_manager()
    draw_hits_and_points()
    players.draw(screen)
    bullets_sprite.draw(screen)
    meteors_manager()
    if hint:
        show_hint()
    bonus_sprite.draw(screen)
    enemy_bullets.draw(screen)
    anim_sprite.draw(screen)


def draw_intro():
    global running, GAME_MODE
    pygame.mouse.set_visible(True)
    player.hits = player.max_hits
    draw_background()
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 2 - WIDTH // 12, HEIGHT // 2, WIDTH // 6, HEIGHT // 10))
    font = pygame.font.Font(None, WIDTH // 11)
    text = font.render('PLAY', True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - WIDTH // 12, HEIGHT // 2))
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 2 - WIDTH // 12, HEIGHT // 2 + HEIGHT // 8, WIDTH // 6, HEIGHT // 10))
    font = pygame.font.Font(None, WIDTH // 16)
    text = font.render('LEVELS', True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - WIDTH // 12, HEIGHT // 2 + HEIGHT // 7))
    font = pygame.font.Font(None, WIDTH // 30)
    text = font.render('Made by Prosvetov Sergey', True, (255, 255, 255))
    screen.blit(text, (30, HEIGHT - 70))
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 2 - WIDTH // 12, HEIGHT // 2 + HEIGHT // 4, WIDTH // 6, HEIGHT // 10))
    font = pygame.font.Font(None, WIDTH // 12)
    text = font.render('EXIT', True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - WIDTH // 14, HEIGHT // 2 + HEIGHT // 4))
    file = open('hints.txt', encoding='utf-8')
    file_text = file.read().split('\n')
    for i in range(len(file_text)):
        font = pygame.font.Font(None, WIDTH // 20)
        text = font.render(file_text[i], True, (0, 255, 255))
        screen.blit(text, (WIDTH // 100, i * HEIGHT // 10))
    if coords:
        x, y = coords
        if WIDTH // 2 - WIDTH // 12 <= x <= WIDTH // 2 - WIDTH // 12 + WIDTH // 6 and \
                HEIGHT // 2 <= y <= HEIGHT // 2 + HEIGHT // 10:
            GAME_MODE = 'game'
            pygame.mouse.set_visible(False)
        elif WIDTH // 2 - WIDTH // 12 <= x <= WIDTH // 2 - WIDTH // 12 + WIDTH // 6 and \
                HEIGHT // 2 + HEIGHT // 4 <= y <= HEIGHT // 2 + HEIGHT // 4 + HEIGHT // 10:
            running = False
        elif WIDTH // 2 - WIDTH // 12 <= x <= WIDTH // 2 - WIDTH // 12 + WIDTH // 6 and \
                HEIGHT // 2 + HEIGHT // 8 <= y <= HEIGHT // 2 + HEIGHT // 8 + HEIGHT // 10:
            GAME_MODE = 'draw_level_choice'


def draw_background():
    background_sprite.draw(screen)
    for i in background_sprite:
        i.update()


def meteors_manager():
    global spawn_meteor
    if spawn_meteor:
        Meteor()
        spawn_meteor = False
    for i in meteors_sprite:
        i.update()
    meteors_sprite.draw(screen)


def enemies_manager():
    global spawn_enemy
    if spawn_enemy:
        Enemy()
        spawn_enemy = False
    for i in enemies_sprite:
        i.update()
    enemies_sprite.draw(screen)


def draw_hits_and_points():
    font = pygame.font.Font(None, 100)
    if player.hits:
        if player.hits / player.max_hits >= 0.7:
            color = (0, 255, 0)
        elif 0.3 <= player.hits / player.max_hits < 0.7:
            color = (255, 255, 0)
        elif player.hits / player.max_hits < 0.3:
            color = (255, 0, 0)
    else:
        color = (0, 0, 0)
    k2 = player.hits / player.max_hits
    if k2 > 1:
        plus_hp = True
        k2 = 1
    else:
        plus_hp = False
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH / 4, HEIGHT / 25, WIDTH / 4, HEIGHT / 15), 3)
    pygame.draw.rect(screen, color, (WIDTH / 4 + 3, HEIGHT / 25 + 3,
                     (WIDTH / 4 - 6) * (k2), HEIGHT / 15 - 6))
    text = font.render(f'health: {player.hits}', True, color)
    screen.blit(text, (WIDTH / 20, HEIGHT / 20))
    if plus_hp:
        text = font.render('+', True, color)
        screen.blit(text, (WIDTH / 2, HEIGHT / 23))
    text = font.render(f'points: {points}', True, (255, 255, 255))
    screen.blit(text, (WIDTH - WIDTH / 5, HEIGHT / 20))
    text = None
    if player.shield:
        text = font.render('shield is active', True, (255, 0, 255))
    elif player.triple_shoot:
        text = font.render('triple shoot is active', True, (255, 0, 255))
    elif player.speed_boost:
        text = font.render('speed_boost is active', True, (255, 0, 255))
    if text:
        k = seconds / 20
        if k == 1:
            k = 0
        screen.blit(text, (WIDTH // 20, HEIGHT - HEIGHT / 5))
        pygame.draw.rect(screen, (255, 255, 255), ((WIDTH / 20, HEIGHT - HEIGHT / 9), (600, 100)), 3)
        pygame.draw.rect(screen, (255, 0, 255), ((WIDTH / 20 + 3, HEIGHT - HEIGHT / 9 + 3), (594 - (594 * k), 94)))
    k1 = player.super_shoot
    if k1 > 5:
        k1 = 5
    if k1 == 5:
        text = font.render('supershoot is ready', True, (255, 255, 0))
    else:
        text = font.render('supershoot is not ready', True, (255, 255, 255))
    screen.blit(text, (WIDTH / 1.7, HEIGHT - HEIGHT / 5))
    pygame.draw.rect(screen, (255, 255, 255), ((WIDTH - WIDTH / 3.5, HEIGHT - HEIGHT / 9), (500, 100)), 3)
    pygame.draw.rect(screen, (255, 255, 0), ((WIDTH - WIDTH / 3.5 + 3, HEIGHT - HEIGHT / 9 + 3), (100 * k1 - 6, 94)))


def show_hint():
    font = pygame.font.Font(None, 100)
    text = font.render('Click Esc to exit', True, (255, 255, 0))
    screen.blit(text, (WIDTH / 30, HEIGHT / 8))


def draw_over():
    global running, play_gameover
    if play_gameover:
        gameover_sound.play()
        play_gameover = False
    pygame.mouse.set_visible(True)
    screen.blit(GAMEOVER_IMAGE, (0, 0))
    pygame.draw.rect(screen, (0, 200, 200), (WIDTH // 2 - WIDTH // 12 - 100, HEIGHT // 2 + 100, WIDTH // 6 + 210, HEIGHT // 11))
    font = pygame.font.Font(None, WIDTH // 14)
    text = font.render('TRY AGAIN', True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - WIDTH // 12 - 100, HEIGHT // 2 + 100))
    pygame.draw.rect(screen, (0, 200, 200), (WIDTH // 2 - WIDTH // 12 + 40, HEIGHT // 2 + 230, WIDTH // 6 - 80, HEIGHT // 11))
    text = font.render('EXIT', True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - WIDTH // 12 + 40, HEIGHT // 2 + 230))
    text = font.render(f'Points: {points}', True, (200, 50, 250))
    screen.blit(text, (WIDTH // 2 - WIDTH // 16 - 100, HEIGHT // 5))
    if over_coords:
        x, y = over_coords
        if WIDTH // 2 - WIDTH // 12 - 100 <= x <= WIDTH // 2 - WIDTH // 12 + WIDTH // 6 + 110 and \
                HEIGHT // 2 + 100 <= y <= HEIGHT // 2 + 100 + HEIGHT // 11:
            pygame.mouse.set_visible(False)
            game_init()
            play_gameover = True
            draw_background()
        elif WIDTH // 2 - WIDTH // 12 + 40 <= x <= WIDTH // 2 - WIDTH // 12 + 40 + (WIDTH // 6 - 80) and \
                HEIGHT // 2 + 230 <= y <= HEIGHT // 2 + 230 + HEIGHT // 11:
            running = False


def game_init():
    global bonus_sprite, meteors_sprite, bullets_sprite, enemies_sprite
    global enemy_bullets, background_sprite, hint_timer, seconds, points
    global coords, over_coords, spawn_meteor, super_shoot
    global spawn_enemy, spawn_enemy_query, player, GAME_MODE, play_gameover
    
    players = pygame.sprite.Group()
    bonus_sprite = pygame.sprite.Group()
    meteors_sprite = pygame.sprite.Group()
    bullets_sprite = pygame.sprite.Group()
    enemies_sprite = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    anim_sprite = pygame.sprite.Group()
    
    player = Player(players)
    hint_timer = 0
    seconds = 0
    points = 0
    
    coords = None
    play_gameover = True
    over_coords = None
    spawn_meteor = False
    GAME_MODE = 'intro'
    super_shoot = False
    spawn_enemy = False
    spawn_enemy_query = 1


def game_manager():
    if GAME_MODE != 'over':
        if 20 <= points <= 100:
            spawn_enemy_query = points // 20
        for i in bonus_sprite:
            i.update()
        for i in bullets_sprite:
            i.update()
        for i in enemy_bullets:
            i.update()
        for i in anim_sprite:
            i.update()
        player.update()


def game_time():
    global seconds, spawn_meteor, spawn_enemy, bonus, can_shoot
    seconds += 1
    can_shoot = True
    spawn_meteor = True
    if seconds % (6 - spawn_enemy_query) == 0:
        spawn_enemy = True
    if seconds == 20:
        seconds = 0
        if GAME_MODE != 'draw_level':
            bonus = Bonus(random.randint(1, 5))
            player.triple_shoot = False
            player.shield = False
            player.speed_boost = False
    for i in enemies_sprite:
        i.shoot()


def draw_level_menu():
    global GAME_MODE, LEVEL, level_coords
    LEVEL = None
    pygame.draw.rect(screen, (0, 255, 0), (WIDTH / 3 - 100, HEIGHT / 2 - 100, 200, 200))
    pygame.draw.rect(screen, (255, 255, 0), (WIDTH / 2 - 100, HEIGHT / 2 - 100, 200, 200))
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH / 2 + 200, HEIGHT / 2 - 100, 200, 200))
    font = pygame.font.Font(None, 300)
    text = font.render('1', True, (255, 255, 255))
    screen.blit(text, (WIDTH / 3 - 50, HEIGHT / 2 - 100))
    text = font.render('2', True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 - 50, HEIGHT / 2 - 100))
    text = font.render('3', True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 + 250, HEIGHT / 2 - 100))
    font = pygame.font.Font(None, 50)
    text = font.render('easy', True, (255, 255, 255))
    screen.blit(text, (WIDTH / 3 - 100, HEIGHT / 2 - 140))
    text = font.render('medium', True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 - 100, HEIGHT / 2 - 140))
    text = font.render('hard', True, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 + 200, HEIGHT / 2 - 140))
    if level_coords:
        x, y = level_coords
        if WIDTH / 3 - 100 <= x <= WIDTH / 3 + 100 and HEIGHT / 2 - 100 <= y <= HEIGHT / 2 + 100:
            LEVEL = 1
        elif WIDTH / 2 - 100 <= x <= WIDTH / 2 + 100 and \
                HEIGHT / 2 - 100 <= y <= HEIGHT / 2 + 100:
            LEVEL = 2
        elif WIDTH / 2 + 200 <= x <= WIDTH / 2 + 400 and HEIGHT / 2 - 100 <= y <= HEIGHT / 2 + 100:
            LEVEL = 3
        if LEVEL:
            GAME_MODE = 'draw_level'
            load_level(LEVEL)
            level_coords = None


def draw_level_func():
    global GAME_MODE, play_gameover
    if GAME_MODE != 'over':
        for i in over_sprite:
            i.update()
        for i in enemies_sprite:
            i.update()
        for i in meteors_sprite:
            i.update()
        for i in bullets_sprite:
            i.update()
        background_sprite.draw(screen)
        draw_hits_and_points()
        players.draw(screen)
        over_sprite.draw(screen)
        obst_sprite.draw(screen)
        meteors_sprite.draw(screen)
        bullets_sprite.draw(screen)
        enemies_sprite.draw(screen)
        enemy_bullets.draw(screen)
        anim_sprite.draw(screen)
    if player.hits <= 0:
        player.kill()
        GAME_MODE = 'over'
        play_gameover = True


def load_level(LEVEL):
    global obst_sprite, player, obstacles, meteors_sprite, enemies_sprite, over_splrite
    obst_sprite = pygame.sprite.Group()
    meteors_sprite = pygame.sprite.Group()
    enemies_sprite = pygame.sprite.Group()
    over_splrite = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    level_file = open(f'levels/level_{LEVEL}.txt')
    level_file = level_file.read().split('\n')
    for line in level_file:
        line = line.split()
        if line[0] == 'CREATE':
            if line[1] == 'place_spawn':
                player.x = int(line[2])
                player.y = int(line[3])
                player.rect.x = int(line[2])
                player.rect.y = int(line[3])                
            elif line[1] == 'place_over':
                Over(int(line[2]), int(line[3]))
            elif line[1] == 'Obstacle':
                Obstacle(int(line[2]), int(line[3]))
            elif line[1] == 'Enemy':
                Enemy(moving=False, x=int(line[2]), y=int(line[3]), level=int(line[4]))
            elif line[1] == 'Meteor':
                Meteor(x=int(line[2]), y=int(line[3]), speed_x=int(line[4]), speed_y=int(line[5]))          


def draw_win_window(level):
    global LEVEL, GAME_MODE, win_choice_coords, player, play_win_sound, play_gameover
    if play_win_sound:
        win_sound.play()
        play_win_sound = False
    screen.blit(WIN_IMAGE, (0, 0))
    font = pygame.font.Font(None, 85)
    text = font.render(f'Level {LEVEL} complete', True, (0, 255, 100))
    screen.blit(text, (WIDTH / 3 + 50, HEIGHT / 3))
    if player.hits / player.max_hits >= 0.66:
        finish = 4
    elif 0.66 > player.hits / player.max_hits >= 0.33:
        finish = 3
    elif player.hits / player.max_hits < 0.33:
        finish = 2
    for i in range(1, finish):
        screen.blit(STAR_IMAGE, (WIDTH / 4 + 200 * i, HEIGHT / 2))
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 4, int(HEIGHT / 1.5), 400, 150))
    font = pygame.font.Font(None, 200)
    text = font.render('Menu', True, (255, 255, 255))
    screen.blit(text, (WIDTH // 4, int(HEIGHT / 1.5)))
    if level != 3:
        pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 4 + 500, int(HEIGHT / 1.5), 400, 150))
        font = pygame.font.Font(None, 120)
        text = font.render('Next level', True, (255, 255, 255))
        screen.blit(text, (WIDTH // 4 + 500, int(HEIGHT / 1.45)))
    if win_choice_coords:
        x, y = win_choice_coords
        if WIDTH // 4 <= x <= WIDTH // 4 + 400 and \
                int(HEIGHT / 1.5) <= y <= int(HEIGHT / 1.5) + 150:
            game_init()
            GAME_MODE = 'intro'
            play_win_sound = True
        elif WIDTH // 4 + 500 <= x <= WIDTH // 4 + 900 and \
                int(HEIGHT / 1.45) <= y <= int(HEIGHT / 1.45) + 150:
            if level != 3:
                player.kill()
                player = None
                game_init()
                LEVEL = level + 1
                load_level(LEVEL)
                GAME_MODE = 'draw_level'
                play_win_sound = True
                play_gameover = True
        win_choice_coords = None


if __name__ == '__main__':
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
    pygame.init()
    pygame.mixer.init()
    WIDTH, HEIGHT = [int(i[i.find('=') + 1:]) for i in str(get_monitors()).split(', ')[2:4]]
    size = WIDTH, HEIGHT
    pygame.display.set_caption('Galaxy shooter')
    screen = pygame.display.set_mode(size)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    bonus_dict = {2: 'shield', 3: 'speed_boost', 1: 'triple_shoot', 4: 'super_shoot', 5: 'hp_bonus'}

    pygame.mixer.music.load("sounds/background_sounds/sound0.mp3")
    exp_sound = pygame.mixer.Sound("sounds/sounds/exp_sound.wav")
    player_shoot_sound = pygame.mixer.Sound("sounds/sounds/player_shoot_sound.wav")
    enemy_shoot_sound = pygame.mixer.Sound("sounds/sounds/enemy_shoot_sound.wav")
    super_shoot_sound = pygame.mixer.Sound("sounds/sounds/super_shoot_sound.wav")
    bonus_sound = pygame.mixer.Sound("sounds/sounds/bonus_sound.wav")
    damage_sound = pygame.mixer.Sound("sounds/sounds/damage_sound.wav")
    gameover_sound = pygame.mixer.Sound("sounds/sounds/gameover.wav")
    win_sound = pygame.mixer.Sound("sounds/sounds/win_sound.wav")

    players = pygame.sprite.Group()
    bonus_sprite = pygame.sprite.Group()
    meteors_sprite = pygame.sprite.Group()
    bullets_sprite = pygame.sprite.Group()
    enemies_sprite = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    background_sprite = pygame.sprite.Group()
    anim_sprite = pygame.sprite.Group()
    obst_sprite = pygame.sprite.Group()
    over_sprite = pygame.sprite.Group()

    BACKGROUND_IMAGE = pygame.image.load('backgrounds/space.png').convert()
    METEOR_IMAGES = [pygame.image.load(f'meteors/Meteor_{i}.png') for i in range(1, 11)]
    BONUS_IMAGES = [pygame.image.load(f'bonuses/{bonus_dict[i]}.png') for i in range(1, 6)]
    PLAYER_BULLET_SHOOT = pygame.image.load('bullets/laser.png')
    ENEMIES_SHOOT = [pygame.image.load(f'bullets/enemy_bullet{i}.png') for i in range(1, 6)]
    ENEMY_IMAGES = [pygame.image.load(f'enemies/enemy{i}.png') for i in range(1, 6)]
    ANIM_IMAGES = [pygame.transform.scale(pygame.image.load(f'animation/exp{i}.png'), (100, 100)) for i in range(1, 6)]
    GAMEOVER_IMAGE = pygame.image.load(f'backgrounds/gameover.jpg')
    WIN_IMAGE = pygame.image.load(f'backgrounds/win.jpg')
    OBST_IMAGES = [pygame.transform.scale(pygame.image.load(f'obstacles/obst{i}.png'), (120, 120)) for i in range(1, 5)]
    OVER_IMAGES = [pygame.transform.scale(pygame.image.load(f'over_animation/image{i}.png'), (100, 100)) for i in range(0, 360, 10)]
    STAR_IMAGE = pygame.transform.scale(pygame.image.load('other/star.png'), (100, 100))
    player = Player(players)
    bonus = None
    [Background(i) for i in range(2)]

    spawn_enemy_query = 1
    hint_timer = 0
    seconds = 0
    points = 0
    clock = pygame.time.Clock()

    can_shoot = True
    LEVEL = 1
    
    coords = None
    level_coords = None
    over_coords = None
    win_choice_coords = None
    
    spawn_meteor = False
    super_shoot = False
    spawn_enemy = False
    GAME_MODE = 'intro'
    play_gameover = True
    play_win_sound = True
    pygame.mixer.music.play(-1)
    running = True

    while running:
        if GAME_MODE != 'draw_level':
            if player.hits <= 0:
                player.kill()
                GAME_MODE = 'over'
            if hint_timer < 1000:
                hint_timer += 1
                if (hint_timer // 100 + 1) % 2 == 1:
                    hint = True
                else:
                    hint = False
            else:
                hint = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                game_time()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if GAME_MODE == 'draw_level_choice':
                        level_coords = event.pos
                    elif GAME_MODE == 'win':
                        win_choice_coords = event.pos
                    elif GAME_MODE == 'intro':
                        coords = event.pos
                    elif GAME_MODE == 'over':
                        over_coords = event.pos
                    else:
                        player.shoot('default')
                if event.button == 3 and player.super_shoot >= 5 and \
                        GAME_MODE != 'intro':
                    if GAME_MODE not in ('over', 'win'):
                        player.shoot('super')
                        super_shoot_sound.play()
                        player.super_shoot = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False                   
        if pygame.key.get_pressed()[pygame.K_w]:
            player.move(0, -player.speed)
        if pygame.key.get_pressed()[pygame.K_s]:
            player.move(0, player.speed)
        if pygame.key.get_pressed()[pygame.K_d]:
            player.move(player.speed, 0)
        if pygame.key.get_pressed()[pygame.K_a]:
            player.move(-player.speed, 0)
        game_manager()
        screen.fill((0, 0, 0))
        if GAME_MODE == 'draw_level':
            draw_level_func()
        elif GAME_MODE == 'draw_level_choice':
            draw_level_menu()
        elif GAME_MODE == 'intro':
            draw_intro()
        elif GAME_MODE == 'over':
            draw_over()
            pygame.mouse.set_visible(True)
        elif GAME_MODE == 'win':
            draw_win_window(LEVEL)
            pygame.mouse.set_visible(True)
        else:
            drawing()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
