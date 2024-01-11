import pygame
import os
from objects import Player, Stone, Button, load_image, Spike


def loadLevel(scale: float,
              all_sprites: pygame.sprite.Group, level_nr: int = 1, 
              music: str = '001.mp3', icon: str = 'icon_1.png') -> Player:
    filename = "geometry_levels/" + str(level_nr)
    if not os.path.isfile(filename):
        return False
    f = open(filename, "r")
    data = f.readlines()
    x, y = 0, 0
    for row in data:
        for ch in row:
            if ch == "O":
                Stone((x, y), scale, all_sprites)
            elif ch == "S":
                Spike((x, y), scale, all_sprites)
            elif ch == "~":
                person = Player((x, y), scale, all_sprites, icon)
            x += 128 * scale
        x = 0
        y += 128 * scale
    pygame.mixer.music.load(f'data/{music}')
    pygame.mixer.music.play()
    return person


class Editor:
    def __init__(self, width: int, height: int, screen: pygame.display, icon: pygame.image) -> None:
        super().__init__()

        pygame.init()
        pygame.display.set_caption('Редактор уровня')

        clock = pygame.time.Clock()
        running = True

        all_sprites = pygame.sprite.Group()

        scale = 0.5

        scale_screen = 0.2

        image = pygame.Surface((width, height * scale_screen))
        image.fill((255, 120, 120))
        self.screen = pygame.sprite.Sprite(all_sprites)
        self.screen.image = image.convert_alpha()
        self.screen.rect = self.screen.image.get_rect()
        self.screen.rect.y = height * (1 - scale_screen)

        btn_save = Button(load_image('save_level_buton_state1.png'),
                          (width * 0.7, height * (1 - scale_screen)), 0.6)
        btn_close = Button(load_image('back_button.png'), (width * (1 - scale_screen + btn_save.image.get_width() * 0.6 / width), height * (1 - scale_screen)), 0.6)

        image = pygame.Surface((64, height * scale_screen))
        image.fill((0, 120, 120))
        self.screen1 = pygame.sprite.Sprite(all_sprites)
        self.screen1.image = image.convert_alpha()
        self.screen1.rect = self.screen1.image.get_rect()
        self.screen1.rect.x = width * 0.1
        self.screen1.rect.y = height * (1 - scale_screen)

        self.stone = Stone(
            (width * 0.1, height * (1 - scale_screen / 1.5)), scale, all_sprites)

        self.trap = Spike((width * 0.2, height * (1 - scale_screen / 1.5)), scale, all_sprites)
        self.player = Player(
            (width * 0.3, height * (1 - scale_screen / 1.5)), scale, all_sprites, icon)

        all_sprites2 = pygame.sprite.Group()

        fon = pygame.sprite.Sprite(all_sprites2)
        fon.image = pygame.transform.scale(load_image(
            'editor_background.png'), (width, height))
        fon.rect = fon.image.get_rect()

        self.player1 = Player(
            (self.player.width * scale * 5, self.player.height * scale * 3), scale, all_sprites2, icon)

        self.posit = 0

        up, down, right, left = False, False, False, False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[1] < height * (1 - scale_screen):
                        click = True
                        for i in all_sprites2:
                            if i != fon and (i.rect.collidepoint(event.pos[0], event.pos[1]) or (
                                    self.posit == 3 and i.rect.collidepoint(event.pos[0],
                                                                            event.pos[1] + int(self.player.height * scale)))):
                                click = False
                        if click:
                            if self.posit == 0:
                                Stone((event.pos[0] - event.pos[0] % int(self.player.width * scale),
                                       event.pos[1] - event.pos[1] % int(self.player.height * scale)), scale,
                                      all_sprites2)
                            elif self.posit == 1:
                                Spike((event.pos[0] - event.pos[0] % int(self.player.width * scale),
                                       event.pos[1] - event.pos[1] % int(self.player.height * scale)), scale,
                                      all_sprites2)
                            elif self.posit == 2:
                                self.player1.rect.x = event.pos[0] - event.pos[0] % int(self.player.width * scale)
                                self.player1.rect.y = event.pos[1] - event.pos[1] % int(self.player.height * scale)
                    else:
                        if btn_save.rect.collidepoint(event.pos):
                            self.save(all_sprites2, scale, level_nr=4)
                            btn_save.update('save_level_buton_state2.png')
                        elif btn_close.rect.collidepoint(event.pos):
                            btn_close.update('back_button.png')
                        if self.stone.rect.collidepoint(event.pos):
                            self.posit = 0
                            self.screen1.rect.x = width * 0.1
                        elif self.trap.rect.collidepoint(event.pos):
                            self.posit = 1
                            self.screen1.rect.x = width * 0.2
                        elif self.player.rect.collidepoint(event.pos):
                            self.posit = 2
                            self.screen1.rect.x = width * 0.3

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if event.pos[1] < height * (1 - scale_screen):
                        for i in all_sprites2:
                            if i not in [self.player1, fon] and i.rect.collidepoint(event.pos):
                                all_sprites2.remove(i)

                if event.type == pygame.MOUSEBUTTONUP:
                    btn_save.update('save_level_buton_state2.png')
                    if btn_close.rect.collidepoint(event.pos):
                        running = False
                    else:
                        btn_close.update('back_button.png')

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                    elif event.key == pygame.K_RIGHT:
                        right = True
                    elif event.key == pygame.K_DOWN:
                        down = True
                    elif event.key == pygame.K_UP:
                        up = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    elif event.key == pygame.K_RIGHT:
                        right = False
                    elif event.key == pygame.K_DOWN:
                        down = False
                    elif event.key == pygame.K_UP:
                        up = False

            for i in all_sprites2:
                if i != fon and i.rect.y == 0:
                    up = False
                if i != fon and i.rect.x == 0:
                    left = False

            for i in all_sprites2:
                if i != fon:
                    if left:
                        i.rect.x -= self.player.width * scale
                    elif up:
                        i.rect.y -= self.player.height * scale
                    elif right:
                        i.rect.x += self.player.width * scale
                    elif down:
                        i.rect.y += self.player.height * scale

            all_sprites2.draw(screen)
            all_sprites.draw(screen)
            btn_save.draw(screen)
            btn_close.draw(screen)

            for y in range(int(height * (1 - scale_screen) / (self.player.height * scale))):
                for x in range(int(width / (self.player.width * scale))):
                    pygame.draw.rect(screen, (255, 255, 255), (
                        int(x * self.player.width * scale), int(y * self.player.height * scale), int(self.player.width * scale), int(self.player.height * scale)), 1)
            clock.tick(50)
            pygame.display.flip()

    def save(self, all_sprites, scale, level_nr=1) -> None:
        filename = "geometry_levels/" + str(level_nr)

        f = open(filename, "w")

        max_x = 0
        max_y = 0
        for i in all_sprites:
            if max_x < i.rect.x:
                max_x = i.rect.x
            if max_y < i.rect.y:
                max_y = i.rect.y

        for y in range(int(max_y / self.player.height / scale) + 1):
            for x in range(int(max_x / self.player.width / scale) + 1):
                write = True
                for i in all_sprites:
                    if i.rect.x == x * int(self.player.width * scale) and i.rect.y == y * int(self.player.height * scale):
                        if type(i) == Spike:
                            f.write('S')
                        elif type(i) == Stone:
                            f.write('O')
                        elif type(i) == Player:
                            f.write('~')
                        write = False
                        break
                if write:
                    f.write('.')
            f.write('\n')
        f.close()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Инициализация игры')
    size = width, height = 1000, 1000

    all_sprites = pygame.sprite.Group()
    level_nr = 1
    scale = 0.5

    screen = pygame.display.set_mode(size)
    fon = pygame.sprite.Sprite(all_sprites)
    fon.image = pygame.transform.scale(
        load_image('editor_background.png'), size)
    fon.rect = fon.image.get_rect()

    clock = pygame.time.Clock()
    running = True

    person = loadLevel(scale, all_sprites, level_nr)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                person.rect.x = event.pos[0]
                person.rect.y = event.pos[1]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Stone(event.pos, scale, all_sprites)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not person.collide:
                    person.jump_bul = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    person.jump_bul = False

        if person.jump_bul and person.g <= -person.height * 0.13:
            person.g = person.height * 0.13 * person.g // abs(person.g) * -1

        for i in all_sprites:
            if i != fon:
                i.update()
        all_sprites.draw(screen)
        clock.tick(50)
        pygame.display.flip()
    pygame.quit()
