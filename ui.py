# -*- coding: utf-8 -*-
import sys
import os

from constants import *
from unit import Worker


HEADING_TEXT = '''\r## THE GAME HAS BEEN RUNNING FOR {self.game.time_running:.0f} SECONDS! ##

You have {self.game.player.cash:.2f} (+ {self.game.player.money_generated_per_second:.2f}/s) cash!

Units:
------
{self.game.player.verbose_unit_ownership}


'''


class UserInterface(object):
    def __init__(self, game):
        self.game = game
        self.menu_stack = []

        self.show_sub_menu(menu_instance=MainMenu(user_interface=self))

    def show_sub_menu(self, menu_instance):
        self.menu_stack.insert(0, menu_instance)

    def close_current_menu(self):
        self.menu_stack.pop(0)

    @property
    def current_menu(self):
        return self.menu_stack[0]

    def process(self, user_input):
        menu = self.menu_stack[0]

        menu.process(user_input=user_input)

    def render(self):
        os.system('cls')

        text = HEADING_TEXT.format(self=self)
        text += self.current_menu.text

        print(text, end='')


class Menu(object):
    def __init__(self, user_interface):
        self.position = 0
        self.user_interface = user_interface

    @property
    def items(self):
        return []

    def process(self, user_input):
        if user_input == KEY.UP:
            self.position -= 1
        elif user_input == KEY.DOWN:
            self.position += 1
        elif user_input == KEY.ENTER:
            self.enter(self.position)

        if self.position < 0:
            self.position = len(self.items) - 1
        elif self.position > len(self.items) - 1:
            self.position = 0

    def enter(self, position):
        raise NotImplementedError()

    @property
    def text(self):
        items = list(self.items)
        items[self.position] = '> {}'.format(items[self.position])

        return '\n'.join(items)


class MainMenu(Menu):
    POSITION_BUY = 0
    POSITION_EXIT_GAME = 1

    @property
    def items(self):
        return ('Buy Items',
                'Exit Game')

    def enter(self, position):
        if position == self.POSITION_EXIT_GAME:
            sys.exit(0)

        elif position == self.POSITION_BUY:
            sub_menu = PurchaseUnitMenu(user_interface=self.user_interface)
            self.user_interface.show_sub_menu(sub_menu)


class PurchaseUnitMenu(Menu):
    POSITION_BUY_UNIT = 0
    POSITION_SELL_UNIT = 1
    POSITION_EXIT_MENU = 2

    @property
    def items(self):
        return ('Purchase Unit',
                'Sell Unit',
                'Cancel')

    def enter(self, position):
        if position == self.POSITION_BUY_UNIT:
            self.user_interface.game.player.purchase(unit_class=Worker)

        elif position == self.POSITION_SELL_UNIT:
            self.user_interface.game.player.sell(unit_class=Worker)

        elif position == self.POSITION_EXIT_MENU:
            self.user_interface.close_current_menu()