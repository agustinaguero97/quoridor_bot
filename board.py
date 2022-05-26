from piece import  Pawn

class Board():
    def __init__(self,walls,side,board_string):
        self.walls = walls
        self.side = side
        self.board_string = board_string
        self.board = []
        self.my_pawns = []
        self.opponent_pawns = []
        self.dic_of_posible_movements = {}
        self.direction_of_movement = 1 if self.side == 'N' else -1
        self.count = 0
        self.actual_row,self.actual_col = '',''
        self.new_row,self.new_col = '', ''
        self.score = 0
        self.wall_row,self.wall_col = '',''
        self.orientation = ''
        self.wall_score = ''
    
    
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
                    self.board[x][y] = Pawn(x,y,piece,self.board)
                    #check if this pawn is in my side 
                    if piece == self.side:
                        self.my_pawns.append(self.board[x][y])
                    else:
                        self.opponent_pawns.append(self.board[x][y])
                        self.board[x][y].calculate_score()
        
        
    def board_printer(self):
        print("0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16")
        for x,row in enumerate(self.board):
            print(*row,x,sep = " ; ")
        
        
    #return an object is certain row,col of the board            
    def get_piece(self,row,col):
        return self.board[row][col]
    
    
    #calculate the score of the foward movement
    def foward_score(self,row):
        if self.direction_of_movement == -1:
            #its a 'S' side
            if not row+(self.direction_of_movement*2) == 0:
                return  2**(8-int((row+(self.direction_of_movement*2))/2))
            return 999
        else:
            #its a 'N' side
            if not row+(self.direction_of_movement*2) == 16:
                return 2**(int((row+(self.direction_of_movement*2))/2))
            return 999
    
    
    def side_score(self,row):
        if self.direction_of_movement == -1:
            
            #'S'
            if row == 16:
                return 1
            return (8-int((row)/2))
        else:
            #'N'
            if row == 0:
                return 1
            return (int((row)/2))
    
    
    def check_if_space_is_empty(self,row,col):
        #return a True if the piece is empty (' '), else, return a False
        return self.get_piece(row,col) == ' '
    
    
    #all the best posible placements for walls 
    def posible_wall_placement(self):
        if self.walls == 0:
            return
        for pawn in self.opponent_pawns:
            if pawn.right_edge == False:
                self.front_wall(pawn.row,pawn.col,pawn.direction_of_movement,pawn.name,pawn.pawn_value,direction= 1)
                self.lateral_wall(pawn.row,pawn.col,pawn.direction_of_movement,pawn.name,pawn.pawn_value,direction = 1)
            if pawn.left_edge == False:
                self.front_wall(pawn.row,pawn.col,pawn.direction_of_movement,pawn.name,pawn.pawn_value,direction= -1)
                self.lateral_wall(pawn.row,pawn.col,pawn.direction_of_movement,pawn.name,pawn.pawn_value,direction = -1)
    
    
    def front_wall(self,row,col,direction_of_movement,name,value,direction):
        #check if if has a wall in front of it already
        if not self.check_if_space_is_empty(row+direction_of_movement,col):
            return
        #check if has a pawn in front of it AND if is my pawn or enemy pawn
        if (not self.check_if_space_is_empty(row+(direction_of_movement*2),col)):
            piece = self.get_piece(row+(direction_of_movement*2),col)
            if piece.name != self.side:
                return
        #check for an '*' to the right or left
        if not self.check_if_space_is_empty(row+(direction_of_movement),col+direction):
            return
        #check if the next position to left or right of the pawn movement has a wall or not
        if not self.check_if_space_is_empty(row+(direction_of_movement),col+(direction*2)):
            return
        self.count += 1
        self.wall_row = row if name == 'N' else row -2
        self.wall_col = col if direction == 1 else col-2
        self.orientation = 'h'
        self.wall_score = value
        self.record_a_wall()
        
        
    def lateral_wall(self,row,col,direction_of_movement,name,value,direction):
        #dont place a wall if the opp pawn is in the starting position
        if row == 0 or row == 16:
            return
        #return if the pawn does not have a wall in front of it
        if self.check_if_space_is_empty(row+direction_of_movement,col):
            return
        #return if the pawn has a '*' to the right or left
        if not self.check_if_space_is_empty(row+direction_of_movement,col+direction):
            return
        #return if the pawn has a '|' to the right or left already
        if not self.check_if_space_is_empty(row,col+direction):
            return
        if not self.check_if_space_is_empty(row-(direction_of_movement),col+direction):
            return
        if not self.check_if_space_is_empty(row-(direction_of_movement*2),col+direction):
            return
        self.count += 1
        self.wall_row = row if name == 'S' else row-2
        self.wall_col = col if direction == 1 else col-2
        self.orientation = 'v'
        self.wall_score = value
        self.record_a_wall()
        
        
    def record_a_wall(self):
        self.dic_of_posible_movements[self.count] = {   'row':self.wall_row,
                                                        'col':self.wall_col,
                                                        'orientation':self.orientation,
                                                        'score':self.wall_score,
                                                        'action':'wall'}
        
        
    def record_a_movement(self):
        self.dic_of_posible_movements[self.count]={ 'actual_row':self.actual_row,
                                                    'actual_col':self.actual_col,
                                                    'new_row':self.new_row,
                                                    'new_col':self.new_col,
                                                    'score':self.score,
                                                    'action':'move'}
        
        
    #all posible movements for my side
    def posible_pawn_movements(self):
        for pawn in self.my_pawns:
            self.check_mov_foward(pawn.row,pawn.col,pawn)
            if not pawn.left_edge:
                #check left movement -1 on col
                self.check_side_movement(pawn.row,pawn.col,pawn,direction=-1)
            if not pawn.right_edge:    
                #check right movement +1 on col
                self.check_side_movement(pawn.row,pawn.col,pawn,direction=1)
    
    
    def check_mov_foward(self,row,col,pawn):
        #return if the foward wall space is  true
        if pawn.front_wall:
            return
        #if the pawn space is  not empty
        if (not self.check_if_space_is_empty(row+(self.direction_of_movement*2),col)):
            #see if i can jump that pawn as piece   
            self.check_mov_jump_foward(pawn)
            #check if posible diagonal move to left or right
            if not pawn.left_edge:
                self.check_diagonal_mov(pawn,direction=-1)
            if not pawn.right_edge:
                self.check_diagonal_mov(pawn,direction=1)
            return
        #if the pawn space is empty
        #will not move to a space that is sorrounded by walls
        if self.move_to_confinement(row+(self.direction_of_movement*2),col):
            return
        self.actual_row = row
        self.actual_col = self.new_col = col
        self.new_row= row+(self.direction_of_movement*2)
        self.score = self.foward_score(self.new_row)
        self.count += 1
        self.record_a_movement()
    
    def move_to_confinement(self,row,col):
        if row == 0 or row == 16:
            return
        test_space = Pawn(row,col,self.side,self.board)
        if test_space.front_wall and test_space.left_wall and test_space.right_wall:
            return True
        
    
    def check_diagonal_mov(self,pawn,direction):
        piece = self.get_piece(pawn.row+(self.direction_of_movement*2),pawn.col)
        #cant jump one of my pawns
        if piece.name == self.side:
            return
        if (piece.bottom_edge or piece.top_edge):
            return
        #check if it has a wall the other pawn
        if self.check_if_space_is_empty(piece.row+self.direction_of_movement,piece.col):
            return
        #check if left or right, has a wall
        if not self.check_if_space_is_empty(piece.row,piece.col+direction):
            return
        #check if left or right has a pawn, diagonal move only posible if can land in an empty space
        if not self.check_if_space_is_empty(piece.row,piece.col+(direction*2)):
            return
        self.count += 1
        self.actual_row = pawn.row
        self.actual_col = pawn.col
        self.new_col = piece.col+(direction*2)
        self.new_row = piece.row
        self.score = self.foward_score(self.new_row)
        self.record_a_movement()
    
    
    def check_mov_jump_foward(self,pawn):
        piece = self.get_piece(pawn.row+(self.direction_of_movement*2),pawn.col)
        #cant jump my own pawns
        if piece.name == self.side:
            return
        #cant jump into nothingness
        if (piece.bottom_edge or piece.top_edge):
            return
        if not self.check_if_space_is_empty(piece.row+self.direction_of_movement,piece.col):
            return 
        if  not self.check_if_space_is_empty(piece.row+(self.direction_of_movement*2),piece.col):
            return
        self.actual_row = pawn.row
        self.actual_col = pawn.col
        self.new_row = piece.row+(self.direction_of_movement*2)
        self.new_col = piece.col
        self.score = self.foward_score(self.new_row)
        self.count += 1
        self.record_a_movement()
    
    
    def check_side_movement(self,row,col,pawn,direction):
        #return if has a wall left or right
        if not self.check_if_space_is_empty(row,col+direction):
            return
        #check pawn space
        if not self.check_if_space_is_empty(row,col+(direction*2)):
            #check if is the opponent pawn
            self.side_jump(pawn,direction)
            self.check_diagonal_side_mov(pawn,direction)
            return
        self.new_col = col+(direction*2)
        self.count += 1
        #check if after lateral movement has a wall in the direction of movement
        if  not self.check_if_space_is_empty(row+self.direction_of_movement,self.new_col):
            self.seach_the_exit(row,col,pawn,direction)
            return
        self.actual_row = self.new_row = pawn.row
        self.actual_col = pawn.col
        #self.wall_of_pass(pawn.row,col,direction)
        self.score = self.side_score(self.actual_row)+1
        self.record_a_movement()
    
    #dont know if this truly works
    #this should put a vertical wall to avoid being bloqued by an horizontal wall
    def wall_of_pass(self,row,col,direction):
        if self.walls == 0:
            return
        col_to_check = col+(direction*2)
        if not(row == 2 or row == 14):
            return
        if col_to_check== 0 or col_to_check == 16:
            return
        if not self.check_if_space_is_empty(row+self.direction_of_movement,col_to_check+direction):
            return
        if not self.check_if_space_is_empty(row,col_to_check+direction):
            return
        if not self.check_if_space_is_empty(row-self.direction_of_movement,col_to_check+direction):
            return
        self.count += 1
        self.wall_row = 0 if self.side == 'S' else 14
        self.wall_col = col_to_check-2 if direction == -1 else col_to_check
        self.orientation = 'v'
        self.wall_score = 990
        self.record_a_wall()

    
    
    #ONLY consider a foward diagonal side movement, never check for backwards diagonal side movement
    def check_diagonal_side_mov(self,pawn,direction):
        piece = self.get_piece(pawn.row,pawn.col+(direction*2))
        #cant jump one of my pawns
        if piece.name == self.side:
            return
        #diagonal side move cant occur in the edges
        if piece.left_edge or piece.right_edge:
            return
        #return if piece does not have a wall to the left or right
        if self.check_if_space_is_empty(piece.row,piece.col+direction):
            return
        if piece.back_wall:
            return
        if not self.check_if_space_is_empty(piece.row+(self.direction_of_movement*2),piece.col):
            return
        self.actual_row = pawn.row
        self.actual_col = pawn.col
        self.new_row = piece.row+self.direction_of_movement*2
        self.new_col = piece.col
        self.count += 1
        self.score = self.foward_score(self.new_row)
        self.record_a_movement()
        
    
    def seach_the_exit(self,row,col,pawn,direction):
        new_col = col+(direction*2)
        temp = col+(direction*2)
        while 2<=temp<=14:
            if not self.check_if_space_is_empty(row,temp+direction):
                break
            if not self.check_if_space_is_empty(row,temp+(direction*2)):
                piece = self.get_piece(row,temp+(direction*2))
                if piece.name == self.side:
                    break
            if  not self.check_if_space_is_empty(row+self.direction_of_movement,temp+(direction*2)):
                temp = temp +(direction*2)
                continue
            self.actual_row = self.new_row = row
            self.actual_col = pawn.col
            self.new_col = new_col
            self.score = 0
            self.record_a_movement()
            break
    
    
    def side_jump(self,pawn,direction):
        piece_to_jump = self.get_piece(pawn.row,pawn.col+(direction*2))
        if piece_to_jump.name == self.side:
            return
        if (piece_to_jump.left_edge or piece_to_jump.right_edge):
            return 
        #if wall space isnt empty, stops
        if not self.check_if_space_is_empty(piece_to_jump.row,piece_to_jump.col+direction):
            return 
        #if pawn space isnt empty, stops
        if not self.check_if_space_is_empty(piece_to_jump.row,piece_to_jump.col+(direction*2)):
            return
        self.actual_row = pawn.row
        self.actual_col = pawn.col
        self.new_col = piece_to_jump.col+(direction*2)
        self.new_row = piece_to_jump.row
        self.count += 1
        self.score = self.side_score(piece_to_jump.row)
        self.record_a_movement()
    
    #will only back if has no movement o wall placement available
    def no_movements(self):
        if self.dic_of_posible_movements != {}:
            return
        for pawn in self.my_pawns:
            self.back_move(pawn.row,pawn.col,pawn)
    
    
    def back_move(self,row,col,pawn):
        if pawn.top_edge or pawn.bottom_edge:
            return
        if pawn.back_wall:
            return
        if not self.check_if_space_is_empty(row-(self.direction_of_movement*2),col):
            return
        self.actual_row = row
        self.actual_col = self.new_col = col
        self.new_row = row-(self.direction_of_movement*2)
        self.score = -row
        self.count += 1
        self.record_a_movement()


if __name__ == '__main__':
    #tablero='                       -*- -*- -*-             | |         -*-  * *        | |   | |        * *              | |                                             -*-                                                                                N                               S S              '
    #tablero = '                 -*- -*-                S|           -*-  *          |     |          *                |                                 |                *                |N     N     N    -*- -*- -*- -*-                                                       -*- -*-          S         S  '
    #tablero = '                 -*- -*-                S|           -*-  *          |     |          *                |                                 |                *                |N     N     N    -*- -*- -*- -*-                                                       -*- -*-          S         S  '
    #tablero='                   -*- -*-             |  S|         -*-*   *        |   |   |        *                |                                 |N               *                |      N     N    -*- -*- -*- -*-                 -*- -*- -*- -*-  S                -*-              S                '
    #tablero='                                                                       |     |     | -*-*  -*-*  -*-*   S|    S|    S|                            N                    -*-  N|       |     -*-*-*-    *        |N      |         -*- -*- -*-                                                     '
    #tablero= '                                                                       |     |     | -*-*  -*-*  -*-*   S|    S|    S|                            N                    -*-  N|       |     -*-*-*-    *        |N      |         -*- -*- -*-                                                     '
    #tablero="                       -*-   -*-       |    N     N     *    -*- -*-     |                 -*-        N      |           -*-  *                |         -*- -*-                                 -*-                           -*-   -*-   -*-                                    S           S S"
    #tablero='                       -*- -*-         |  S|            *   *            |   |                               |S  |            *   *            |   |                                                                             -*- -*-             |N   S N N       *  -*- -*-       |         '
    tablero= '  N     N                         S|                *                |                                 |                *                |                                 |N               *                |                 -*- -*- -*- -*-                                              S S  '
    muros = 10.0
    lado = 'N'
    score_1 = 20
    score_2 = 20
    board = Board(muros,lado,tablero)
    board.create_board()
    board.populates_board()
    board.board_printer()
    board.posible_wall_placement()
    board.posible_pawn_movements()
    board.no_movements()
    for k1,v1 in board.dic_of_posible_movements.items():
        print(k1,v1)
