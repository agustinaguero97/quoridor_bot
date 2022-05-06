import argparse
import websockets
import asyncio
import os
import json

#the token enter as an argument returns it as a variable, make sure that at lest has the len() of a token
def token_parser():
    parser = argparse.ArgumentParser(description='Process the token [-h HELP] [-t TOKEN].')
    parser.add_argument('-t', '--token',
                        metavar='TOKEN', 
                        type=str,
                        default='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWd1c3RpbjE5OTdhZ3Vlcm9AZ21haWwuY29tIn0.IJF-41Cn58L_KcLkLNET80pDxt4F06YWxQ02kZ4VufE',
                        help='enter your token as an argument to iniciate the conexion')
    args = parser.parse_args()
    token = args.token
    if len(token) == 132:
        return token
    else:
        print('bad token input')
        os._exit(0)


class Conexion():
    
    def __init__(self,player_token):
        self.player_token = player_token
        self.url_to_connect = f"wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={self.player_token}"
    
    async def start_the_conection(self):
        async with websockets.connect(self.url_to_connect) as ws:
            await conexion.check_the_data_received(ws)
    
    async def check_the_data_received(self,ws):
        while True:
            request = await ws.recv()
            print(request)
            
if __name__ == '__main__':
    player_token = token_parser()
    conexion = Conexion(player_token)
    asyncio.get_event_loop().run_until_complete(conexion.start_the_conection())
    
    

