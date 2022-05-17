
import argparse,websockets,asyncio,os,json,time
#import the board
from board import Board
from bot import Bot


#the token enter as an argument returns it as a variable, make sure that at lest has the len() of a token
def token_parser():
    parser = argparse.ArgumentParser(description='Process the token [-h HELP] [-t TOKEN].')
    parser.add_argument('-t', '--token',
                        metavar='TOKEN', 
                        type=str,
                        required=True,
                        help='enter your token as an argument to iniciate the connection')
    args = parser.parse_args()
    token = args.token
    return token

class Connection():
    
    def __init__(self,player_token):
        self.url_to_connect = f"wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={player_token}"
        
        #i dont know if this argument can be change in the middle of use, making wrong answers to a board
        #like working with forks, change the information of the argument when i dont want to
        self.my_answer = {}
        self.request = {}
    
    async def start_the_connection(self):
        
        while True:
            try:
                async with websockets.connect(self.url_to_connect) as ws:
                    print(f"conecting to {self.url_to_connect}")
                    await self.check_the_data_received(ws)

            except Exception as e:
                print(f"connection error: {e}")
                
                
                
    async def check_the_data_received(self,ws):
        while True:
            #clean the terminal
            #os.system('cls' if os.name == 'nt' else 'clear')
            #time.sleep(1)
            
            try:
                #the time it takes to receive something its absurd some times
                self.request = await ws.recv()

                
                #convert the string self.request to a json and put it in request_data
                request_data =json.loads(self.request)
                
                
                #logic for acept a challenge
                if request_data['event'] == 'challenge':
                    self.my_answer = {
                                        'action': 'accept_challenge',
                                        'data': {
                                                'challenge_id': request_data['data']['challenge_id'] 
                                        }
                    }
                    await conexion.send_data(ws)
                
                elif request_data['event'] == 'list_users':
                    print(f"users connected:::{request_data['data']['users']}:::")
                    
                
                #logic for make a movement 
                elif request_data['event'] == 'your_turn':
                    #play_sta = time.time()
                    
                    bot = Bot(request_data['data'])
                    board = Board(bot.walls,bot.side,bot.board_string,bot.score_1,bot.score_2)
                    board.create_board()
                    board.populates_board()
                    board.posible_pawn_movements()
                    board.posible_wall_placement()
                    bot.dic_of_posible_movements = board.dic_of_posible_movements
                    bot.chose_movement()
                    self.my_answer=bot.make_movement()
                    del board,bot
                    
                    #play_end = time.time()
                    #print(f"time for make a play: {play_end-play_sta}")
                    

                    await conexion.send_data(ws)

                elif request_data['event'] == 'game_over':
                    print(f"game over,ID: {request_data['data']['game_id']}")
                    
                
                elif request_data['event'] == 'update_user_list':
                    print(f"update:::{request_data['data']}:::")
                    
            
            except Exception as e:
                print(f"{e}")
                break
            
    #logic where i send the data to the server, where i accept a challenge or make a movement     
    async def send_data(self,ws):
        
        answer = json.dumps(
            {
                'action': self.my_answer['action'],
                'data': self.my_answer['data'],
            
        })
        await ws.send(answer)
        

            
if __name__ == '__main__':
    player_token = token_parser()
    conexion = Connection(player_token)
    asyncio.get_event_loop().run_until_complete(conexion.start_the_connection())
    
    

