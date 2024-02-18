from Game.game import Game
from cProfile import Profile
from pstats import Stats

if __name__ == "__main__":
    with Profile() as profile:
        game1 = Game()
        Stats(profile).strip_dirs().sort_stats("cumulative").print_stats()
