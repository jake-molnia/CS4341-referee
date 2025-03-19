from flask import jsonify, render_template

from ..config import GameConfig
from .abstract import WebGame


class TicTacToeWeb(WebGame):
    def __init__(self, game):
        super().__init__(GameConfig.WEB_TEMPLATE_FOLDER)
        self.game = game
        self.game_history = []
        self.board_states = []
        self.end_message = None

    def get_game_state_json(self):
        """Return current game state as JSON"""
        game_data = {
            "board": self.game.board,
            "currentPlayer": self.game.current_player.get_symbol(),
            "isGameOver": self.game.is_game_over,
            "history": {
                "moves": self.game_history,
                "boards": self.board_states,
            },
            "endMessage": self.end_message if self.game.is_game_over else None,
        }
        return jsonify(game_data)

    def get_index(self):
        """Render template with game state data"""
        game_data = {
            "board": self.game.board,
            "currentPlayer": self.game.current_player.get_symbol(),
            "isGameOver": self.game.is_game_over,
            "history": {
                "moves": self.game_history,
                "boards": self.board_states,
            },
            "endMessage": self.end_message if self.game.is_game_over else None,
        }
        return render_template("./tictactoe/index.html", game_data=game_data)

    def update_history(self, move: str):
        """Update game history with new move"""
        move_data = {"move": move, "player": self.game.current_player.get_symbol()}
        self.game_history.append(move_data)
        self.board_states.append(self.game.board.copy())


class LaskerMorrisWeb(WebGame):
    def __init__(self, game):
        super().__init__(GameConfig.WEB_TEMPLATE_FOLDER)
        self.game = game
        self.end_message = None

    def get_game_state_json(self):
        game_data = {
            "board": self.game.board,
            "playerHands": self.game.player_hands,
            "currentPlayer": self.game.current_player.get_color(),
            "isGameOver": self.game.is_game_over,
            "invalidFields": list(self.game.invalid_fields),
            "history": {
                "moves": self.game.game_history,
                "boards": self.game.board_states,
                "hands": self.game.hand_states,
            },
            "endMessage": self.end_message if self.game.is_game_over else None,
        }
        return jsonify(game_data)

    def get_index(self):
        """Render template with game state data"""
        game_data = {
            "board": self.game.board,
            "playerHands": self.game.player_hands,
            "currentPlayer": self.game.current_player.get_color(),
            "isGameOver": self.game.is_game_over,
            "invalidFields": list(self.game.invalid_fields),
            "history": {
                "moves": self.game.game_history,
                "boards": self.game.board_states,
                "hands": self.game.hand_states,
            },
            "endMessage": self.end_message if self.game.is_game_over else None,
        }
        return render_template("./lasker_morris/index.html", game_data=game_data)
