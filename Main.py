import pygame as pg
import sys
from time import sleep
import pytmx
from os import path
from settings import *
from sprites import *
from tilemap import *

# health bar
def draw_player_count(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    # load images
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')

        #map_folder = path.join(game_folder, 'maps')
        self.map = Map(path.join(game_folder, 'map.txt'))
        #self.map = TiledMap(path.join(map_folder, 'map1.tmx'))
        #self.map_img = self.map.make_map()
        #self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.goal_img = pg.image.load(path.join(img_folder, GOAL_IMG)).convert_alpha()
        self.portal_down_img = pg.image.load(path.join(img_folder, PORTAL_DOWN_IMG)).convert_alpha()
        self.portal_right_img = pg.image.load(path.join(img_folder, PORTAL_RIGHT_IMG)).convert_alpha()
        self.portal_up_img = pg.image.load(path.join(img_folder, PORTAL_UP_IMG)).convert_alpha()
        self.portal_left_img = pg.image.load(path.join(img_folder, PORTAL_LEFT_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.portal_downs = pg.sprite.Group()
        self.portal_rights = pg.sprite.Group()
        self.portal_ups = pg.sprite.Group()
        self.portal_lefts = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):  # Read the map.txt
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'G':
                    Goal(self, col, row)
                if tile == 'D':
                    Portal_Down(self, col, row)
                if tile == 'R':
                    Portal_Right(self, col, row)
                if tile == 'U':
                    Portal_Up(self, col, row)
                if tile == 'L':
                    Portal_Left(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()


        if self.player.count <= 0:  # If player runs out of moves
            self.playing = False

        hits = pg.sprite.spritecollide(self.player, self.goals, True)  # If player makes it to the goal
        for hit in hits:
            self.playing = False

        portal_down_hits = pg.sprite.spritecollide(self.player, self.portal_downs, True)
        portal_right_hits = pg.sprite.spritecollide(self.player, self.portal_rights, True)
        portal_up_hits = pg.sprite.spritecollide(self.player, self.portal_ups, True)
        portal_left_hits = pg.sprite.spritecollide(self.player, self.portal_lefts, True)
        if portal_down_hits:
            for i in range(0, 9):
                self.player.move(dy=1)
        if portal_right_hits:
            for i in range(0, 9):
                self.player.move(dx=1)
        if portal_up_hits:
            for i in range(0, 9):
                self.player.move(dy=-1)
        if portal_left_hits:
            for i in range(0, 9):
                self.player.move(dx=-1)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)


        self.draw_grid()
        self.all_sprites.draw(self.screen)


        draw_player_count(self.screen, 10, 10, self.player.count / PLAYER_COUNT)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.playing = False
                if event.key == pg.K_LEFT:
                    self.player.count -= 10
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.count -= 10
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.count -= 10
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.count -= 10
                    self.player.move(dy=1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
