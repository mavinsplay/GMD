import pygame
import os
from objects import Player, Stone, Portal


def loadLevel(width: int, height: int, scale: float, all_sprites: pygame.sprite.Group, level_nr=1):
    filename = "geometry_levels/" + str(level_nr)
    if not os.path.isfile(filename):
        return False
    f = open(filename, "r")
    data = f.readlines()
    x, y = 0, 0
    for row in data:
        for ch in row:
            if ch == "O":
                Stone((x, y), width, height, scale, all_sprites)
            elif ch == "S":
                Stone((x, y), width, height, scale, all_sprites, True)
            elif ch == "~":
                person = Player((x, y), width, height, scale, all_sprites)
            elif ch == "A":
                Portal((x, y), width, height, scale, all_sprites)
            x += width * scale
        x = 0
        y += height * scale
    return person


class Editor:
    def __init__(self, width: int, height: int):
        super().__init__()

        pygame.init()
        pygame.display.set_caption('Редактор уровня')

        screen2 = pygame.display.set_mode((width, height))

        clock = pygame.time.Clock()
        running2 = True

        all_sprites = pygame.sprite.Group()

        scale = 0.04

        scale_screen = 0.2

        image = pygame.Surface((width, height * scale_screen))
        image.fill((255, 120, 120))
        self.screen = pygame.sprite.Sprite(all_sprites)
        self.screen.image = image.convert_alpha()
        self.screen.rect = self.screen.image.get_rect()
        self.screen.rect.y = height * (1 - scale_screen)

        image = pygame.Surface((width * scale, height * scale_screen))
        image.fill((0, 120, 120))
        self.screen1 = pygame.sprite.Sprite(all_sprites)
        self.screen1.image = image.convert_alpha()
        self.screen1.rect = self.screen1.image.get_rect()
        self.screen1.rect.x = width * 0.1
        self.screen1.rect.y = height * (1 - scale_screen)

        self.stone = Stone(
            (width * 0.1, height * (1 - scale_screen / 1.7)), width, height, scale, all_sprites)

        self.trap = Stone((width * 0.2, height * (1 - scale_screen / 1.7)),
                          width, height, scale, all_sprites, True)
        self.player = Player(
            (width * 0.3, height * (1 - scale_screen / 1.7)), width, height, scale, all_sprites)

        self.portal = Portal(
            (width * 0.4, height * (1 - scale_screen / 1.4)), width, height, scale, all_sprites)

        all_sprites2 = pygame.sprite.Group()

        self.player1 = Player(
            (width * scale * 7, height * scale * 9), width, height, scale, all_sprites2)

        self.posit = 0

        while running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[1] < height * (1 - scale_screen):
                        click = True
                        for i in all_sprites2:
                            if i.rect.collidepoint(event.pos[0], event.pos[1]) or (
                                    self.posit == 3 and i.rect.collidepoint(event.pos[0],
                                                                            event.pos[1] + int(height * scale))):
                                click = False
                        if click:
                            if self.posit == 0:
                                Stone((event.pos[0] - event.pos[0] % int(width * scale),
                                       event.pos[1] - event.pos[1] % int(height * scale)), width, height, scale,
                                      all_sprites2)
                            elif self.posit == 1:
                                Stone((event.pos[0] - event.pos[0] % int(width * scale),
                                       event.pos[1] - event.pos[1] % int(height * scale)), width, height, scale,
                                      all_sprites2, True)
                            elif self.posit == 2:
                                self.player1.rect.x = event.pos[0] - \
                                    event.pos[0] % int(width * scale)
                                self.player1.rect.y = event.pos[1] - \
                                    event.pos[1] % int(height * scale)
                            elif self.posit == 3:
                                Portal((event.pos[0] - event.pos[0] % int(width * scale),
                                        event.pos[1] - event.pos[1] % int(height * scale)), width, height, scale,
                                       all_sprites2)
                    else:
                        if self.stone.rect.collidepoint(event.pos):
                            self.posit = 0
                            self.screen1.rect.x = width * 0.1
                        elif self.trap.rect.collidepoint(event.pos):
                            self.posit = 1
                            self.screen1.rect.x = width * 0.2
                        elif self.player.rect.collidepoint(event.pos):
                            self.posit = 2
                            self.screen1.rect.x = width * 0.3
                        elif self.portal.rect.collidepoint(event.pos):
                            self.posit = 3
                            self.screen1.rect.x = width * 0.4
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if event.pos[1] < height * (1 - scale_screen):
                        for i in all_sprites2:
                            if i != self.player1 and i.rect.collidepoint(event.pos):
                                all_sprites2.remove(i)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                        for i in all_sprites2:
                            if i.rect.x == 0:
                                left = False
                        if left:
                            for i in all_sprites2:
                                i.rect.x -= width * scale
                    elif event.key == pygame.K_RIGHT:
                        for i in all_sprites2:
                            i.rect.x += width * scale
                    elif event.key == pygame.K_DOWN:
                        for i in all_sprites2:
                            i.rect.y += height * scale
                    elif event.key == pygame.K_UP:
                        up = True
                        for i in all_sprites2:
                            if i.rect.y == 0:
                                up = False
                        if up:
                            for i in all_sprites2:
                                i.rect.y -= height * scale

            screen2.fill((0, 255, 0))
            all_sprites2.draw(screen2)
            all_sprites.draw(screen2)
            for y in range(int(height * (1 - scale_screen) / (height * scale))):
                for x in range(int(width / (width * scale))):
                    pygame.draw.rect(screen2, (255, 255, 255), (
                        int(x * width * scale), int(y * height * scale), int(width * scale), int(height * scale)), 1)
            clock.tick(50)
            pygame.display.flip()

        self.save(all_sprites2, width, height, scale)

    def save(self, all_sprites, width, height, scale, level_nr=1):
        filename = "geometry_levels/" + str(level_nr + 1)

        f = open(filename, "w")

        max_x = 0
        max_y = 0
        for i in all_sprites:
            if max_x < i.rect.x:
                max_x = i.rect.x
            if max_y < i.rect.y:
                max_y = i.rect.y

        for y in range(int(max_y / height / scale) + 1):
            for x in range(int(max_x / width / scale) + 1):
                write = True
                for i in all_sprites:
                    if i.rect.x == x * int(width * scale) and i.rect.y == y * int(height * scale):
                        if type(i) == Stone and i.trap:
                            f.write('S')
                        elif type(i) == Stone:
                            f.write('O')
                        elif type(i) == Player:
                            f.write('~')
                        elif type(i) == Portal:
                            f.write('A')
                        write = False
                        break
                if write:
                    f.write('.')
            f.write('\n')
        f.close()
