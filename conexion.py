
import argparse,websockets,asyncio,os,json
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
    if len(token) == 132:
        return token
    else:
        print('bad token input')
        os._exit(0)


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
            async with websockets.connect(self.url_to_connect) as ws:
                await conexion.check_the_data_received(ws)
        
    async def check_the_data_received(self,ws):
        while True:
            try:
                #self.request will be a string
                self.request = await ws.recv()
                
                
                #convert self.request to a json and put it in request_data
                request_data =json.loads(self.request)
                print(f"what i receive{self.request}")
                
                
                #logic for acept a challenge
                if request_data['event'] == 'challenge':
                    self.my_answer = {
                                        'action': 'accept_challenge',
                                        'data': {
                                                'challenge_id': request_data['data']['challenge_id'] 
                                        }
                    }
                    await conexion.send_data(ws)
                
                #logic for make a movement 
                if request_data['event'] == 'your_turn':
                    board= Board(request_data['data'])

                    board.create_board()
                    board.populates_board()
                    board.posible_movements()
                    board.chose_movement()
                    self.my_answer = board.make_movement()
                    await conexion.send_data(ws)

                
                if request_data['event'] == 'game_over':
                    pass
                
                if request_data['event'] == 'update_user_list':
                    pass
                
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
        print(f"what i send: {answer}")
        await ws.send(answer)
        

            
if __name__ == '__main__':
    player_token = token_parser()
    conexion = Connection(player_token)
    asyncio.get_event_loop().run_until_complete(conexion.start_the_connection())
    
    

