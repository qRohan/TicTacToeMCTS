from __future__ import annotations
import math
import copy
import random
from dataclasses import dataclass
from typing import TypeAlias

from TicTacToe import GameBoard, PlayerIdType

move_type: TypeAlias = tuple[int, int]

@dataclass
class GameResults():
    WIN = "WIN"
    LOSS = "LOSS"
    DRAW = "DRAW"
    NO_RESULT = "NO_RESULT"
    
    WIN_VALUE = 1
    LOSS_VALUE = -1
    DRAW_VALUE = 0
    RESULT_VALUES = {WIN: WIN_VALUE, LOSS: LOSS_VALUE, DRAW: DRAW_VALUE}

    @classmethod
    def reverse_result(cls, result : str):
        match result:
            case cls.WIN : return cls.LOSS
            case cls.LOSS : return cls.WIN
            case cls.DRAW : return cls.DRAW
            case _ : return cls.NO_RESULT


class MCTSNode():
    def __init__(self, state: GameBoard, player: PlayerIdType , children: list[MCTSNode] = [], parent: MCTSNode | None = None) -> None:
        self.v = 0
        self.n = 0
        self.parent = parent
        self.player = player
        self.children = children
        self.state = state

    def get_uct(self) -> float:
        uct = float("inf")
        if self.n == 0:
            return uct
        c = 2
        if self.parent:
            uct = (self.v / self.n) + c * \
                math.sqrt(math.log(self.parent.n) / self.n)
        return uct

    def rollout(self, player: int):
        state = copy.deepcopy(self.state)
        while True:
            if state.terminal_state():
                val = None
                if state.winner == player:
                    val = GameResults.WIN
                elif state.winner == (player % 2+1):
                    val = GameResults.LOSS
                elif state.winner == 0:
                    val = GameResults.DRAW
                else:
                    val = GameResults.NO_RESULT
                return val
            state = state.play(random.choice(state.get_valid_moves()))

    def select(self):
        return max(self.children, key=lambda child: child.get_uct())

    def expand(self):
        self.children = [self.create_child(move, GameBoard.next_player(self.player))
                         for move in self.state.get_valid_moves()]
                        

    def backpropogate(self, value: str, root_player: PlayerIdType, discount_rate: float = 1.0):
        self.n += 1
        res = GameResults.reverse_result(value) if self.player == root_player else value
        self.v += GameResults.RESULT_VALUES[res] * discount_rate
        if self.parent:
            self.parent.backpropogate(value, root_player, discount_rate * 1)

    def create_child(self, move: move_type, player: PlayerIdType):
        return MCTSNode(self.state.play(move), player, [], self)

# print(GameResults.reverse_result("WIN"))