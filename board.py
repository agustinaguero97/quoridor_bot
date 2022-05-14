
from cmath import inf
import numpy,json,time,random

from piece import  Wall,Pawn,Empty


class Board():
    
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
        self.board = []
        self.my_pawns = []
        self.opponent_pawns = []
        self.dic_of_posible_movements = {}
        self.action = ''
        self.data = ''
        self.direction_of_movement = 1 if self.side == 'N' else -1
        self.dic_of_this_pawn_mov = {}
        self.count = 0
        print(self.remaining_moves)
        
        
    def evaluate_current_board(self):
        return int(self.score_1) - int(self.score_2)
            
        
    def create_board(self):
        #take the string board and transform every element including spaces in elements of a list
        board_string_to_list = [e for e in self.board_string]

        #transform the elements of the previous list into a 17x17 matrix
        self.board = [board_string_to_list[i:i+17] for i in range(0,len(board_string_to_list),17)]


    #make every element of the matrix into a object telling if it is empty,wall or pawn
    def populates_board(self):
        for x,row in enumerate(self.board):
            for y,piece in enumerate(row):
                if piece == 'N' or piece == 'S':
                    self.board[x][y] = Pawn(x,y,piece)
                    
                    #check if this pawn is in my side 
                    if piece == self.side:
                        self.my_pawns.append(self.board[x][y])
                    else:
                        self.opponent_pawns.append(self.board[x][y])

                elif piece == '-' or piece == '|' or piece == '*':
                    self.board[x][y] = Wall(x,y,piece)
                    continue
                elif piece == ' ':
                    self.board[x][y] = Empty(x,y,piece)
                    continue
                
        for row in self.board:
            print(row)

    #all posbile movments for my side, breaks if some pawn is in an edge
    def posible_movements(self):
        for pawn in self.my_pawns:
            self.dic_of_this_pawn_mov = {}
            self.count = 0
            
            Board.check_mov_foward(self,pawn)

            Board.check_mov_left(self,pawn)
                
            Board.check_mov_right(self,pawn)

            self.dic_of_posible_movements[pawn] = self.dic_of_this_pawn_mov
            
        for k1,v1 in self.dic_of_posible_movements.items():
            for k2,v2 in v1.items():
                print(k2,v2)
                
    def get_piece(self,row,col):
        return self.board[row][col]
    
    #calculate the score of the movement
    def score(self,pawn):
        if self.direction_of_movement == -1:
            return  2**(8-int((pawn.row+(self.direction_of_movement*2))/2))
        else:
            return 2**int((pawn.row+(self.direction_of_movement*2))/2)
        
    def check_mov_foward(self,pawn):
        piece = self.get_piece(pawn.row+self.direction_of_movement,pawn.col)
        
        #if the foward move is a wall or empty space
        #if self.board[pawn.row+self.direction_of_movement][pawn.col].type == 'empty':
        if piece.type == 'empty':
            piece = self.get_piece(pawn.row+(self.direction_of_movement*2),pawn.col)
            #if it is an empty space
            if piece.type == 'empty':
                self.count += 1
                self.dic_of_this_pawn_mov[self.count]  ={'row':piece.row, 'col':piece.col,'score':Board.score(self,piece),'pawn':pawn}
                
            #if it is a pawn and its not one of my pawns
            elif piece.type == 'pawn' and piece.name != self.side:
                Board.check_mov_jump_foward(self,piece,pawn)
                
    def check_mov_jump_foward(self,piece,pawn):

        if not (piece.bottom_edge or piece.top_edge):
            
            piece_to_jump = self.get_piece(piece.row+self.direction_of_movement,piece.col)
            #check if the next  wall space is empty
            if piece_to_jump.type == 'empty':
                #if it is an empty space
                
                piece_to_jump = self.get_piece(piece.row+(self.direction_of_movement*2),piece.col)
                
                if piece_to_jump.type == 'empty':
                    self.count += 1
                    self.dic_of_this_pawn_mov[self.count]  ={'row':piece_to_jump.row, 'col':piece_to_jump.col,'score':Board.score(self,piece_to_jump),'pawn':pawn}

                
    def check_mov_left(self,pawn):
        #check if it is posible move to the left
        if not pawn.left_edge:
            if self.board[pawn.row][pawn.col-1].type == 'empty':
                if self.board[pawn.row][pawn.col-2].type == 'empty':
                    self.count += 1
                    self.dic_of_this_pawn_mov[self.count] ={'row':pawn.row,'col':pawn.col-2,'score':0,'pawn':pawn}
                    
                elif self.board[pawn.row][pawn.col-2].type == 'pawn':
                    Board.check_jump_left(self,self.board[pawn.row][pawn.col-2],pawn)
                    
                    
    def check_jump_left(self,pawn_to_jump,pawn):
        if not pawn_to_jump.left_edge:
            if self.board[pawn_to_jump.row][pawn_to_jump.col-1].type== 'empty':
                if self.board[pawn_to_jump.row][pawn_to_jump.col-2].type == 'empty':
                    self.count += 1
                    self.dic_of_this_pawn_mov[self.count] ={'row':pawn_to_jump.row,'col':pawn_to_jump.col-2,'score':2,'pawn':pawn}
        
                
    
    def check_mov_right(self,pawn):
        #check if it is posible move to the right
        if not pawn.right_edge:
            if self.board[pawn.row][pawn.col+(1)].type == 'empty':
                if self.board[pawn.row][pawn.col+(1*2)].type == 'empty':
                    self.count += 1
                    self.dic_of_this_pawn_mov[self.count]={'row':pawn.row, 'col':pawn.col+(1*2),'score':0,'pawn':pawn}
                    
                elif  self.board[pawn.row][pawn.col+(1*2)].type == 'pawn':
                    
                    Board.check_jump_left(self,self.board[pawn.row][pawn.col+(1*2)],pawn)

                                     
    def check_jump_right(self,pawn_to_jump,pawn):
        if not pawn_to_jump.left_edge:
            if self.board[pawn_to_jump.row][pawn_to_jump.col+(1)].type== 'empty':
                if self.board[pawn_to_jump.row][pawn_to_jump.col+(1*2)].type == 'empty':
                    self.count += 1
                    self.dic_of_this_pawn_mov[self.count] ={'row':pawn_to_jump.row,'col':pawn_to_jump.col+(1*2),'score':2,'pawn':pawn}

    
    def chose_movement(self):
        max = -inf
        best_moves = []
        for k1,v1 in self.dic_of_posible_movements.items():
            for k2,v2 in v1.items():
                if max < v2['score']:
                    max = v2['score']
                    best_mov = v2
                if max == v2['score']:
                    best_moves.append(best_mov)
        if len(best_moves) > 1:
            best_mov = random.choice(best_moves)



        best_pawn = best_mov['pawn']
        actual_row ,actual_col =best_pawn.row, best_pawn.col
        new_row,new_col = best_mov['row'] , best_mov['col']
        print(f"{best_pawn} from  {actual_row},{actual_col} to {new_row},{new_col}")
        self.board[actual_row][actual_col], self.board[new_row][new_col] = self.board[new_row][new_col],self.board[actual_row][actual_col]
        best_pawn.move(new_row,new_col)
        
        self.data = {'game_id':self.game_id,
                     'turn_token': self.turn_token,
                     'from_row': actual_row/2,
                     'from_col': actual_col/2,
                     'to_row': new_row/2,
                     'to_col': new_col/2,}
        self.action = 'move'
    
    
    def make_movement(self):
        if self.action == 'move':
            return {'action':self.action, 'data': self.data}

    
if __name__ == '__main__':
    data = {
        "board": '                                                N                     N     N                           S                                                                                                                                                                               S     S  ',
	    "walls": 10.0,
	    "player_2": "agustin1997aguero@gmail.com",
	    "remaining_moves": 195.0,
	    "score_2": -20.0,
	    "player_1": "enzocrespillo@gmail.com",
	    "score_1": 9.0,
	    "side": "S",
	    "turn_token": "d54c5620-ba0d-4703-8858-bcf1146eadb2",
	    "game_id": "a27c7f1e-cd8c-11ec-aef0-7ecdf393f9cc"}
    board = Board(data)
    board.create_board()
    board.populates_board()
    board.posible_movements()
    board.chose_movement()
    board.make_movement()

