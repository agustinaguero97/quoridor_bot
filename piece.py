
ROWS = 16
COLS = 16
    
    
class Pawn():
    def __init__(self,row,col,name):
        self.row = row
        self.col = col
        self.name = name
        self.top_edge = True if self.row == 0 else False
        self.bottom_edge = True if self.row == ROWS else False
        self.right_edge = True if self.col == COLS else False
        self.left_edge = True if self.col == 0 else False
        self.pawn_value = ''
        self.direction_of_movement = 1 if self.name == 'N' else -1
        #self.check_pawn_border_position()
            
    def check_pawn_border_position(self):
        #if the object is a pawn, check if it is in any border except the botom
        self.top_edge = True if self.row == 0 else False
        self.bottom_edge = True if self.row == ROWS else False
        self.right_edge = True if self.col == COLS else False
        self.left_edge = True if self.col == 0 else False
        

    def move(self,row,col):
        self.row = row
        self.col = col
        self.check_pawn_border_position()
        
    def calculate_score(self):
        if self.direction_of_movement == -1:
            #its a 'S' side
            #self.pawn_value =  2**(8-int((self.row+(self.direction_of_movement*2))/2))
            self.pawn_value =  2**(8-int(self.row/2))
        else:
            #its a 'N' side
            #self.pawn_value = 2**int((self.row+(self.direction_of_movement*2))/2)
            self.pawn_value =  2**(int(self.row/2))
    
    def __repr__(self):
        return str(self.name)
    
class Wall():
    def __init__(self,row,col,name):
        self.row = row
        self.col = col
        self.name = name
        self.wall_direction = ''
        
        if self.name == '-':
            self.wall_direction = 'h'
                
        elif self.name == '|':
            self.wall_direction = 'v'
    
    def __repr__(self):
        return str(self.name)
