import argparse
import websockets
import asyncio
import json
import time
# import the board
# from board import Board
from bot import Bot
from constants.constants import (
    PLATFORM_WS,
    CHALLENGE,
    ACCEPT_CHALLENGE,
    CHALLENGE_ID,
    LIST_USER,
    YOUR_TURN,
    GAME_OVER,
    UPDATE_USER_LIST,
    DATA,
    GAME_ID,
    EVENT,
    ACTION,
    USERS,
)


# the token enter as an argument returns it as a variable
def token_parser():
    parser = argparse.ArgumentParser(
        description='Process the token [-h HELP] [-t TOKEN].'
        )
    parser.add_argument(
        '-t', '--token',
        metavar='TOKEN',
        type=str,
        required=True,
        help='enter your token as an argument to iniciate the connection')
    args = parser.parse_args()
    token = args.token
    return token


class Request():
    def __init__(self, request_data):
        self.event = request_data[EVENT]
        self.challengue_id = request_data[DATA][CHALLENGE_ID]
        self.users = request_data[DATA][USERS]
        self.game_id = request_data[DATA][GAME_ID]
        self.data = request_data[DATA]


class Connection():
    def __init__(self, player_token):
        self.url_to_connect = PLATFORM_WS + str(player_token)
        print(self.url_to_connect)
        self.my_answer = {}
        self.request_ws = {}

    async def start_the_connection(self):
        while True:
            try:
                async with websockets.connect(self.url_to_connect) as ws:
                    await self.check_the_data_received(ws)
            except Exception as e:
                print(f"connection error: {e}")

    async def check_the_data_received(self, ws):
        while True:
            try:
                # the time it takes to receive something its absurd some times
                print("waiting for response...")
                recv_sta = time.time()
                self.request_ws = await ws.recv()
                recv_end = time.time()
                print(f"\n time for receive something: {recv_end - recv_sta}")

                # convert the string self.request_ws to a json
                request = Request(json.loads(self.request_ws))

                # logic for acept a challenge
                if request.event == CHALLENGE:
                    self.my_answer = {
                        ACTION: ACCEPT_CHALLENGE,
                        DATA: {
                            CHALLENGE_ID: request.challengue_id
                                }
                    }
                    await conexion.send_data(ws)

                # logic for make a movement
                elif request.event == YOUR_TURN:
                    play_sta = time.time()
                    bot = Bot(request.data)
                    self.my_answer = bot.bot_main_logic()
                    del bot
                    play_end = time.time()
                    print(f"time for make a play: {play_end - play_sta}")
                    await conexion.send_data(ws)

                elif request.event == LIST_USER:
                    print(f"\n users connected: {request.users}")

                elif request.event == GAME_OVER:
                    print(f"\n game over, GAME ID: {request.game_id}")

                elif request.event == UPDATE_USER_LIST:
                    print(f"\n updated user list: {request.data}")

                else:
                    print(f"unknow request event: {self.request_ws}")
                del request

            except Exception as e:
                print(f"ERROR: {e}, reconecting...")
                del request
                break

    async def send_data(self, ws):
        answer = json.dumps(
                            self.my_answer
                            )
        print(answer)
        await ws.send(answer)


if __name__ == '__main__':
    player_token = token_parser()
    conexion = Connection(player_token)
    asyncio.get_event_loop().run_until_complete(
        conexion.start_the_connection()
        )
