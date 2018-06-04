#!/usr/bin/env python

# WS server example

from examples_to_test import *
import asyncio
import websockets
from server import *

async def hello(websocket, path):
    transaction_str = await websocket.recv()
    print(f"< {transaction_str}")
    server = ServerUtils()
    transaction = server.to_obj(transaction_str)
    print(f"transaction: {transaction.timestamp}")
    assert transaction.is_equal(transactions[0])

    greeting = f"Hello {transaction_str}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
