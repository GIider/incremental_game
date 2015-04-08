# -*- coding: utf-8 -*-
import time
import msvcrt

from .constants import *
from .ui import UserInterface


MS_PER_UPDATE = 1


class Game(object):
    def __init__(self, player):
        self.player = player
        self.starting_time = time.time()
        self.running = True

        self.ui = UserInterface(game=self)

    @property
    def time_running(self):
        return time.time() - self.starting_time

    def run(self):
        """Main game loop"""
        previous_time = time.time()

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - previous_time

            user_input = self.fetch_input()
            self.process_input(user_input)

            self.update(elapsed_time)
            self.render()

            previous_time = current_time

    def fetch_input(self):
        """Check for command line input and return valid inputs

        Either returns a member of the KEY enum or None
        """
        if msvcrt.kbhit():
            char = msvcrt.getch()

            if char == SPECIAL_KEY:
                char = msvcrt.getch()

                if char == RAW_KEY_UP:
                    return KEY.UP

                elif char == RAW_KEY_DOWN:
                    return KEY.DOWN

            elif char == RAW_KEY_ESCAPE:
                return KEY.ESCAPE

            elif char == RAW_KEY_ENTER:
                return KEY.ENTER

        return None

    def process_input(self, user_input):
        self.ui.process(user_input)

    def update(self, elapsed_time):
        self.player.cash += self.player.money_generated_per_second * elapsed_time

    def render(self):
        self.ui.render()