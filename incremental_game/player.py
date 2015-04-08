# -*- coding: utf-8 -*-


class Player(object):
    def __init__(self):
        self.cash = 100
        self.units = {}

    def purchase(self, unit_class):
        """Purchase a unit

        Returns True if the unit could be purchased
        """
        if unit_class.COST > self.cash:
            return False

        else:
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

    @property
    def money_generated_per_second(self):
        return sum((unit_class.GENERATION_RATE * amount_of_units for
                    unit_class, amount_of_units in self.units.items()))

    @property
    def verbose_unit_ownership(self):
        text = ''

        for unit_class, amount in self.units.items():
            text += '{}: {}\n'.format(unit_class.__name__, amount)

        return text