ROWS = 16
COLS = 16

class Pawn():
    def __init__(self,row,col,name,board):
        self.board = board
        self.row = row
        self.col = col
        self.name = name
        self.top_edge = True if self.row == 0 else False
        self.bottom_edge = True if self.row == ROWS else False
        self.right_edge = True if self.col == COLS else False
        self.left_edge = True if self.col == 0 else False
        self.pawn_value = ''
        self.direction_of_movement = 1 if self.name == 'N' else -1
        self.front_wall = True
        self.right_wall = True
        self.left_wall = True
        self.back_wall = True
        self.check_for_adjacent_walls_and_pawns()
    #     self.front_pawn = True
    #     self.right_pawn = True
    #     self.left_pawn = True
    #     self.back_pawn = True
    
    
    def check_for_adjacent_walls_and_pawns(self):
        if not self.right_edge:
            self.right_wall = False if self.board[self.row][self.col+1] == ' ' else True
            #self.right_pawn = False if self.board[self.row][self.col+2] == ' ' else True
        if not self.left_edge:
            self.left_wall = False if self.board[self.row][self.col-1] == ' ' else True
            #self.left_pawn = False if self.board[self.row][self.col-2] == ' ' else True
        if not (self.row==16 or self.row == 0) :
            self.back_wall = False if self.board[self.row-self.direction_of_movement][self.col] == ' ' else True
            #self.back_pawn = False if self.board[self.row-self.direction_of_movement*2][self.col] == ' ' else True
        self.front_wall = False if self.board[self.row+self.direction_of_movement][self.col] == ' ' else True
        #self.front_pawn = False if self.board[self.row+self.direction_of_movement*2][self.col] == ' ' else True
        
    
    #called only for opponent pawns
    def calculate_score(self):
        if self.direction_of_movement == -1:
            #its a 'S' side
            if self.row -2 == 0:
                self.pawn_value = 1000
                return
            #self.pawn_value =  2**(8-int((self.row+(self.direction_of_movement*2))/2))
            if self.row == ROWS:
                self.pawn_value = -1
                return
            self.pawn_value =  2**(8-int(self.row/2))
        else:
            #its a 'N' side
            if self.row +2 == ROWS:
                self.pawn_value = 1000
                return
            if self.row == 0:
                self.pawn_value = -1
                
            #self.pawn_value = 2**int((self.row+(self.direction_of_movement*2))/2)
            self.pawn_value =  2**(int(self.row/2))
        
        
    def __repr__(self):
        return str(self.name)
    
    
    # #dont have any use for this method, this will update the row,col and border position if a pawn moves
    # def move(self,row,col):
    #     self.row = row
    #     self.col = col
    #     self.check_pawn_border_position()
    #     self.check_for_adjacent_walls_and_pawns()
    
    # #recalculates all the bottom,top,right,left edges
    # def check_pawn_border_position(self):
    #     #if the object is a pawn, check if it is in any border
    #     self.top_edge = True if self.row == 0 else False
    #     self.bottom_edge = True if self.row == ROWS else False
    #     self.right_edge = True if self.col == COLS else False
    #     self.left_edge = True if self.col == 0 else False
        
if __name__ == '__main__':
    #                 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16
    board   =   [   [' ',' ',' ',' ',' ',' ',' ',' ','N',' ',' ',' ',' ',' ',' ',' ','N'], #0
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','*','-'], #1 
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','S',' ',' ',' ',' '], #2
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','*','-'], #3
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ','S'], #4
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' '], #5
                    [' ',' ',' ',' ',' ',' ',' ',' ','N',' ',' ',' ',' ','|',' ',' ',' '], #6
                    [' ',' ',' ',' ',' ',' ',' ',' ','-','*','-',' ',' ',' ',' ',' ',' '], #7
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #8
                    [' ',' ',' ',' ',' ',' ',' ',' ','-','*','-',' ',' ',' ',' ',' ',' '], #9
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #10
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #11
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #12
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #13
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #14
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #15
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']] #16
    pawn = Pawn(6,8,'N',board)
    print(pawn.back_wall)