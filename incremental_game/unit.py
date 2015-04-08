# -*- coding: utf-8 -*-


class BaseUnit(object):
    COST = None
    GENERATION_RATE = None

    @classmethod
    def get_unit_description(cls):
        return '{unit.__name__} (-{unit.COST} +{unit.GENERATION_RATE}/s)'.format(unit=cls)

class Worker(BaseUnit):
    COST = 10
    GENERATION_RATE = 1


class SuperWorker(BaseUnit):
    COST = 100
    GENERATION_RATE = 15


units = (Worker, SuperWorker)
