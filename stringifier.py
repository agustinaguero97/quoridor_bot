



def stringifier(lista_de_lista):
    res = ''
    for el in lista_de_lista:
        res =  res+"".join(el)
    
    return res
    
if __name__ == '__main__':
    #                 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16
    lista_de_lista=[[' ',' ','N',' ',' ',' ',' ',' ','N',' ',' ',' ',' ',' ',' ',' ',' '], #0
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #1 
                    ['S','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #2
                    [' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #3
                    [' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #4
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #5
                    [' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #6
                    [' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #7
                    [' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #8
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #9
                    [' ','|','N',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #10
                    [' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #11
                    [' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #12
                    [' ',' ','-','*','-',' ','-','*','-',' ','-','*','-',' ','-','*','-'], #13
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #14
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '], #15
                    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','S',' ','S',' ',' ']] #16
    
    string = stringifier(lista_de_lista)
    print(f"'{string}'")
    print(len(string))
