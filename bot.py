#here the bot should choose one movement from all the ones that Board class creates
from board import Board
from cmath import inf
#import random
class Bot():
    def __init__(self,data):
        self.player_1 = data['player_1']
        self.player_2 = data['player_2']
        self.score_1 = data['score_1']
        self.score_2 = data['score_2']
        self.turn_token = data['turn_token']
        self.game_id = data['game_id']
        self.walls = data['walls']
        self.side = data['side']
        self.remaining_moves = data['remaining_moves']
        self.board_string = data['board']
        self.data = {}
        self.action = ''
        self.dic_of_posible_movements = {}
        print(f"remaining turns: {self.remaining_moves}")
        print(self.player_1,self.score_1)
        print(self.player_2,self.score_2)
        print(f"my side: {self.side}")
        
        
    def chose_movement(self):
        max = -inf
        best_mov = ""
        #list_of_best_moves = []
        for k1,v1 in self.dic_of_posible_movements.items():
            if max < v1['score']:
                max = v1['score']
                best_mov = v1
        #for k1,v1 in self.dic_of_posible_movements.items():
        #    if v1['score'] == max:
        #        list_of_best_moves.append(v1)
        #if len(list_of_best_moves) > 1:
        #    best_mov =random.choice(list_of_best_moves)
                

        if best_mov['action'] == 'wall':
            self.action = 'wall'
            self.data = {'game_id':self.game_id,
                        'turn_token': self.turn_token,
                        'row': (best_mov['row'])/2,
                        'col': (best_mov['col'])/2,
                        'orientation': best_mov['orientation'],
                }
            print (f"wall in ({best_mov['row']},{(best_mov['col'])}) {best_mov['orientation']}")
            return
        
        if best_mov['action'] == 'move':
            
            
            self.data = {'game_id':self.game_id,
                        'turn_token': self.turn_token,
                        'from_row': best_mov['actual_row']/2,
                        'from_col': best_mov['actual_col']/2,
                        'to_row': best_mov['new_row']/2,
                        'to_col': best_mov['new_col']/2,}
            self.action = 'move'
            print(f"from  ({best_mov['actual_row']},{best_mov['actual_col']}) to ({best_mov['new_row']},{best_mov['new_col']})")

    def make_movement(self):
        return {'action':self.action, 'data': self.data}

        
    
if __name__ == '__main__':
    data = {
        "board":'      N   N      -*- -*- -*- -*-    S S     S   N                -*-                                                                                                                                                                 -*-                           -*- -*-                       ',
        "walls": 10.0,
        "player_2": "agustin1997aguero@gmail.com",
        "remaining_moves": 195.0,
        "score_2": -20.0,
        "player_1": "enzocrespillo@gmail.com",
        "score_1": 9.0,
        "side": "S",
        "turn_token": "d54c5620-ba0d-4703-8858-bcf1146eadb2",
        "game_id": "a27c7f1e-cd8c-11ec-aef0-7ecdf393f9cc"}
    
    
    bot = Bot(data)
    board = Board(bot.walls,bot.side,bot.board_string)
    board.create_board()
    board.populates_board()
    board.board_printer()
    board.posible_pawn_movements()
    board.posible_wall_placement()
    bot.dic_of_posible_movements = board.dic_of_posible_movements
    bot.chose_movement()
    bot.make_movement()
    
    del board
    del bot


