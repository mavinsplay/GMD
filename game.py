from editor import Editor, loadLevel, Stone
from objects import Button, load_image
import pygame
import os


class GMD:
    def __init__(self, fps: int, width: int, height: int) -> None:
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.running = True
        self.levels_buttons = True
        self.editor_screen = True
        self.icons_buttons = True
        self.FPS = fps
        self.init_music()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.transform.scale(
            load_image('background.gif'), (self.width, self.height))
        self.background1 = pygame.transform.scale(
            load_image('background.png'), (self.width, self.height))
        pygame.display.set_caption('GMD v 1.0       by o2o and SAVITSKY')
        self.select_icon = load_image('icon_1.png')
        self.init_start_buttons()
        self.init_icons_buttons()
        self.init_levels_buttons()

    def init_music(self, path: str = 'data/menuLoop.mp3', time: int = -1) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def init_start_buttons(self) -> None:
        self.start_butt_group = []

        self.levels_buttons = Button(load_image(
            'play_button.png'), (self.width * 0.4, self.height * 0.2), 0.9)
        self.levels_buttons.set_callback_func(self.levels_window)
        self.start_butt_group.append(self.levels_buttons)

        self.icons_button = Button(load_image(
            'icons_set_button.png'), (self.width * 0.2, self.height * 0.2), 0.9)
        self.icons_button.set_callback_func(self.set_icon_button)
        self.start_butt_group.append(self.icons_button)

        self.redactor_button = Button(load_image(
            'editor_button.png'), (self.width * 0.6, self.height * 0.2), 0.9)
        self.redactor_button.set_callback_func(self.editor)
        self.start_butt_group.append(self.redactor_button)

    def init_levels_buttons(self) -> None:
        self.levels_button_group = []

        self.back_button = Button(load_image('back_button.png'), (0, 0), 0.8)
        self.back_button.set_callback_func(
            lambda: self.back_button_callback('play-to-menu'))
        self.levels_button_group.append(self.back_button)

        self.level_1_button = Button(load_image(
            'level_1_button.png'), (self.width * 0.1, self.height * 0.25), 2.5)
        self.level_1_button.set_callback_func(lambda: self.start_level(1))
        self.levels_button_group.append(self.level_1_button)

        self.level_2_button = Button(load_image(
            'level_2_button.png'), (self.width * 0.4, self.height * 0.25), 2.5)
        self.level_2_button.set_callback_func(lambda: self.start_level(2))
        self.levels_button_group.append(self.level_2_button)

        self.level_3_button = Button(load_image(
            'level_3_button.png'), (self.width * 0.7, self.height * 0.25), 2.5)
        self.level_3_button.set_callback_func(lambda: self.start_level(3))
        self.levels_button_group.append(self.level_3_button)

    def init_icons_buttons(self) -> None:
        self.icons_buttons_group = []

        self.back_button = Button(load_image('back_button.png'), (0, 0), 0.8)
        self.back_button.set_callback_func(
            lambda: self.back_button_callback('icons-to-menu'))
        self.icons_buttons_group.append(self.back_button)

        self.icons = {}
        x = 0.1
        y = 0.65
        # получение списка всех фалйов в каталоге data
        icons = os.listdir('data')
        for i, name in enumerate(list(filter(lambda x: 'icon_' in x, icons))):
            if i == 8:
                x = 0.1
                y += 0.18
            self.icons[name] = Button(load_image(
                name), (self.width * x, self.height * y), 0.8)
            self.icons[name].set_callback_func(lambda n=name: self.set_icon(n))
            x += 0.1

    def back_button_callback(self, call: str) -> None:
        if call == 'play-to-menu':
            self.levels_buttons = False
            self.start_window()
        elif call == 'editor-to-menu':
            self.editor_screen = False
            self.start_window()
        elif call == 'icons-to-menu':
            self.icons_buttons = False
            self.start_window()

    def init_background(self) -> None:
        self.screen.blit(self.background, (0, 0))  # доделать до анимации

    def set_icon(self, icon: str) -> None:
        self.icons_button = False
        self.select_icon = load_image(icon)
        self.set_icon_button()

    def start_window(self) -> None:
        pygame.display.set_caption('Инициализация игры')
        self.screen.fill((0, 0, 0))
        self.init_background()
        for i in self.start_butt_group:
            i.draw(self.screen)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in self.start_butt_group:
                        i.click(event.pos)
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def levels_window(self) -> None:
        self.levels_buttons = True

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background1, (0, 0))
        for i in self.levels_button_group:
            i.draw(self.screen)

        while self.running and self.levels_buttons:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in self.levels_button_group:
                        i.click(event.pos)

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def set_icon_button(self) -> None:
        self.icons_buttons = True
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background1, (0, 0))
        self.screen.blit(pygame.transform.scale(load_image(
            'editor_surface.png'), (self.width, self.height * 0.4)), (0, self.height * 0.6))
        self.screen.blit(pygame.transform.scale(self.select_icon, (self.width *
                         0.2, self.height * 0.36)), (self.width * 0.4, self.height * 0.1))
        for i in self.icons_buttons_group:
            i.draw(self.screen)

        for i, j in self.icons.items():
            j.draw(self.screen)

        while self.running and self.icons_buttons:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in self.icons_buttons_group:
                        i.click(event.pos)
                    for i, j in self.icons.items():
                        j.click(event.pos)
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def editor(self) -> None:
        pygame.mixer.music.stop()
        self.screen.fill((0, 0, 0))
        self.editor_screen = True
        self.back_button = Button(load_image('back_button.png'), (0, 0), 0.3)
        self.back_button.set_callback_func(
            lambda: self.back_button_callback('editor-to-menu'))
        self.back_button.draw(self.screen)
        self.edit = Editor(self.width, self.height, self.screen, self.select_icon)
        self.init_music()
        self.start_window()

    def start_level(self, level_nr: int = 1):
        pygame.mixer.music.stop()
        all_sprites = pygame.sprite.Group()
        scale = 0.04
        v = 10000
        person = loadLevel(self.width, self.height,
                           scale, all_sprites, level_nr, f'{str(level_nr).rjust(3, "0")}.mp3',
                           self.select_icon)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not person.collide:
                        person.jump_bul = True
                    if event.key == pygame.K_ESCAPE:
                        return (self.init_music(), self.levels_window())
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        person.jump_bul = False
            if person.jump_bul and person.g <= -person.height * 0.13:
                person.g = person.height * 0.13

            all_sprites.update()
            self.screen.fill((255, 255, 255))
            all_sprites.draw(self.screen)
            self.clock.tick(v / self.FPS)
            pygame.display.flip()


if __name__ == "__main__":
    gmd = GMD(240, 1500, 800)
    gmd.start_window()
    pygame.quit()
