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
                 position: tuple, scale: int) -> None:
        self.signal_func = None
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def set_signal_func(self, func: ...) -> None:
        self.signal_func = func

    def click(self, pos) -> None:
        if self.rect.collidepoint(pos) and self.signal_func:
            self.signal_func()


class GMD:
    def __init__(self, fps: int, width: int, height: int) -> None:
        global screen
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('data/menuLoop.mp3')
        pygame.mixer.music.play(-1)
        self.width = width
        self.height = height
        self.running = True
        self.FPS = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.transform.scale(load_image('background.gif'), (self.width, self.height))
        pygame.display.set_caption('GMD v 1.0       by o2o and SAVITSKY')
        self.init_buttons()

    def init_buttons(self) -> None:
        self.butt_group = []

        self.play_button = Button(load_image('play_button.png'), (self.width * 0.4, self.height * 0.2), 0.9)
        self.play_button.set_signal_func(self.start_game_button)
        self.butt_group.append(self.play_button)

        self.icons_button = Button(load_image('icon_set_button.png'), (self.width * 0.2, self.height * 0.2), 0.9)
        self.icons_button.set_signal_func(self.set_icon_button)
        self.butt_group.append(self.icons_button)
        
        self.redactor_button = Button(load_image('editor_button.png'), (self.width * 0.6, self.height * 0.2), 0.9)
        self.redactor_button.set_signal_func(self.editor_button)
        self.butt_group.append(self.redactor_button)
    
    def init_background(self):
        self.screen.blit(self.background, (0, 0))

    def start_game(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            clock.tick(self.FPS)
            pygame.display.flip()

    def start_window(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in self.butt_group:
                        i.click(event.pos)

            self.screen.fill((0, 0, 0))
            self.init_background()
            for i in self.butt_group:
                i.draw(self.screen)
            pygame.display.flip()
            clock.tick(self.FPS)

    def start_game_button(self):
        print('start_game_button')

    def set_icon_button(self):
        print('set_icon_button')

    def editor_button(self):
        print('editor_button')


if __name__ == "__main__":
    screen = None
    gmd = GMD(240, 1500, 800)
    gmd.start_window()
    pygame.quit()
