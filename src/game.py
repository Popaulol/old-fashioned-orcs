import os.path as path
import pathlib

import pygame
import pytmx

import src.client.client as client
import src.player as player
import src.solid as solid

pygame.mixer.init()


def _resource_path(file: str):
    """Return the absolute path for a file."""
    pathobj = pathlib.Path(file).absolute()
    return path.join(*pathobj.parts)


game_crash = pygame.mixer.Sound(_resource_path("assets/game_crash.wav"))
game_crash.set_volume(0.35)  # We don't want players to get their eardrums destroyed


class Game:
    """The Game"""

    def __init__(self):
        self.player = player.Player(self)
        self.tiles = pygame.sprite.LayeredUpdates()
        self.other_players = pygame.sprite.Group()
        self.objects = pygame.sprite.LayeredUpdates(self.player)
        self.crashing = False
        self.tmx_data: pytmx.TiledMap | None = None
        self.client = client.Client(self)
        self.level = -1  # Value for the test map.
        self.read_map("maps/test.tmx")

    def crash(self):
        """<<Crash>> the game."""
        self.crashing = True
        game_crash.play(-1)

    def read_map(self, directory):
        """This reads the TMX Map data"""
        # TMX is a variant of the XML format, used by the map editor Tiled.
        # Said maps use tilesets, stored in TSX files (which are also based on the XML format).
        self.tmx_data = pytmx.TiledMap(_resource_path(directory))
        for sprite in self.tiles:
            sprite.kill()
        for layer in range(len(list(self.tmx_data.visible_tile_layers))):
            for tile_y in range(self.tmx_data.height):
                for tile_x in range(self.tmx_data.width):
                    tile = self.tmx_data.get_tile_properties(tile_x, tile_y, layer)
                    if tile is None:
                        continue
                    if not tile["id"]:
                        # Solid tile
                        self.tiles.add(solid.Solid(self, (tile_x, tile_y), layer), layer=layer)
                    elif tile["id"] == 1:
                        # "Glitchy" tile (starts a pseudo-crash upon contact)
                        self.tiles.add(solid.BuggyThingy(self, (tile_x, tile_y), layer), layer=layer)
        for sprite in self.tiles:
            self.objects.add(sprite, layer=self.tiles.get_layer_of_sprite(sprite))

    def add_player(self, nickname, pos=None):
        """Adds a player that joined the game online."""
        if pos is None:
            pos = [0, 0]
        new_player = player.OtherPlayer(nickname)
        self.other_players.add(new_player)
        self.objects.add(new_player, layer=0)
        new_player.rect.topleft = tuple(pos)

    def update_player(self, nickname, pos=None):
        """Update players movement"""
        if pos is None:
            pos = [0, 0]
        if not any(other_player for other_player in self.other_players if other_player.nickname == nickname):
            raise Exception(f"invalid player : {nickname}")
        for other_player in self.other_players:
            if other_player.nickname == nickname:
                other_player.rect.topleft = tuple(pos)
