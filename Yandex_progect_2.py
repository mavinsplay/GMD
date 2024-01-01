import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, scale, all):
        super().__init__(all)
        self.image = pygame.transform.scale(load_image('icon_1.png', -1), (int(width * scale), int(height * scale)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.jump = -12
        self.jump_bul = False

        self.collide = False

    def update(self):
        self.collide = True
        for i in all_sprites:
            if pygame.sprite.collide_mask(i, self) and type(i) == Stone:
                if i.trap or abs(self.rect.y - i.rect.y) < 20:
                    sys.exit()  # TODO
                if abs(self.rect.y - i.rect.y) < 30:
                    print(30 + self.rect.y - i.rect.y)
                    self.rect.y -= 30 + self.rect.y - i.rect.y

                self.collide = False

        if self.collide and self.jump < 0:
            self.rect.y += 2

        self.jump -= 1
        if self.jump > 0:
            self.rect.y -= 2

        if not self.collide:
            self.jump = 0


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, scale, all, trap=False):
        super().__init__(all)
        screen1 = pygame.Surface((30, 30))
        if not trap:
            screen1.fill((125, 125, 125))
        else:
            screen1.fill((255, 0, 255))
            pygame.draw.polygon(screen1, (0, 0, 0), ((0, 30), (15, 0), (30, 30)))
            pygame.draw.polygon(screen1, (255, 255, 255), ((0, 29), (15, 0), (30, 29)), 1)
            screen1.set_colorkey((255, 0, 255))
        self.image = pygame.transform.scale(screen1.convert_alpha(), (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.trap = trap

    def update(self):
        self.rect.x -= 10


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, scale, all, var=1):
        super().__init__(all)

        self.image = pygame.transform.scale(load_image("icon_2.png", -1), (int(width * scale), int(height * scale * 1.5)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.var = var

    def update(self):
        self.rect.x -= 10


class Redactor:
    def __init__(self, width: int, height: int):
        super().__init__()

        pygame.init()
        pygame.display.set_caption('Редактор уровня')

        screen2 = pygame.display.set_mode((width, height))

        clock = pygame.time.Clock()
        running2 = True

        all_sprites = pygame.sprite.Group()

        image = pygame.Surface((width, height * 0.12))
        image.fill((255, 120, 120))
        self.screen = pygame.sprite.Sprite(all_sprites)
        self.screen.image = image.convert_alpha()
        self.screen.rect = self.screen.image.get_rect()
        self.screen.rect.y = height * 0.88

        image = pygame.Surface((60,  height * 0.12))
        image.fill((0, 120, 120))
        self.screen1 = pygame.sprite.Sprite(all_sprites)
        self.screen1.image = image.convert_alpha()
        self.screen1.rect = self.screen1.image.get_rect()
        self.screen1.rect.x = width * 0.1
        self.screen1.rect.y = height * 0.88

        scale = 0.04

        self.stone = Stone((width * 0.1, height * 0.9), width, height, scale, all_sprites)

        self.trap = Stone((width * 0.2, height * 0.9), width, height, scale, all_sprites, True)
        self.player = Player((width * 0.3, height * 0.9), width, height, scale, all_sprites)

        self.portal = Portal((width * 0.4, height * 0.9), width, height, scale, all_sprites)

        all_sprites2 = pygame.sprite.Group()

        self.player1 = Player((width * scale * 7, height * scale * 9), width, height, scale, all_sprites2)

        self.posit = 0

        while running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[1] < height * 0.88:
                        click = True
                        for i in all_sprites:
                            if i.rect.collidepoint(event.pos[0], event.pos[1]) or (
                                    self.posit == 3 and i.rect.collidepoint(event.pos[0], event.pos[1] + int(height * scale))):
                                click = False
                        if click:
                            if self.posit == 0:
                                Stone((event.pos[0] - event.pos[0] % int(width * scale), event.pos[1] - event.pos[1] % int(height * scale)), width, height, scale, all_sprites2)
                            elif self.posit == 1:
                                Stone((event.pos[0] - event.pos[0] % int(width * scale), event.pos[1] - event.pos[1] % int(height * scale)), width, height, scale, all_sprites2, True)
                            elif self.posit == 2:
                                self.player1.rect.x = event.pos[0] - event.pos[0] % int(width * scale)
                                self.player1.rect.y = event.pos[1] - event.pos[1] % int(height * scale)
                            elif self.posit == 3:
                                Portal((event.pos[0] - event.pos[0] % int(width * scale), event.pos[1] - event.pos[1] % int(height * scale)), width, height, scale, all_sprites2)
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
                    if event.pos[1] < height * 0.88:
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
            for x in range(int(width / (width * scale))):
                for y in range(int(height * 0.9 / (height * scale))):
                    pygame.draw.rect(screen2, (255, 255, 255), (int(x * width * scale), int(y * height * scale), int(width * scale), int(height * scale)), 1)
            clock.tick(50)
            pygame.display.flip()

        self.save(all_sprites2, width, height, scale, level_nr)

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


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Инициализация игры')
    size = width, height = 1200, 800

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    running = True
    scale = 0.2
    all_sprites = pygame.sprite.Group()
    level_nr = 1
    a = Redactor(width, height)
    person = loadLevel(width, height, 0.04, all_sprites, level_nr)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                person.rect.x = event.pos[0]
                person.rect.y = event.pos[1]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Stone(event.pos, width, height, scale, all_sprites)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not person.collide:
                    person.jump_bul = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    person.jump_bul = False

        if person.jump_bul and not person.collide:
            person.jump = 30

        all_sprites.update()
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        clock.tick(50)
        pygame.display.flip()
    pygame.quit()
