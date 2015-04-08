# -*- coding: utf-8 -*-
from game import Game
from player import Player

if __name__ == '__main__':
    player = Player()
    game = Game(player=player)

    try:
        game.run()
    except KeyboardInterrupt:
        pass
