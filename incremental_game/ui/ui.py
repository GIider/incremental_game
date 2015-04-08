# -*- coding: utf-8 -*-
import time
import os

from .menu import *

MAX_MESSAGES = 5
HEADING_TEXT = '''\r## THE GAME HAS BEEN RUNNING FOR {self.game.time_running:.0f} SECONDS! ##

You have {self.game.player.cash:.2f} (+ {self.game.player.money_generated_per_second:.2f}/s) cash!

Units:
------
{self.game.player.verbose_unit_ownership}

Messages:
---------
{self.messages}

Menu:
-----
{self.current_menu.text}
'''


__all__ = ['UserInterface']


class UserInterface(object):
    def __init__(self, game):
        self.game = game
        self.menu_stack = []
        self.message_stack = ['' for _ in range(MAX_MESSAGES)]
        self.previous_text = ''

        self.show_sub_menu(menu_class=MainMenu)

    def show_sub_menu(self, menu_class):
        menu_instance = menu_class(user_interface=self)
        self.menu_stack.insert(0, menu_instance)

    def close_current_menu(self):
        self.menu_stack.pop(0)

    def add_message(self, text):
        text = '{}: {}'.format(time.strftime('%H:%m:%S'), text)
        self.message_stack.insert(0, text)

        if len(self.message_stack) > MAX_MESSAGES:
            self.message_stack.pop(-1)

    @property
    def current_menu(self):
        return self.menu_stack[0]

    @property
    def messages(self):
        return '\n'.join(self.message_stack)

    def process(self, user_input):
        self.current_menu.process(user_input=user_input)

    def render(self):
        text = HEADING_TEXT.format(self=self)

        if text != self.previous_text:
            os.system('cls')
            print(text, end='')

        self.previous_text = text


