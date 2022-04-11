from __future__ import annotations
from typing import TYPE_CHECKING

from MCTSNode import MCTSNode
if TYPE_CHECKING:
    from TicTacToe import GameBoard


class MCTS():
    def __init__(self, initial_state: GameBoard, player_id: int, num_of_playouts: int) -> None:
        self.initial_state = initial_state
        self.root_node = MCTSNode(self.initial_state, player_id, children=[], parent=None)
        self.num_of_playouts = num_of_playouts
        self.player_id = player_id

    def best_move(self):
        children = self.root_node.children
        # print([child.n for child in children])
        # print([child.v for child in children])
        best_node = max(children, key=lambda child: child.v/child.n)
        best_node_index = children.index(best_node)
        result = self.initial_state.get_valid_moves()[best_node_index]
        return result

    def run_mcts(self):
        for _ in range(self.num_of_playouts):
            self.run_playout()
        return self.best_move()

    def run_playout(self):
        self.current = self.root_node
        while not self.current.state.terminal_state():
            if not self.current.children:
                self.current.expand()
                self.current = self.current.children[0]
                break
            else:
                self.current = self.current.select()
        value = self.current.rollout(self.player_id)
        self.current.backpropogate(value, self.player_id)

