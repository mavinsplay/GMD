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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, all_sprites):
        self.all_sprites = all_sprites
        super().__init__(self.all_sprites)
        self.image = pygame.transform.scale(load_image('icon_1.png '), (31, 31))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.jump = -12
        self.jump_bul = False

        self.collide = False

    def update(self):
        self.collide = True
        for i in self.all_sprites:
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
