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


class Connection():
    def __init__(self, player_token):
        self.url_to_connect = PLATFORM_WS + str(player_token)
        self.my_answer = {}
        self.request = {}

    async def start_the_connection(self):
        while True:
            try:
                async with websockets.connect(self.url_to_connect) as ws:
                    await self.check_the_data_received(ws)
            except Exception as e:
                print(f"connection error: {e}")

    async def check_the_data_received(self, ws):
        while True:
            # time.sleep(1)
            try:
                # the time it takes to receive something its absurd some times
                print("waiting")
                recv_sta = time.time()
                self.request = await ws.recv()
                recv_end = time.time()
                print(f"\ntime for receive something: {recv_end - recv_sta}")

                # convert the string self.request to a json
                # and put it in request_data
                request_data = json.loads(self.request)

                # logic for acept a challenge
                if request_data[EVENT] == CHALLENGE:
                    self.my_answer = {
                        ACTION: ACCEPT_CHALLENGE,
                        DATA: {
                            CHALLENGE_ID: request_data[DATA][CHALLENGE_ID]
                                }
                    }
                    await conexion.send_data(ws)

                elif request_data[EVENT] == LIST_USER:
                    print(
                        f"\nusers connected:{request_data[DATA][USERS]}:"
                        )

                # logic for make a movement
                elif request_data[EVENT] == YOUR_TURN:
                    play_sta = time.time()

                    bot = Bot(request_data[DATA])
                    self.my_answer = bot.bot_main_logic()
                    del bot

                    play_end = time.time()
                    print(f"time for make a play: {play_end - play_sta}")

                    await conexion.send_data(ws)

                elif request_data[EVENT] == GAME_OVER:
                    print(f"\ngame over,ID: {request_data[DATA][GAME_ID]}")

                elif request_data[EVENT] == UPDATE_USER_LIST:
                    print(f"\nupdate:::{request_data[DATA]}:::")

                else:
                    print(self.request)
            except Exception as e:
                print(f"{e}")
                break

    # logic where i send the data to the server,
    # where i accept a challenge or make a movement
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
