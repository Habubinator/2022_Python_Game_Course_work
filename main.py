import pygame
import os

WIDTH = 1280
HEIGHT = 720
FPS = 60

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


def load_sprite(file):
    return pygame.image.load(os.path.join(img_folder, file))


def change_player(file):
    return pygame.image.load(os.path.join(img_folder, "player", file))


def check_key(keys):
    if keys[pygame.K_d]:
        player.speed_x = 1
    elif keys[pygame.K_a]:
        player.speed_x = -1
    elif keys[pygame.K_w]:
        if player.collision.down:
            player.jump()
    else:
        player.speed_x = 0

class Player:
    def __init__(self):
        self.speed_x = 0
        self.speed_y = 0
        self.direction = 1
        self.walking_speed = 5
        self.jump_speed = -16
        self.x = 0
        self.y = 0
        self.player_img = change_player("p1_front.png")
        self.player_hud = change_player("hud_p1.png")
        self.health = 6
        self.coins = 0
        self.key = {
            "yellow": False
        }
        self.keyYellow = (change_player("hud_keyYellow_disabled.png"),
                          change_player("hud_keyYellow.png"))
        self.hearts = (change_player("hud_heartEmpty.png"),
                       change_player("hud_heartHalf.png"),
                       change_player("hud_heartFull.png"))
        self.coin = (change_player("hud_0.png"),
                     change_player("hud_1.png"),
                     change_player("hud_2.png"),
                     change_player("hud_3.png"),
                     change_player("hud_4.png"),
                     change_player("hud_5.png"),
                     change_player("hud_6.png"),
                     change_player("hud_7.png"),
                     change_player("hud_8.png"),
                     change_player("hud_9.png"))
        self.count = change_player("hud_x.png")
        self.coin_texture = change_player("hud_coins.png")
        self.animations = 1
        self.animation_cooldown = 0
        self.collision = Collision()

    def update(self):
        self.check_model()
        self.fall()
        self.collision.check([self.x, self.y, 66, 92])  # p1,p2,p3
        self.check_health()
        self.check_coins()
        self.check_key()
        screen.blit(self.player_img, (self.x, self.y))

    def walk(self):
        self.player_img = change_player(f"p1_walk{self.animations}.png")
        self.rotate_side()
        self.animations += 1
        if self.animations == 12:
            self.animations = 1

    def check_model(self):
        if self.speed_x > 0:
            self.x += self.walking_speed
            self.direction = 1
            self.walk()
        elif self.speed_x < 0:
            self.x -= self.walking_speed
            self.direction = 0
            self.walk()
        else:
            self.stand()
        if self.speed_y < 0:
            self.player_img = change_player("p1_jump.png")
            self.rotate_side()

    def rotate_side(self):
        if self.direction == 0:
            self.player_img = pygame.transform.flip(self.player_img, True, False)

    def stand(self):
        self.player_img = change_player('p1_stand.png')
        self.rotate_side()
        self.animations = 1

    def jump(self):
        self.speed_y = self.jump_speed
        self.y -= 1

    def fall(self):
        if not self.collision.down or self.speed_y < 0:
            self.speed_y += 0.5
            self.y += self.speed_y
            self.collision.down = False
        elif self.collision.down:
            self.speed_y = 0

    def hurt(self):
        self.health -= 1
        if self.health != 0:
            self.x = 100
            self.y = HEIGHT - 222
        else:
            level.add_front(load_sprite("lose.png"), [500, 250])
            self.x = 2000
            self.y = 1000

    def heal(self):
        self.health = 6

    def check_health(self):
        screen.blit(self.player_hud, (20, 18))
        output = [0,0,0]
        match self.health:
            case 0:
                pass
            case 1:
                output[0] = 1
            case 2:
                output[0] = 2
            case 3:
                output = [2,1,0]
            case 4:
                output = [2,2,0]
            case 5:
                output = [2,2,1]
            case 6:
                output = [2,2,2]

        screen.blit(self.hearts[output[0]], (90, 20))
        screen.blit(self.hearts[output[1]], (160, 20))
        screen.blit(self.hearts[output[2]], (230, 20))

    def check_coins(self):
        screen.blit(self.coin_texture, (300, 20))
        screen.blit(self.count, (350, 30))
        screen.blit(self.coin[self.coins], (380, 25))

    def check_key(self):
        if self.key["yellow"]:
            screen.blit(self.keyYellow[1], (420, 22))
        else:
            screen.blit(self.keyYellow[0], (420, 22))

    def add_coin(self):
        self.coins += 1

    def add_key(self,colour):
        self.key[colour] = True


class LevelNormal:
    def __init__(self):
        # download sprites from folder
        self.ground = load_sprite('grassCenter.png')
        self.ground_grass = load_sprite('grassMid.png')
        self.plant = load_sprite("plant.png")
        self.bush = load_sprite("bush.png")
        self.cloud = (load_sprite("cloud1.png"),
                      load_sprite("cloud2.png"),
                      load_sprite("cloud3.png"))
        self.brickWall = load_sprite("brickWall.png")
        self.coin = load_sprite("coinGold.png")
        self.door = (load_sprite("door_closedTop.png"),
                     load_sprite("door_closedMid.png"),
                     load_sprite("door_openTop.png"),
                     load_sprite("door_openMid.png"))
        self.keyYellow = load_sprite("keyYellow.png")
        self.signs = (load_sprite("left.png"),
                      load_sprite("right.png"),
                      load_sprite("up.png"))
        self.spikes = load_sprite("spikes.png")
        self.spring = load_sprite("springboardUp.png")
        self.level = 0
        self.items = []
        self.added_blocks = []
        # Make level
        self.new_level()

    def new_level(self):
        self.added_blocks = []
        self.items = []
        player.collision.coord = []
        coord = [-100, WIDTH + 100, 590, HEIGHT]
        player.collision.add(coord)

        player.x = 100
        player.y = HEIGHT - 222
        player.heal()
        player.key["yellow"] = False

        match self.level:
            case 0:
                # background
                self.add_front(self.bush, [20 + 140, HEIGHT - 200])
                self.add_front(self.bush, [20 + 510, HEIGHT - 200])
                self.add_front(self.plant, [20 + 380, HEIGHT - 200])
                self.add_front(self.plant, [20 + 380, HEIGHT - 200])
                self.add_front(self.plant, [20 + 920, HEIGHT - 200])
                self.add_front(self.cloud[2], [20 + 810, HEIGHT - 520])
                self.add_front(self.cloud[0], [20 + 380, HEIGHT - 420])
                self.add_front(self.cloud[2], [20 + 580, HEIGHT - 600])
                self.add_front(self.cloud[1], [20 + 1080, HEIGHT - 320])
                self.add_front(self.cloud[2], [20 + 70, 140])
                self.add_front(self.cloud[0], [20 + 180, HEIGHT - 420])
                self.add_front(self.signs[0],[20,HEIGHT-200])
                self.add_front(self.signs[1],[180,HEIGHT-200])
                self.add_front(self.signs[2],[280,380])
                # playable
                self.add_block(self.brickWall, [840, 350])
                self.add_block(self.brickWall, [770, 350])
                self.add_block(self.brickWall, [560, 210])
                self.add_block(self.brickWall, [490, 210])
                self.add_block(self.brickWall, [280, 450])
                self.add_block(self.brickWall, [280, 520])
                self.add_item(self.coin, [280, 160], "coin")
                self.add_item(self.keyYellow, [800,280],"keyYellow")
                self.add_door([1150, HEIGHT-200])
            case 1:
                self.add_front(self.cloud[2], [20 + 710, HEIGHT - 520])
                self.add_front(self.cloud[0], [20 + 380, HEIGHT - 420])
                self.add_front(self.cloud[2], [20 + 580, HEIGHT - 600])
                self.add_front(self.cloud[1], [20 + 1080, HEIGHT - 420])
                self.add_front(self.cloud[2], [20 + 50, HEIGHT - 600])
                self.add_front(self.cloud[1], [20 + 100, HEIGHT - 420])
                self.add_front(self.cloud[2], [20 + 420, 140])
                self.add_front(self.cloud[0], [20 + 600, HEIGHT - 450])

                self.add_item(self.coin, [450, 160], "coin")
                self.add_spikes([210, 520])
                self.add_spikes([280, 520])
                self.add_block(self.brickWall, [280, 380])
                self.add_spikes([350, 520])
                self.add_item(self.keyYellow,[450, 520],"keyYellow")
                self.add_spikes([560,520])
                self.add_spikes([630,520])
                self.add_block(self.brickWall, [630, 380])
                self.add_spikes([700,520])
                self.add_spikes([770,520])
                self.add_spikes([840,520])
                self.add_block(self.brickWall, [840, 380])
                self.add_spikes([910,520])
                self.add_spikes([980,520])
                self.add_spikes([1050,520])

                self.add_door([1150, HEIGHT-200])
            case 2:
                self.add_front(self.cloud[2], [20 + 710, HEIGHT - 520])
                self.add_front(self.cloud[0], [20 + 380, HEIGHT - 420])
                self.add_front(self.cloud[2], [20 + 580, HEIGHT - 600])
                self.add_front(self.cloud[1], [20 + 1080, HEIGHT - 420])
                self.add_front(self.cloud[2], [20 + 50, HEIGHT - 600])
                self.add_front(self.cloud[1], [20 + 100, HEIGHT - 420])
                self.add_front(self.cloud[2], [20 + 420, 140])
                self.add_front(self.cloud[0], [20 + 600, HEIGHT - 450])

                self.add_spring([490, 520])
                self.add_block(self.brickWall, [560, 520])
                self.add_block(self.brickWall, [560, 450])
                self.add_block(self.brickWall, [560, 380])
                self.add_item(self.keyYellow,  [700, 380], "keyYellow")
                self.add_spikes([630, 520])
                self.add_spikes([700, 520])
                self.add_spikes([770, 520])
                self.add_block(self.brickWall, [560, 310])
                self.add_block(self.brickWall, [560, 240])
                self.add_block(self.brickWall, [630, 240])
                self.add_block(self.brickWall, [0, 240])
                self.add_block(self.brickWall, [70, 240])
                self.add_item(self.coin, [70, 160], "coin")
                self.add_block(self.brickWall, [140, 240])

                self.add_spring([1010, 520])
                self.add_block(self.brickWall, [1150, 170])
                self.add_block(self.brickWall, [1080, 170])
                self.add_block(self.brickWall, [1220, 170])
                self.add_door([1150, 100])

    def next_level(self):
        self.level += 1
        self.new_level()

    def update(self):
        screen.fill((208, 244, 247))
        for i in range(0, WIDTH, 70):
            screen.blit(self.ground, (i, HEIGHT - 70))
            screen.blit(self.ground_grass, (i, HEIGHT - 130))
        for j in range(len(self.added_blocks)):
            screen.blit(self.added_blocks[j][0], (self.added_blocks[j][1], self.added_blocks[j][2]))
        for thing in self.items:
            thing.update()

    def add_block(self, block, placement):
        self.added_blocks.append([block, placement[0], placement[1]])
        player.collision.add([placement[0] - 50, placement[0] + 130, placement[1], placement[1] + 70])

    def add_front(self,block, placement):
        self.added_blocks.append([block, placement[0], placement[1]])

    def add_item(self, block, placement,options):
        self.added_blocks.append([block, placement[0], placement[1]])
        if options == "coin":
            a = Coin(placement,len(self.items),len(self.added_blocks)-1)
            self.items.append(a)
        if options == "keyYellow":
            a = KeyYellow(placement,len(self.items),len(self.added_blocks)-1)
            self.items.append(a)

    def add_door(self, placement):
        self.added_blocks.append([self.door[0], placement[0], placement[1]-70])
        self.added_blocks.append([self.door[1], placement[0], placement[1]])
        a = Door(placement, len(self.items), len(self.added_blocks) - 1)
        self.items.append(a)

    def add_spikes(self,placement):
        self.added_blocks.append([self.spikes, placement[0], placement[1]])
        a = Spikes(placement)
        self.items.append(a)

    def add_spring(self,placement):
        self.added_blocks.append([self.spring, placement[0], placement[1]])
        a = Spring(placement)
        self.items.append(a)

class Item:
    def __init__(self,coord,pos,visual_pos):
        self.x = coord[0]
        self.y = coord[1]
        self.pos = pos
        self.visual_pos = visual_pos

    def update(self):
        if player.x + 70 >= self.x >= player.x - 20 and player.y + 92 >= self.y >= player.y:
            level.items.pop(self.pos)
            level.added_blocks.pop(self.visual_pos)
            for i in range(len(level.items)):
                if i >= self.pos:
                    level.items[i].pos -= 1
                    level.items[i].visual_pos -= 1
            self.do_something()

    def do_something(self):
        pass

class Spikes:
    def __init__(self, coord):
        self.pos = 0
        self.visual_pos = 0
        self.x = coord[0]
        self.y = coord[1]

    def update(self):
        if player.x + 50 >= self.x >= player.x - 50 and player.y + 92 >= self.y >= player.y:
            player.hurt()

class Spring:
    def __init__(self, coord):
        self.pos = 0
        self.visual_pos = 0
        self.x = coord[0]
        self.y = coord[1]

    def update(self):
        if player.x + 50 >= self.x >= player.x - 50 and player.y + 92 >= self.y >= player.y:
            player.speed_y = -20

class Coin(Item):
    def __init__(self,coord,pos,visual_pos):
        super().__init__(coord,pos,visual_pos)

    def do_something(self):
        player.add_coin()

class KeyYellow(Item):
    def __init__(self, coord, pos, visual_pos):
        super().__init__(coord, pos, visual_pos)

    def do_something(self):
        player.add_key("yellow")

class Door:
    def __init__(self, coord, pos, visual_pos):
        self.x = coord[0]
        self.y = coord[1]
        self.pos = pos
        self.visual_pos = visual_pos

    def update(self):
        if player.key["yellow"]:
            level.added_blocks[self.visual_pos][0] = level.door[3]
            level.added_blocks[self.visual_pos-1][0] = level.door[2]
            if player.x + 70 >= self.x >= player.x - 20 and player.y + 92 >= self.y >= player.y:
                level.items.pop(self.pos)
                for i in level.items:
                    i.pos -= 2
                    i.visual_pos -= 2
                level.added_blocks.pop(self.visual_pos)
                level.added_blocks.pop(self.visual_pos-1)
                level.next_level()

class Collision:
    def __init__(self):
        self.down = False
        self.up = False
        self.right = False
        self.left = False
        self.coord = []

    def add(self, coordinates):
        # [ 0, 0, 0, 0] left x, right x, and top y, bottom y
        self.coord.append(coordinates)

    def check(self, character):  # character x, character y , x and y of the picture
        # vertical
        for i in range(len(self.coord)):
            if self.coord[i][1] < character[0]:
                self.down = False
                self.up = False
            elif self.coord[i][0] <= character[0] <= self.coord[i][1]:                      # Check x
                if self.coord[i][0] <= (character[0] + character[2]) <= self.coord[i][1]:   #
                    if self.coord[i][2] <= character[1] <= self.coord[i][3]:
                        self.up = True
                        player.speed_y = 0
                        player.y -= (self.coord[i][3] - character[1] - character[3]) / 5
                        break
                    elif self.coord[i][3] >= character[1] + character[3] >= self.coord[i][2]:
                        self.down = True
                        player.y += self.coord[i][2] - character[1] - character[3]
                        break
            else:
                self.down = False
                self.up = False
        # horizontal
        for i in range(len(self.coord)):
            if self.coord[i][1] < character[0]:
                self.right = False
                self.left = False
            elif (character[1] < self.coord[i][3] < character[1] + character[3]) or \
                    (self.coord[i][3] <= character[1] + character[3] <= self.coord[i][2]):
                if self.coord[i][1] >= character[0] + character[2] >= self.coord[i][0] + 80:
                    self.left = True
                    player.speed_x = 0
                    player.x += -(character[0]-self.coord[i][1])/15
                elif self.coord[i][1]-50 >= character[0] + character[2] >= self.coord[i][0] + 50:
                    self.right = True
                    player.speed_x = 0
                    player.x -= (character[0] + character[2] - self.coord[i][0]) / 10
            else:
                self.right = False
                self.left = False

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab_6")
clock = pygame.time.Clock()
All_objects = []

player = Player()
level = LevelNormal()

All_objects.append(level)
All_objects.append(player)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    check_key(pygame.key.get_pressed())

    for item in All_objects:
        item.update()
    pygame.display.update()

pygame.quit()
