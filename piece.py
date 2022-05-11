ROWS = 16
COLS = 16

class Piece():
    
    def __init__(self,row,col,type_name,pawn,wall,empty):
        self.row = row
        self.col = col
        self.type_name = type_name
        self.wall = wall
        self.pawn = pawn
        self.empty = empty
        self.left_edge = False
        self.right_edge = False
        self.top_edge = False
        self.wall_direction = ''
        
        if self.pawn:
            Piece.check_pawn_border_position(self)
            
        if self.wall:
            if self.type_name == '-':
                self.wall_direction = 'h'
                
            elif self.type_name == '|':
                self.wall_direction = 'v'
                
                
    def move(self,row,col):
        self.row = row
        self.col = col
        Piece.check_pawn_border_position(self)
    
    def check_pawn_border_position(self):
        #if the object is a pawn, check if it is in any border except the botom

        if self.row == 0:
            self.top_edge = True
        else:
            self.top_edge = False
            
        if self.col == COLS:
            self.right_edge = True
        else:
            self.right_edge = False
            
        if self.col == 0:
            self.left_edge = True
        else:
            self.left_edge = False
        
        
    def __repr__(self):
        return str(self.type_name)