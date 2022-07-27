import os.path as path
import pathlib
from typing import Callable

import pygame
import pygame.freetype  # needs to be imported explicitly

pygame.freetype.init()  # must also be initialised explicitly and separately from the remainder of pygame


def _resource_path(file: str):
    """Return the absolute path for a file."""
    pathobj = pathlib.Path(file).absolute()
    return path.join(*pathobj.parts)


button = pygame.image.load(_resource_path("assets/button.png")).convert_alpha()
button_clicked = pygame.image.load(_resource_path("assets/button_clicked.png")).convert_alpha()
nickname_input = pygame.image.load(_resource_path("assets/nickname_input.png")).convert_alpha()


class GUIItem(pygame.sprite.Sprite):
    """Base class for all GUI items."""

    font = pygame.freetype.Font(_resource_path("assets/scj2022.ttf"), 10)
    font.fgcolor = pygame.Color("white")


class Button(GUIItem):
    """A clickable button meant for GUI elements."""

    def __init__(self, pos: tuple[int, int], text: str, func: Callable):
        super().__init__()
        self.pos = pos
        self.text = text
        self.func = func
        self._img_list = []
        self._init_img_list()
        self.image = self._img_list[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args, **kwargs):
        """Update the currently showing Image, based on if the button is pressed."""
        self.image = self._img_list[self.clicked]

    @property
    def clicked(self):
        """Return if the button is currently clicked."""
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def click(self):
        """Actually activate the button press."""
        self.func()

    def _init_img_list(self):
        # PRIVATE USE ONLY!
        text, text_rect = self.font.render(self.text)
        text = text.convert_alpha()
        img = pygame.Surface((8 + text_rect.width, button.get_height())).convert_alpha()
        img2 = img.copy()
        for _ in range(2):
            img.blit(button, (0, 0), area=pygame.Rect(0, 0, 4, button.get_height()))
            img2.blit(button_clicked, (0, 0), area=pygame.Rect(0, 0, 4, button.get_height()))
            if not _:
                img = pygame.transform.flip(img, True, False).convert_alpha()
                img2 = pygame.transform.flip(img2, True, False).convert_alpha()
        text_rect.center = img.get_width() // 2, img.get_height() // 2
        button_slice = pygame.Rect(4, 0, 1, 16)
        for x in range(4, img.get_width() - 4):
            img.blit(button, (x, 0), area=button_slice)
            img2.blit(button_clicked, (x, 0), area=button_slice)
        img.blit(text, text_rect)
        img2.blit(text, text_rect)
        blank = pygame.Color(0, 0, 0, 0)
        width, height = img.get_size()
        with pygame.PixelArray(img) as pxarray, pygame.PixelArray(img2) as pxarray2:
            for array in (pxarray, pxarray2):
                array[:2, :2] = blank
                array[2:4, 0] = blank
                array[0, 2:4] = blank
                array[0, 12:14] = blank
                array[:2, 14:] = blank
                array[2:4, 15] = blank
                array[width - 2 :, :2] = blank
                array[width - 4 : width - 2, 0] = blank
                array[width - 1, 2:4] = blank
                array[width - 2 :, 14:] = blank
                array[width - 1, 12:14] = blank
                array[width - 4 : width - 2, 15] = blank
        self._img_list.append(img)
        self._img_list.append(img2)


class TextInput(GUIItem):
    """Nickname text input"""

    _input_rect = pygame.Rect(12, 66, 136, 12)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = nickname_input
        self.text = ""
        self.rect = self.image.get_rect(center=(160 // 2, 144 // 2))
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self._input_rect)

    def fetch(self, text):
        """Update the text to display."""
        self.text += text
        self.update()

    def kill(self):
        super().kill()
        pygame.key.stop_text_input()
        self.game.nickname = self.text
        self.game.inputting_nickname = False

    def update(self, *args, **kwargs):
        self.image = nickname_input.copy()
        txt = self.font.render(self.text)
        txt[1].center = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.image.blit(*txt)