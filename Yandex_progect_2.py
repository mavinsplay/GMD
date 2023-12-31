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


def loadLevel(level_nr=1):
    global person
    filename = "geometry_levels/" + str(level_nr)
    if not os.path.isfile(filename):
        return False
    f = open(filename, "r")
    data = f.readlines()
    x, y = 0, 0
    for row in data:
        for ch in row:
            if ch == "O":
                Stone((x, y))
            elif ch == "S":
                Stone((x, y), True)
            elif ch == "~":
                person = Player((x, y))
            x += 30
        x = 0
        y += 30
    return True


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('icon_1.png'), (31, 31))
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
            if pygame.sprite.collide_mask(i, self) and type(i) != Player:
                if i.trap or abs(self.rect.y - i.rect.y) < 20:  # Удар об ловушки или в переднюю стенку платформы
                    sys.exit()  # TODO
                if abs(self.rect.y - i.rect.y) < 30:
                    self.rect.y -= 30 + self.rect.y - i.rect.y

                self.collide = False

        if self.collide and self.jump < 0:
            self.rect.y -= self.jump

        if self.jump > 0:
            self.rect.y -= self.jump

        self.jump -= 0.5
        if not self.collide:
            self.jump = 0


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos, trap=False):
        super().__init__(all_sprites)
        screen1 = pygame.Surface((30, 30))
        if not trap:
            screen1.fill((125, 125, 125))
        else:
            screen1.fill((255, 0, 255))
            pygame.draw.polygon(screen1, (0, 0, 0), ((0, 30), (15, 0), (30, 30)))
            pygame.draw.polygon(screen1, (255, 255, 255), ((0, 29), (15, 0), (30, 29)), 1)
            screen1.set_colorkey((255, 0, 255))
        self.image = screen1.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.nap = False
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.trap = trap

    def update(self):
        self.rect.x -= 5
        self.rect.x %= 1000


class Redactor:
    def __init__(self):
        super().__init__()
        global all_sprites, level_nr

        pygame.init()
        pygame.display.set_caption('Редактор уровня')

        screen2 = pygame.display.set_mode(size)

        clock = pygame.time.Clock()
        running2 = True

        all_sprites = pygame.sprite.Group()

        image = pygame.Surface((100, 510))
        image.fill((255, 120, 120))
        self.screen = pygame.sprite.Sprite(all_sprites)
        self.screen.image = image.convert_alpha()
        self.screen.rect = self.screen.image.get_rect()
        self.screen.rect.x = 900

        image = pygame.Surface((100, 30))
        image.fill((0, 120, 120))
        self.screen1 = pygame.sprite.Sprite(all_sprites)
        self.screen1.image = image.convert_alpha()
        self.screen1.rect = self.screen1.image.get_rect()
        self.screen1.rect.x = 900
        self.screen1.rect.y = 100

        self.stone = Stone((920, 100))

        self.trap = Stone((920, 200), True)

        self.player1 = Player((210, 210))
        self.player = Player((920, 300))

        self.posit = 0

        while running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[0] < 900:
                        click = True
                        for i in all_sprites:
                            if (i.rect.x, i.rect.y) == (
                            event.pos[0] - event.pos[0] % 30, event.pos[1] - event.pos[1] % 30):
                                click = False
                        if click:
                            if self.posit == 0:
                                Stone((event.pos[0] - event.pos[0] % 30, event.pos[1] - event.pos[1] % 30))
                            elif self.posit == 1:
                                Stone((event.pos[0] - event.pos[0] % 30, event.pos[1] - event.pos[1] % 30), True)
                            elif self.posit == 2:
                                self.player1.rect.x = event.pos[0] - event.pos[0] % 30
                                self.player1.rect.y = event.pos[1] - event.pos[1] % 30
                    else:
                        if self.trap.rect.collidepoint(event.pos):
                            self.posit = 1
                            self.screen1.rect.y = 200
                        elif self.stone.rect.collidepoint(event.pos):
                            self.posit = 0
                            self.screen1.rect.y = 100
                        elif self.player.rect.collidepoint(event.pos):
                            self.posit = 2
                            self.screen1.rect.y = 300
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if event.pos[0] < 900:
                        for i in all_sprites:
                            if i != self.player1 and i.rect.collidepoint(event.pos):
                                all_sprites.remove(i)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                        for i in all_sprites:
                            if i.rect.x == 0:
                                left = False
                        if left:
                            for i in all_sprites:
                                if i not in [self.stone, self.trap, self.player, self.screen, self.screen1]:
                                    i.rect.x -= 30
                    elif event.key == pygame.K_RIGHT:
                        for i in all_sprites:
                            if i not in [self.stone, self.trap, self.player, self.screen, self.screen1]:
                                i.rect.x += 30
                    elif event.key == pygame.K_DOWN:
                        for i in all_sprites:
                            if i not in [self.stone, self.trap, self.player, self.screen, self.screen1]:
                                i.rect.y += 30
                    elif event.key == pygame.K_UP:
                        up = True
                        for i in all_sprites:
                            if i.rect.y == 0 and i not in [self.stone, self.trap, self.player, self.screen,
                                                           self.screen1]:
                                up = False
                        if up:
                            for i in all_sprites:
                                if i not in [self.stone, self.trap, self.player, self.screen, self.screen1]:
                                    i.rect.y -= 30

            screen2.fill((0, 255, 0))
            all_sprites.draw(screen2)
            for x in range(30):
                for y in range(17):
                    pygame.draw.rect(screen2, (255, 255, 255), (x * 30, y * 30, 30, 30), 1)
            clock.tick(50)
            pygame.display.flip()

        all_sprites.remove(self.player, self.stone, self.trap, self.screen, self.screen1)
        self.save(level_nr)
        all_sprites.remove(self.player1)

    def save(self, level_nr=1):
        global all_sprites

        filename = "geometry_levels/" + str(level_nr + 1)

        f = open(filename, "w")

        max_x = 0
        max_y = 0
        for i in all_sprites:
            if max_x < i.rect.x:
                max_x = i.rect.x
            if max_y < i.rect.y:
                max_y = i.rect.y

        for y in range(max_y // 30 + 1):
            for x in range(max_x // 30 + 1):
                write = True
                for i in all_sprites:
                    if i.rect.x == x * 30 and i.rect.y == y * 30:
                        if type(i) == Stone and i.trap:
                            f.write('S')
                        elif type(i) == Stone:
                            f.write('O')
                        elif type(i) == Player:
                            f.write('~')
                        write = False
                if write:
                    f.write('.')
            f.write('\n')
        f.close()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Инициализация игры')
    size = width, height = 1000, 510
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    person = None
    level_nr = 1
    a = Redactor()
    loadLevel(level_nr)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                person.rect.x = event.pos[0]
                person.rect.y = event.pos[1]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Stone(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not person.collide:
                    person.jump_bul = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    person.jump_bul = False

        if person.jump_bul and not person.collide:
            person.jump = 8

        all_sprites.update()
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        clock.tick(50)
        pygame.display.flip()
    pygame.quit()
