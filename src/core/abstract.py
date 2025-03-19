import shlex
import subprocess
from abc import ABC, abstractmethod
from datetime import datetime
from time import sleep
from typing import Any, Optional


class AbstractPlayer(ABC):
    """Base player class that manages external process communication."""

    def __init__(self, command: str, log: bool = False, debug: bool = False):
        self.process: Optional[subprocess.Popen] = None
        self.command = command
        self.log = log

    def _log_operation(self, operation: str, data: str) -> None:
        if not self.log:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_entry = f"[{timestamp}] {operation}: {data}\n"
        try:
            with open("log.txt", "a") as log_file:
                log_file.write(log_entry)
        except IOError:
            pass

    def start(self) -> None:
        self.process = subprocess.Popen(
            shlex.split(self.command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def write(self, data: str) -> None:
        if self.process and self.process.stdin:
            try:
                self.process.stdin.write(f"{data}\n")
                self.process.stdin.flush()
                if self.log:
                    self._log_operation("WRITE", data)
            except (BrokenPipeError, IOError):
                if self.log:
                    self._log_operation("WRITE_ERROR", f"Error writing '{data}'")

    def read(self) -> str:
        if self.process and self.process.stdout:
            data = self.process.stdout.readline().strip()
            if self.log:
                self._log_operation("READ", data)
            return data
        return ""

    def stop(self) -> None:
        sleep(0.25)
        if self.process:
            try:
                for pipe in [self.process.stdin, self.process.stdout, self.process.stderr]:
                    try:
                        if pipe:
                            pipe.close()
                    except (BrokenPipeError, IOError):
                        pass

                self.process.terminate()
                try:
                    self.process.wait(timeout=1.0)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    try:
                        self.process.wait(timeout=1.0)
                    except (subprocess.TimeoutExpired, ProcessLookupError):
                        pass
            except ProcessLookupError:
                pass
            finally:
                self.process = None

    def __del__(self):
        self.stop()


class AbstractGame(ABC):
    """Abstract base class for turn-based games between two players."""

    def __init__(self, player1: AbstractPlayer, player2: AbstractPlayer) -> None:
        self._player1 = player1
        self._player2 = player2
        self._current_player = player1
        self._is_game_over = False

    @property
    def current_player(self) -> AbstractPlayer:
        return self._current_player

    def switch_player(self) -> None:
        self._current_player = self._player2 if self._current_player == self._player1 else self._player1

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @abstractmethod
    def initialize_game(self) -> None:
        pass

    @abstractmethod
    def make_move(self, move: Any) -> bool:
        pass

    @abstractmethod
    def determine_winner(self) -> Optional[AbstractPlayer]:
        pass


class WebGame(ABC):
    """Abstract base class for web-enabled games"""

    def __init__(self, template_folder):
        from flask import Flask
        from flask_cors import CORS

        self.app = Flask(__name__, template_folder=template_folder)
        CORS(self.app)
        self.game_history = []
        self.app.route("/")(self.get_index)
        self.app.route("/game-state")(self.get_game_state_json)

    @abstractmethod
    def get_game_state_json(self):
        pass

    @abstractmethod
    def get_index(self):
        pass

    def start_web_server(self, port=8000):
        import threading

        from click import echo
        from waitress import serve

        url = f"http://localhost:{port}"
        echo(f"\n🎮 Game visualization available at: 🌐 {url}")
        threading.Thread(
            target=lambda: serve(self.app, host="0.0.0.0", port=port), daemon=True
        ).start()
