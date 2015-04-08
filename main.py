# -*- coding: utf-8 -*-
from incremental_game import Game

if __name__ == '__main__':
    game = Game()

    try:
        game.run()
    except KeyboardInterrupt:
        pass
