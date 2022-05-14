
import argparse,websockets,asyncio,os,json,time
#import the board
from board import Board

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
        self.player_token = player_token
        self.url_to_connect = f"wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={self.player_token}"
        
        #i dont know if this argument can be change in the middle of use, making wrong answers to a board
        #like working with forks, change the information of the argument when i dont want to
        self.my_answer = {}
        self.request = {}
    
    async def start_the_connection(self):
        
        while True:
            try:
                async with websockets.connect(self.url_to_connect) as ws:
                    #print(f"conecting to {self.url_to_connect}")
                    await self.check_the_data_received(ws)
                      
            except Exception as e:
                print(f"connection error: {e}")
                
                
                
    async def check_the_data_received(self,ws):
        while True:
            #time.sleep(1)
            #os.system('cls' if os.name == 'nt' else 'clear')
            start = time.time()
            try:
                
                #self.request will be a string
                print("waiting")
                self.request = await ws.recv()
                print("something came!")
                
                #convert self.request to a json and put it in request_data
                request_data =json.loads(self.request)
                #print(f"what i receive{self.request}")
                
                
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
                    play_sta = time.time()
                    
                    board= Board(request_data['data'])
                    board.create_board()
                    board.populates_board()
                    board.posible_movements()
                    board.chose_movement()
                    self.my_answer = board.make_movement()
                    
                    #a fundamental line, wihout the del, it will break
                    del board
                    
                    play_end = time.time()
                    print(f"time for make a play: {play_end-play_sta}")
                    
                    await conexion.send_data(ws)
                    
                    end = time.time()    
                    print(f"time for communication: {end-start}")     
                    
                
                elif request_data['event'] == 'game_over':
                    print(f"game over,ID: {request_data['data']['game_id']}")
                    
                
                elif request_data['event'] == 'update_user_list':
                    print(f"update:::{request_data['data']}:::")
                    
                
                #put this to see if there is any other data that i am receiving
                else:
                    print(request_data)
                    
                
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
        #print(f"what i send: {answer}")
        await ws.send(answer)
        self.my_answer = {}
        

            
if __name__ == '__main__':
    player_token = token_parser()
    conexion = Connection(player_token)
    asyncio.get_event_loop().run_until_complete(conexion.start_the_connection())
    
    

