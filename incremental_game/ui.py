# -*- coding: utf-8 -*-
import sys
import os

from .constants import *
from .unit import units


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

        self.show_sub_menu(menu_class=MainMenu)

    def show_sub_menu(self, menu_class):
        menu_instance = menu_class(user_interface=self)
        self.menu_stack.insert(0, menu_instance)

    def close_current_menu(self):
        self.menu_stack.pop(0)

    @property
    def current_menu(self):
        return self.menu_stack[0]

    def process(self, user_input):
        self.current_menu.process(user_input=user_input)

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
        raise NotImplementedError()

    def process(self, user_input):
        if user_input == KEY.UP:
            self.position -= 1
        elif user_input == KEY.DOWN:
            self.position += 1
        elif user_input == KEY.ENTER:
            self.enter()
        elif user_input == KEY.ESCAPE:
            self.cancel()

        if self.position < 0:
            self.position = len(self.items) - 1
        elif self.position > len(self.items) - 1:
            self.position = 0

    def enter(self):
        raise NotImplementedError()

    def cancel(self):
        """Cancel this menu instance"""
        self.user_interface.close_current_menu()

    @property
    def text(self):
        # Create a list from the items so we can modify it in place
        items = list(self.items)

        if len(items) == 0:
            return ''

        items[self.position] = '> {}'.format(items[self.position])

        return '\n'.join(items)


class MainMenu(Menu):
    POSITION_BUY_UNITS = 0
    POSITION_SELL_UNITS = 1
    POSITION_EXIT_GAME = 2

    @property
    def items(self):
        return ('Purchase Units',
                'Sell Units',
                'Exit Game')

    def enter(self):
        if self.position == self.POSITION_BUY_UNITS:
            self.user_interface.show_sub_menu(menu_class=PurchaseUnitMenu)

        elif self.position == self.POSITION_SELL_UNITS:
            self.user_interface.show_sub_menu(menu_class=SellUnitMenu)

        elif self.position == self.POSITION_EXIT_GAME:
            self.cancel()

    def cancel(self):
        """End the game"""
        sys.exit(0)


class PurchaseUnitMenu(Menu):

    @property
    def items(self):
        return [unit.__name__ for unit in units]

    def enter(self):
        unit = units[self.position]

        self.user_interface.game.player.purchase(unit_class=unit)


class SellUnitMenu(Menu):

    @property
    def items(self):
        return [unit.__name__ for unit in units]

    def enter(self):
        unit_class = units[self.position]

        self.user_interface.game.player.sell(unit_class=unit_class)