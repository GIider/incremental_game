# -*- coding: utf-8 -*-
import sys

from ..constants import *
from ..unit import units

__all__ = ['MainMenu', 'PurchaseUnitMenu', 'SellUnitMenu']


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

    def add_message(self, text):
        self.user_interface.add_message(text=text)

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
        return [unit.get_unit_description() for unit in units]

    def enter(self):
        unit_class = units[self.position]

        if self.user_interface.game.player.purchase(unit_class=unit_class):
            self.add_message('Purchased {}'.format(unit_class.__name__))
        else:
            self.add_message('Can\'t afford {}'.format(unit_class.__name__))


class SellUnitMenu(Menu):
    @property
    def items(self):
        return [unit.get_unit_description() for unit in units]

    def enter(self):
        unit_class = units[self.position]

        if self.user_interface.game.player.sell(unit_class=unit_class):
            self.add_message('Sold {}'.format(unit_class.__name__))
        else:
            self.add_message('Can\'t sell {}'.format(unit_class.__name__))
