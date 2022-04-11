import copy
import itertools
from typing import TypeAlias
PLAYER1_ID = 1
PLAYER2_ID = 2

PlayerIdType: TypeAlias = int
GameBoardType = list[list[int]]


class InvalidMoveError(Exception):
    ...


class GameBoard():
    def __init__(self, grid: list[list[int]] | None = None) -> None:
        self.grid = grid if grid is not None else [[0]*3, [0]*3, [0]*3]
        self.winner = None

    def can_play(self, y: int, x: int):
        if not(0 <= x < 3) or not(0 <= y < 3):
            return False
        return self.grid[y][x] == 0

    def get_valid_moves(self):
        return [(y, x) for y, x in itertools.product(range(3), repeat=2) if self.can_play(y, x)]

    def has_valid_moves(self) -> bool:
        return len(self.get_valid_moves()) > 0

    def get_player(self):
        player1 = sum([self.grid[y][x] == 1 for
                       y, x in itertools.product(range(3), repeat=2)])
        player2 = sum([self.grid[y][x] == 2 for
                       y, x in itertools.product(range(3), repeat=2)])

        player = None
        if player1 > player2:
            player = PLAYER2_ID
        else:
            player = PLAYER1_ID
        return player

    @staticmethod
    def next_player(player: PlayerIdType) -> PlayerIdType:
        return player % 2 + 1

    def play(self, move: tuple[int, int], player: PlayerIdType | None = None):
        if self.terminal_state():
            result = GameBoard(self.grid.copy())
            result.set_draw()
            return result
        if player is None:
            player = self.get_player()
        grid = copy.deepcopy(self.grid)
        y, x = move
        if self.can_play(y, x):
            grid[y][x] = player
        else:
            raise InvalidMoveError(f"{y}, {x} is invalid move")
        result = GameBoard(grid)
        result.check_win(player)
        result.check_draw()
        return result

    def set_draw(self):
        self.winner = 0

    def set_winner(self, player: PlayerIdType):
        self.winner = player

    def check_draw(self):
        is_draw = self.terminal_state() and not(
            self.has_won(PLAYER1_ID) or self.has_won(PLAYER2_ID))
        if is_draw:
            self.set_draw()
        return is_draw

    def check_win(self, player: PlayerIdType) -> bool:
        victory = self.has_won(player)
        if victory:
            self.set_winner(player)
        return victory

    def has_won(self, player: PlayerIdType) -> bool:
        grid = self.grid
        horizontal_top = grid[0][0] == grid[0][1] == grid[0][2] == player
        horizontal_middle = grid[1][0] == grid[1][1] == grid[1][2] == player
        horizontal_bottom = grid[2][0] == grid[2][1] == grid[2][2] == player

        vertical_left = grid[0][0] == grid[1][0] == grid[2][0] == player
        vertical_middle = grid[0][1] == grid[1][1] == grid[2][1] == player
        vertical_right = grid[0][2] == grid[1][2] == grid[2][2] == player

        diagonal_top_left_to_bottom_right = grid[0][0] == grid[1][1] == grid[2][2] == player
        diagonal_bottom_left_to_top_right = grid[2][0] == grid[1][1] == grid[0][2] == player

        win_conditions = [horizontal_top, horizontal_middle, horizontal_bottom,
                          vertical_left, vertical_middle, vertical_right,
                          diagonal_top_left_to_bottom_right, diagonal_bottom_left_to_top_right]

        return any(win_conditions)

    def terminal_state(self) -> bool:
        return bool(self.winner) or not self.has_valid_moves()

    def __str__(self):
        grid = copy.deepcopy(self.grid)
        row3 = grid[0]
        row2 = grid[1]
        row1 = grid[2]
        result = f'''
       |     |     
3   {row3[0]}`  |  {row3[1]}`  |  {row3[2]}`  
  _____|_____|_____
       |     |     
2   {row2[0]}`  |  {row2[1]}`  |  {row2[2]}`
  _____|_____|_____
       |     |     
1   {row1[0]}`  |  {row1[1]}`  |  {row1[2]}`
       |     |     
    a     b     c
'''
        result = result.replace("0`", " ")
        result = result.replace("1`", "X")
        result = result.replace("2`", "O")
        # result = str(self.grid[0])+"\n" + \
            # str(self.grid[1])+"\n"+str(self.grid[2])+"\n"
        return result
