import word_game.reduction_game as redux
import word_game.chain_game as chain
import word_game.hex_game as hex

GAME_DICT = {
    "redux": redux,
    "chain": chain,
    "hex": hex,
    }

def new_game(game_name, seed_word=None):
    try:
        module = GAME_DICT[game_name]
        module.start(seed_word)
    except KeyError as e:
        print(f"{game_name} is not a game we offer")
