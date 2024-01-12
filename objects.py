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
            return True


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos, scale, all):
        super().__init__(all)

        screen1 = pygame.Surface((128, 128))
        screen1.fill((0, 0, 0))
        pygame.draw.rect(screen1, 'white', (0, 0, 128, 128), 5)

        self.width = screen1.convert_alpha().get_width()
        self.height = screen1.convert_alpha().get_height()
        self.image = pygame.transform.scale(
            screen1.convert_alpha(), (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect.x -= self.width // 15


class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, scale, all):
        super().__init__(all)
        self.original_image = load_image('spike.png')
        self.width = self.original_image.get_width()
        self.height = self.original_image.get_height()
        self.image = pygame.transform.scale(self.original_image, (int(self.width * scale), int(self.height * scale)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect.x -= self.width // 15

class Final_line(pygame.sprite.Sprite):
    def __init__(self, pos, scale, all):
        super().__init__(all)
        self.original_image = load_image('final_line.png')
        self.width = self.original_image.get_width()
        self.height = self.original_image.get_height()
        self.image = pygame.transform.scale(self.original_image, (int(self.width * scale), int(self.height * scale)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
    def update(self):
        self.rect.x -= self.width // 15


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, scale: float,
                 all: pygame.sprite.Sprite, icon: pygame.image):
        super().__init__(all)
        self.width = icon.get_width()
        self.height = icon.get_height()
        self.image = pygame.transform.scale(icon, (int(self.width * scale), int(self.height * scale)))
        self.image_rotate = pygame.transform.scale(icon, (int(self.width * scale), int(self.height * scale)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.all_sprites = all

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.jump_bul = False

        self.g = self.height * 0.01

        self.collide = False

        self.rotation = 4.5

        self.a = Stone((0, 0), 0.5, all)
        
        self.islive, self.isfinal = True, False

    def update(self):
        self.g -= self.height * 0.004

        self.rect.y -= int(self.g * abs(self.g)) / 240 * 90

        self.collide = True
        for i in self.all_sprites:
            if pygame.sprite.collide_mask(i, self) and \
                    (type(i) == Stone or type(i) == Spike or type(i) == Final_line):
                if type(i) == Spike and self.width * 0.1 < abs(self.rect.x - i.rect.x) < self.width * 0.9:
                    self.islive = False
                elif type(i) == Final_line:
                    self.islive, self.isfinal = False, True
                if abs(self.rect.y - i.rect.y) <= self.height:
                    self.rect.y -= self.height // 2 + self.rect.y - i.rect.y - 1

                self.collide = False
                if self.g < self.height * 0.06:
                    self.g = -self.height * 0.05
                self.a = i

        if self.collide:
            self.rotation -= 4.5
            self.rotation %= 180
            self.image = pygame.transform.rotate(self.image_rotate, self.rotation)
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.rotation //= 4
            self.image = pygame.transform.rotate(self.image_rotate, self.rotation)
            self.mask = pygame.mask.from_surface(self.image)
