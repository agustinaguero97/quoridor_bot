from cmath import inf
from tkinter import scrolledtext
import numpy,json,time,random

from piece import  Piece


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
        self.dic_of_posible_movements = {}
        self.action = ''
        self.data = ''
        self.direction_of_movement = 1 if self.side == 'N' else -1

            
        
    def create_board(self):
        #take the string board and transform every element including spaces in elements of a list
        board_string_to_list = [e for e in self.board_string]

        #transform the elements of the previous list into a 17x17 matrix
        self.board = [board_string_to_list[i:i+17] for i in range(0,len(board_string_to_list),17)]


    #make every element of the matrix into a object telling if it is empty,wall or pawn
    def populates_board(self):
        for x,row in enumerate(self.board):
            for y,col in enumerate(row):
                if col == 'N' or col == 'S':
                    self.board[x][y] = Piece(x,y,col,True,False,False)
                    
                    #check if this pawn is in my side 
                    if col == self.side:
                        self.my_pawns.append(self.board[x][y])
                        
                elif col == '-' or col == '|' or col == '*':
                    self.board[x][y] = Piece(x,y,col,False,True,False)
                    continue
                elif col == ' ':
                    self.board[x][y] = Piece(x,y,col,False,False,True)
                    continue
                
        for row in self.board:
            print(row)
    
    #dont have any use yet
    def get_piece(self,row,col):
        return self.board[row][col]
    
    #calculate the score of the movement
    def score(self,pawn):
        if self.direction_of_movement == -1:
            return  2**(8-int((pawn.row+(self.direction_of_movement*2))/2))
        else:
            return 2**int((pawn.row+(self.direction_of_movement*2))/2)
        
    
    #all posbile movments for my side, breaks if some pawn is in an edge
    def posible_movements(self):
        count = 0
        for pawn in self.my_pawns:
            list_of_posible_movements = []
            dic_of_pawn_mov = {}
            #check if it is possible advance 
            if self.board[pawn.row+self.direction_of_movement][pawn.col].wall == False:
                if self.board[pawn.row+(self.direction_of_movement*2)][pawn.col].empty == True:
                    score = Board.score(self,pawn)
                    count +=1
                    dic_of_pawn_mov[1]  ={'row':pawn.row+(self.direction_of_movement*2), 'col':pawn.col,'score':score,'pawn':pawn}
                    #self.dic_of_posible_movements[count]=dic_of_pawn_mov
                    #list_of_posible_movements.append((pawn.row+(self.direction_of_movement*2),pawn.col,score))
                    
            #check if it is posible move to the left
            if not pawn.left_edge:
                if self.board[pawn.row][pawn.col-1].wall == False:
                    if self.board[pawn.row][pawn.col-2].empty == True:
                        count +=1
                        dic_of_pawn_mov[2] ={'row':pawn.row,'col':pawn.col-2,'score':0,'pawn':pawn}
                        #self.dic_of_posible_movements[count]=dic_of_pawn_mov
                        #list_of_posible_movements.append((pawn.row,pawn.col-2,0))

            #check if it is posible move to the right
            if not pawn.right_edge:
                if self.board[pawn.row][pawn.col+1].wall == False:
                    if self.board[pawn.row][pawn.col+2].empty == True:
                        count +=1
                        dic_of_pawn_mov[3]={'row':pawn.row, 'col':pawn.col+2,'score':0,'pawn':pawn}              
                        #self.dic_of_posible_movements[count]=dic_of_pawn_mov                  
                        #list_of_posible_movements.append((pawn.row,pawn.col+2,0))
                    
            self.dic_of_posible_movements[pawn] = dic_of_pawn_mov
            
            

        
    def chose_movement(self):
        max = -inf
        for k1,v1 in self.dic_of_posible_movements.items():
            for k2,v2 in v1.items():
                if max < v2['score']:
                    max = v2['score']
                    best_mov = v2
                    best_pawn = k1



        actual_row ,actual_col =best_pawn.row, best_pawn.col
        print(f"{best_pawn} from  {actual_row},{actual_col} to {best_mov['row']},{best_mov['col']}")
        self.board[actual_row][actual_col], self.board[best_mov['row']][best_mov['col']] = self.board[best_mov['row']][best_mov['col']],self.board[actual_row][actual_col]
        best_pawn.move(best_mov['row'],best_mov['col'])
        
        self.data = {'game_id':self.game_id,
                     'turn_token': self.turn_token,
                     'from_row': actual_row/2,
                     'from_col': actual_col/2,
                     'to_row': best_mov['row']/2,
                     'to_col': best_mov['col']/2,}
        self.action = 'move'
    
    
    def make_movement(self):
        if self.action == 'move':
            return {'action':self.action, 'data': self.data}



    
    
if __name__ == '__main__':
    data = {"board": "  N     N     N                                                                                                                                                                                                                                                              -*-  S     S     S  ",
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

