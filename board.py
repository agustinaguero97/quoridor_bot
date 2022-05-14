

from piece import  Wall,Pawn,Empty


class Board():
    
    def __init__(self,walls,side,board_string):
        self.walls = walls
        self.side = side
        self.board_string = board_string
        self.board = []
        self.my_pawns = []
        self.opponent_pawns = []
        self.dic_of_posible_movements = {}
        self.action = ''
        self.data = ''
        self.direction_of_movement = 1 if self.side == 'N' else -1
        self.dic_of_this_pawn_mov = {}
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

            #check left movement -1 on col
            Board.check_side_movement(self,pawn,direction=-1)
                
            #check right movement +1 on col
            Board.check_side_movement(self,pawn,direction=1)

            self.dic_of_posible_movements[pawn] = self.dic_of_this_pawn_mov
            
            
        for k1,v1 in self.dic_of_posible_movements.items():
            for k2,v2 in v1.items():
                print(k2,v2)
        
        return self.dic_of_posible_movements
    
    #return an object is certain row,col of the board            
    def get_piece(self,row,col):
        return self.board[row][col]
    
    #calculate the score of the movement
    def score(self,pawn):
        
        if self.direction_of_movement == -1:
            #its a 'S' side
            return  2**(8-int((pawn.row+(self.direction_of_movement*2))/2))
        else:
            #its a 'N' side
            return 2**int((pawn.row+(self.direction_of_movement*2))/2)
        
    def side_score(self,pawn):
        if self.direction_of_movement == -1:
            #'S'
            return 2*(8-int((pawn.row)/2))
        else:
            #'N'
            return 2*(int((pawn.row)/2))
            
                
    def check_if_wall_space_is_empty(self,row,col):
        piece = self.get_piece(row,col)
        if piece.type == 'wall':
            del piece
            return False
        else:
            del piece
            return True
    
    
    def check_if_pawn_space_is_empty(self,row,col):
        piece = self.get_piece(row,col)
        if piece.type == 'pawn':
            del piece
            return False
        else:
            del piece
            return True
        
        
    def check_if_is_opponent_pawn(self,row,col):
        piece = self.get_piece(row,col)
        if piece.name != self.side:
            return True
        else:
            return False
    
    
    def check_mov_foward(self,pawn):
        #if the foward wall space is empty
        if self.check_if_wall_space_is_empty(pawn.row+self.direction_of_movement,pawn.col):
            piece = self.get_piece(pawn.row+(self.direction_of_movement*2),pawn.col)
            
            #if the pawn space is empty
            if  self.check_if_pawn_space_is_empty(piece.row,pawn.col):
                
                self.count += 1
                self.dic_of_this_pawn_mov[self.count]  ={'row':piece.row, 'col':piece.col,'score':Board.score(self,piece),'pawn':pawn}
                del piece
            #if the pawn space isnt empty
            else:
                #if the pawn is the opponent pawn
                if self.check_if_is_opponent_pawn(piece.row,piece.col):
                    #check if can jump it, sending his coordenates 
                    Board.check_mov_jump_foward(self,piece,pawn)

                
    def check_mov_jump_foward(self,piece,pawn):
        #check if the piece i am going to jump is a jumpeable piece

        if not (piece.bottom_edge or piece.top_edge):
            #check if the piece i am going to jump has a wall in front of it
            if self.check_if_wall_space_is_empty(piece.row+self.direction_of_movement,piece.col):
                #check if the space i am going to land has a pawn 
                if self.check_if_pawn_space_is_empty(piece.row+(self.direction_of_movement*2),piece.col):
                    space_to_land = self.get_piece(piece.row+(self.direction_of_movement*2),piece.col)
                    self.count += 1
                    self.dic_of_this_pawn_mov[self.count]  ={'row':space_to_land.row, 'col':space_to_land.col,'score':Board.score(self,space_to_land),'pawn':pawn}
                    del space_to_land
                    
    def check_side_movement(self,pawn,direction):
        #check if the pawn is on the left edge or right edge
        if not (pawn.left_edge or pawn.right_edge):
            #if the wall space is empty
            if self.check_if_wall_space_is_empty(pawn.row,pawn.col+direction):
                piece = self.get_piece(pawn.row,pawn.col+(direction*2))
                #if the pawn space is empty
                if self.check_if_pawn_space_is_empty(piece.row,piece.col):
                    #this last check of foward movement check if it is posible after moving sideways,move foward
                    if self.check_if_wall_space_is_empty(piece.row+self.direction_of_movement,piece.col):
                        self.count += 1
                        self.dic_of_this_pawn_mov[self.count] ={'row':piece.row,'col':piece.col,'score':self.side_score(piece),'pawn':pawn}
                        del piece

                #if the pawn space isnt empty
                else:
                    #if the pawn is the opponent pawn
                    if self.check_if_is_opponent_pawn(piece.row,piece.col):
                        #logic of the jump
                        self.side_jump(piece,direction,pawn)
                        
                        
    def side_jump(self,piece_to_jump,direction,pawn):
        if not (piece_to_jump.left_edge or piece_to_jump.right_edge):
             
            if self.check_if_wall_space_is_empty(piece_to_jump.row,piece_to_jump.col+direction):
                if self.check_if_pawn_space_is_empty(piece_to_jump.row,piece_to_jump.col+(direction*2)):
                    space_to_land = self.get_piece(piece_to_jump.row,piece_to_jump.col+(direction*2))
                    
                    if self.check_if_wall_space_is_empty(space_to_land.row+self.direction_of_movement,space_to_land.col):

                        self.count += 1
                        self.dic_of_this_pawn_mov[self.count] ={'row':space_to_land.row,'col':space_to_land.col,'score':self.side_score(space_to_land),'pawn':pawn}
                        del space_to_land
    
    #move a pawn in the board 
    def update_board(self,actual_row,actual_col,new_row,new_col):


        self.board[actual_row][actual_col], self.board[new_row][new_col] = self.board[new_row][new_col],self.board[actual_row][actual_col]
        
        pawn_to_move = self.get_piece(actual_row,actual_col)
        empty_space = self.get_piece(new_row,new_col)
        
        pawn_to_move.move(new_row,new_col)
        empty_space.move(actual_row,actual_col)       

    
if __name__ == '__main__':
    
    tablero = '                                                                                     -*-                S                            -*-              N S                                                                                       N     N                                 S        '
    muros = 10.0
    lado = 'S'

    board = Board(muros,lado,tablero)
    board.create_board()
    board.populates_board()
    board.posible_movements()
