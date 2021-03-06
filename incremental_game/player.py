# -*- coding: utf-8 -*-
from .unit import units


class Player(object):
    def __init__(self):
        self.cash = 250
        self.units = {}

    def purchase(self, unit_class):
        """Purchase a unit

        Returns True if the unit could be purchased
        """
        if unit_class.COST > self.cash:
            return False

        self.cash -= unit_class.COST
        self.units[unit_class] = self.units.get(unit_class, 0) + 1

        return True

    def sell(self, unit_class):
        """Sell a unit

        Returns True if the unit could be sold
        """
        amount_of_units = self.units.get(unit_class, 0)

        if amount_of_units == 0:
            return False

        self.units[unit_class] -= 1
        self.cash += unit_class.COST * 0.5

        return True

    @property
    def money_generated_per_second(self):
        return sum((unit_class.GENERATION_RATE * amount_of_units for
                    unit_class, amount_of_units in self.units.items()))

    @property
    def verbose_unit_ownership(self):
        text = ''

        for unit in units:
            text += '{}: {}\n'.format(unit.__name__, self.units.get(unit, 0))

        return text