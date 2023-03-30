from bot import Bot
from board import Board
import unittest
from parameterized import parameterized


class TestBot(unittest.TestCase):
    @parameterized.expand([
        ({
            "board": '      N   N      -*- -*- -*- -*-    S S     S   N                -*-                                                                                                                                                                 -*-                           -*- -*-                       ',
            "walls": 10.0,
            "player_2": "agustin1997aguero@gmail.com",
            "remaining_moves": 195.0,
            "score_2": -20.0,
            "player_1": "enzocrespillo@gmail.com",
            "score_1": 9.0,
            "side": "S",
            "turn_token": "d54c5620-ba0d-4703-8858-bcf1146eadb2",
            "game_id": "a27c7f1e-cd8c-11ec-aef0-7ecdf393f9cc"}, "move", 2, 12),

    ])
    def test_chose_movement(self, data, action, new_row, new_col):
        bot = Bot(data)
        board = Board(bot.walls, bot.side, bot.board_string)
        board.create_board()
        board.populates_board()
        board.posible_pawn_movements()
        board.posible_wall_placement()
        board.no_movements()
        bot.dic_of_posible_movements = board.dic_of_posible_movements
        bot.chose_movement()
        self.assertEqual(bot.best_mov['action'], action)
        self.assertEqual(bot.best_mov['new_row'], new_row)
        self.assertEqual(bot.best_mov['new_col'], new_col)

    """UNFINISHED TEST"""


if __name__ == '__main__':
    unittest.main()
