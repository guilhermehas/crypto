import asyncio
import websockets
from examples_to_test import *
from server import *

async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:

        transaction = transactions[0]
        server = ServerUtils()
        transaction_str = server.to_str(transaction)
        #transaction2 = server.to_obj(transaction_str)
        #assert transaction.is_equal(transaction2)

        #name = "joao"
        await websocket.send(transaction_str)
        print(f"> {transaction_str}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())