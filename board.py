from piece import  Wall,Pawn

class Board():
    
    def __init__(self,walls,side,board_string,score_1,score_2):
        self.walls = walls
        self.side = side
        self.board_string = board_string
        self.score_1 = score_1
        self.score_2 = score_2
        self.board = []
        self.my_pawns = []
        self.opponent_pawns = []
        self.dic_of_posible_movements = {}
        self.direction_of_movement = 1 if self.side == 'N' else -1
        self.count = 0
        
        
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
                        self.board[x][y].calculate_score()

                elif piece == '-' or piece == '|' or piece == '*':
                    self.board[x][y] = Wall(x,y,piece)

        print("0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16")
        for x,row in enumerate(self.board):
            print(*row,x,sep = " ; ")
            
            
    #all posbile movments for my side
    def posible_pawn_movements(self):
        for pawn in self.my_pawns:
            self.check_mov_foward(pawn)

            #check left movement -1 on col
            if not pawn.left_edge:
                self.check_side_movement(pawn,direction=-1)
            if not pawn.right_edge:    
            #check right movement +1 on col
                self.check_side_movement(pawn,direction=1)


    def posible_wall_placement(self):
        if self.walls == 0:
            return
        for pawn in self.opponent_pawns:
            self.front_wall(pawn)
            
    
    def front_wall(self,pawn):
        #check if if has a wall in front of it already
        if not self.check_if_space_is_empty(pawn.row+pawn.direction_of_movement,pawn.col):
            return
        #check if has a pawn in front of it
        if not self.check_if_space_is_empty(pawn.row+(pawn.direction_of_movement*2),pawn.col):
            return

        if not pawn.right_edge:

            if not self.check_if_space_is_empty(pawn.row+pawn.direction_of_movement,pawn.col+1):
                return
            if not self.check_if_space_is_empty(pawn.row+pawn.direction_of_movement,pawn.col+2):
                return
            self.count += 1
            self.dic_of_posible_movements[self.count] ={
                                                        'row': pawn.row if pawn.name == 'N' else pawn.row -2,
                                                        'col':pawn.col,
                                                        'orientation': 'h',
                                                        'score':pawn.pawn_value,
                                                        'pawn':pawn,
                                                        'action': 'wall'
            }
            
        if not pawn.left_edge:

            if not self.check_if_space_is_empty(pawn.row+pawn.direction_of_movement,pawn.col-1):
                return
            if not self.check_if_space_is_empty(pawn.row+pawn.direction_of_movement,pawn.col-2):
                return
            self.count += 1
            self.dic_of_posible_movements[self.count] ={
                                                        'row': pawn.row if pawn.name == 'N' else pawn.row -2,
                                                        'col':pawn.col-2,
                                                        'orientation': 'h',
                                                        'score':pawn.pawn_value,
                                                        'pawn':pawn,
                                                        'action': 'wall'
            }
            

    #return an object is certain row,col of the board            
    def get_piece(self,row,col):
        return self.board[row][col]
    
    #calculate the score of the foward movement
    def foward_score(self,row):
        if self.direction_of_movement == -1:
            #its a 'S' side
            return  2**(8-int((row+(self.direction_of_movement*2))/2))
        else:
            #its a 'N' side
            return 2**int((row+(self.direction_of_movement*2))/2)
        
    def side_score(self,row):
        if self.direction_of_movement == -1:
            #'S'
            return (7-int((row)/2))
        else:
            #'N'
            return (int((row)/2))
            
                
    def check_if_space_is_empty(self,row,col):
        piece = self.get_piece(row,col)
        if piece == ' ':
            return True
        else:
            return False
    
    def check_if_is_opponent_pawn(self,row,col):
        piece = self.get_piece(row,col)
        if piece.name != self.side:
            return True
        else:
            return False
    

    
    def check_mov_foward(self,pawn):

        #if the foward wall space is empty
        if not self.check_if_space_is_empty(pawn.row+self.direction_of_movement,pawn.col):
            return
        #if the pawn space is empty
        if not self.check_if_space_is_empty(pawn.row+(self.direction_of_movement*2),pawn.col):
            
            if not self.check_if_is_opponent_pawn(pawn.row+(self.direction_of_movement*2),pawn.col):
                return
            piece = self.get_piece(pawn.row+(self.direction_of_movement*2),pawn.col)
            self.check_mov_jump_foward(piece,pawn)
            return
        new_row= pawn.row+(self.direction_of_movement*2)
        self.count += 1
        self.dic_of_posible_movements[self.count]={'row':new_row, 
                                                    'col':pawn.col,
                                                    'score':self.foward_score(new_row),
                                                    'pawn':pawn,
                                                    'action':'move'}
            
        
    def check_mov_jump_foward(self,piece,pawn):
        if (piece.bottom_edge or piece.top_edge):
            return False
        if not self.check_if_space_is_empty(piece.row+self.direction_of_movement,piece.col):
            return False
        if  not self.check_if_space_is_empty(piece.row+(self.direction_of_movement*2),piece.col):
            return False
        new_row = piece.row+(self.direction_of_movement*2)
        self.count += 1
        self.dic_of_posible_movements[self.count] ={'row':new_row, 
                                                    'col':piece.col,
                                                    'score':self.foward_score(new_row),
                                                    'pawn':pawn,
                                                    'action':'move'}

                    
    def check_side_movement(self,pawn,direction):
            #check  wall space
            if not self.check_if_space_is_empty(pawn.row,pawn.col+direction):
                return 
            #check pawn space
            if not self.check_if_space_is_empty(pawn.row,pawn.col+(direction*2)):
                #check if is the opponent pawn
                if  not self.check_if_is_opponent_pawn(pawn.row,pawn.col+(direction*2)):
                    return 
                
                piece = self.get_piece(pawn.row,pawn.col+(direction*2))
                self.side_jump(piece,direction,pawn)
                return
                
            new_col = pawn.col+(direction*2)
            self.count += 1
            #check if after lateral movement has a wall in front
            if  not self.check_if_space_is_empty(pawn.row+self.direction_of_movement,new_col):
                self.dic_of_posible_movements[self.count]={'row':pawn.row,
                                                        'col':new_col,
                                                        #'score':self.side_score(pawn.row),
                                                        'score':0,
                                                        'pawn':pawn,'action':'move'}
                return
            #add one more point if 
            self.dic_of_posible_movements[self.count]={'row':pawn.row,
                                                        'col':new_col,
                                                        'score':self.side_score(pawn.row)+1,
                                                        'pawn':pawn,'action':'move'}
            

    def side_jump(self,piece_to_jump,direction,pawn):
        if (piece_to_jump.left_edge or piece_to_jump.right_edge):
            return 
        #check for a wall space is empty
        if not self.check_if_space_is_empty(piece_to_jump.row,piece_to_jump.col+direction):
            return 
        if not self.check_if_space_is_empty(piece_to_jump.row,piece_to_jump.col+(direction*2)):
            return 
        new_col = piece_to_jump.col+(direction*2)
        self.count += 1
        #check if after making a jump, has a wall in front of it
        if  not self.check_if_space_is_empty(piece_to_jump.row+self.direction_of_movement,piece_to_jump.col+(direction*2)):
            return

        self.dic_of_posible_movements[self.count]={ 'row':piece_to_jump.row,
                                                    'col':new_col,
                                                    'score':self.side_score(piece_to_jump.row)+1,
                                                    'pawn':pawn,
                                                    'action':'move'}


    
if __name__ == '__main__':
    #tablero = '                                                                                     -*-              N                -*-           -*-                S              -*-                                                                                                                       '
    
    #tablero = "  N     N     N                                                                                                                                                                                                                                                                   S     S     S  "
    #tablero = '              N N                 S                                                                                                                                                                                                           N                -*- -*- -*- -*-  S             S  '
    tablero = '                 -*- -*-   -*- -*-  S         S S                                                     N                -*-                                                N                -*-                                                N                -*- -*-                           '
    #tablero  = '              N N                 S                                                                                                                                                                                                           N                -*- -*- -*- -*-  S             S  '
    muros = 10.0
    lado = 'N'
    score_1 = 20
    score_2 = 20
    board = Board(muros,lado,tablero,score_1,score_2)
    board.create_board()
    board.populates_board()
    board.posible_wall_placement()
    board.posible_pawn_movements()
    for k1,v1 in board.dic_of_posible_movements.items():
        print(k1,v1)
