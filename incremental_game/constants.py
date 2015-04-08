# -*- coding: utf-8 -*-
import enum

SPECIAL_KEY = b'\xe0'

RAW_KEY_UP = b'H'
RAW_KEY_DOWN = b'P'
RAW_KEY_ESCAPE = b'\x1b'
RAW_KEY_ENTER = b'\r'


class KEY(enum.Enum):
    UP = 0
    DOWN = 1
    ESCAPE = 2
    ENTER = 3