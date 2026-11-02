"""The phone screen: one 240x320 surface, shown in a window scaled by an integer factor.

Headless mode (SDL_VIDEODRIVER=dummy) is used by tools/shot.py and tests.
"""
import os

import pygame

import config

screen = None      # pygame.Surface 240x320 - what the game draws on
window = None      # the real window (scaled)
frame_hooks = []   # callables(screen) after every painted frame (screenshots, tests)


def init(headless=False):
    global screen, window
    if headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    w, h = config.SCREEN_W * config.SCALE, config.SCREEN_H * config.SCALE
    window = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Path of a Warrior")
    screen = pygame.Surface((config.SCREEN_W, config.SCREEN_H)).convert()
    screen.fill((0, 0, 0))


def present():
    for hook in frame_hooks:
        hook(screen)
    if window is not None:
        if config.SCALE == 1:
            window.blit(screen, (0, 0))
        else:
            pygame.transform.scale(screen, window.get_size(), window)  # nearest neighbour
        pygame.display.flip()
