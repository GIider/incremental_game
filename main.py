# -*- coding: utf-8 -*-
from incremental_game.game import Game
from incremental_game.player  import Player

if __name__ == '__main__':
    player = Player()
    game = Game(player=player)

    try:
        game.run()
    except KeyboardInterrupt:
        pass
