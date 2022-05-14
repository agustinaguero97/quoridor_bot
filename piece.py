from sqlite3 import Row


ROWS = 16
COLS = 16
    
    
class Pawn():
    def __init__(self,row,col,name):
        self.row = row
        self.col = col
        self.name = name
        self.type = 'pawn'
        self.top_edge = False
        self.bottom_edge = False
        self.right_edge = False
        self.left_edge = False
        self.check_pawn_border_position()
            
    def check_pawn_border_position(self):
        #if the object is a pawn, check if it is in any border except the botom

        if self.row == 0:
            self.top_edge = True
        else:
            self.top_edge = False
        
        if self.row == ROWS:
            self.bottom_edge = True
        else:
            self.bottom_edge = False
            
        if self.col == COLS:
            self.right_edge = True
        else:
            self.right_edge = False
            
        if self.col == 0:
            self.left_edge = True
        else:
            self.left_edge = False
            

    def move(self,row,col):
        self.row = row
        self.col = col
        self.check_pawn_border_position()
    
    def __repr__(self):
        return str(self.name)
    
class Wall():
    def _init__(self,row,col,name):
        self.row = row
        self.col = col
        self.name = name
        self.type = 'wall'
        self.wall_direction = ''
        

        if self.name == '-':
            self.wall_direction = 'h'
                
        elif self.name == '|':
            self.wall_direction = 'v'
    
    def __repr__(self):
        return str(self.name)

class Empty():
    
    def __init__(self,row,col,name):
        self.row = row
        self.col = col
        self.name = name
        self.type = 'empty'

    def move(self,row,col):
        self.row = row
        self.col = col

    def __repr__(self):
        return str(self.name)
        
    

"""class Piece():
    
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
        self.bottom_edge = False
        self.wall_direction = ''
        
        if self.pawn:
            self.check_pawn_border_position()
            
        if self.wall:
            if self.type_name == '-':
                self.wall_direction = 'h'
                
            elif self.type_name == '|':
                self.wall_direction = 'v'
                
                
    def move(self,row,col):
        self.row = row
        self.col = col
        self.check_pawn_border_position()
    
    def check_pawn_border_position(self):
        #if the object is a pawn, check if it is in any border except the botom

        if self.row == 0:
            self.top_edge = True
        else:
            self.top_edge = False
        
        if self.row == ROWS:
            self.bottom_edge = True
        else:
            self.bottom_edge = False
            
        if self.col == COLS:
            self.right_edge = True
        else:
            self.right_edge = False
            
        if self.col == 0:
            self.left_edge = True
        else:
            self.left_edge = False
        
        
        
    def __repr__(self):
        return str(self.type_name)"""