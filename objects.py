import pygame
import os


def load_image(name: str, colorkey=None) -> pygame.image:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.image,
                 position: tuple, scale: float) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.signal_func = None
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def set_callback_func(self, func: ...) -> None:
        self.signal_func = func

    def click(self, pos: tuple) -> None:
        if self.rect.collidepoint(pos) and self.signal_func:
            self.signal_func()


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, scale, all, trap=False):
        super().__init__(all)
        screen1 = pygame.Surface((30, 30))
        if not trap:
            screen1.fill((125, 125, 125))
        else:
            screen1.fill((255, 0, 255))
            pygame.draw.polygon(screen1, (0, 0, 0),
                                ((0, 30), (15, 0), (30, 30)))
            pygame.draw.polygon(screen1, (255, 255, 255),
                                ((0, 29), (15, 0), (30, 29)), 1)
            screen1.set_colorkey((255, 0, 255))
        self.image = pygame.transform.scale(
            screen1.convert_alpha(), (int(width * scale), int(height * scale)))
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

        self.image = pygame.transform.scale(load_image("ShipPortal.png", -1),
                                            (int(width * scale), int(height * scale * 2)))  # удалено subsurafce - ошибка ValueError: subsurface rectangle outside surface area
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.var = var

    def update(self):
        self.rect.x -= 10


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, scale, all):
        super().__init__(all)
        self.image = pygame.transform.scale(load_image(
            'icon_4.png'), (int(width * scale), int(height * scale)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.all_sprites = all

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.width = int(width * scale)
        self.height = int(height * scale)

        self.jump_bul = False

        self.g = self.height * 0.02

        self.collide = False

    def update(self):
        self.collide = True
        for i in self.all_sprites:
            if pygame.sprite.collide_mask(i, self) and type(i) == Stone:
                if i.trap or abs(self.rect.y - i.rect.y) < int(self.height * 0.5):
                    print(self.height + self.rect.y - i.rect.y - 1)
                    exit()  # TODO
                if abs(self.rect.y - i.rect.y) < self.height:
                    self.rect.y -= self.height + self.rect.y - i.rect.y - 1

                self.collide = False
            if pygame.sprite.collide_mask(i, self) and type(i) == Portal:
                self.g *= -1

        self.g -= self.height * 0.01

        if self.g ** 2 > int(self.height * 0.5):
            self.rect.y -= -1 * (int(self.height * 0.5) - 2) ** 0.5
        elif self.g != 0:
            self.rect.y -= int(self.g * abs(self.g))
