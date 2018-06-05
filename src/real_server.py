# WS server example

import asyncio
import websockets
from server import *
import argparse
from wallet import *
from json import loads, dumps

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="choose the port", type=int)
parser.add_argument("--wallet", help="choose the wallet private key", type=int)
parser.add_argument('--servers', nargs='*', help="servers to connect")

args = parser.parse_args()
port = 8765
wallet_number = 40
servers_connected = []

if args.port:
    port = args.port
if args.wallet:
    wallet_number = args.wallet
if args.servers:
    servers_connected = args.servers

wallet = Wallet(wallet_number)
server = ServerUtils(wallet)

async def connect_servers():
    for server_connected in servers_connected:
        async with websockets.connect(
            server_connected) as websocket:
                command = {
                    "agent": "machine",
                    "command": "connect",
                    "peer": f'ws://localhost:{port}'
                }
                await websocket.send(dumps(command))



async def hello(websocket, path):
    command_string = await websocket.recv()
    command = loads(command_string)
    if 'agent' in command and command['agent'] == 'machine' and 'command' in command and command['command'] == 'connect':
        peer = command.get('peer',None)
        if peer:
            servers_connected.append(peer)
    if 'agent' in command and command['agent'] == 'person' and 'command' in command and command['command'] == 'transaction':
        command['sender'] = wallet_number

    ret = server.execute(command)
    if 'message' in ret and ret['message']:
        print(ret['message'])
        await websocket.send(dumps(ret))
        if 'command' in ret:
            if ret['command'] == 'blockchain':
                for server_connected in servers_connected:
                    async with websockets.connect(
                        server_connected) as websocket:
                            command = dumps(server.get_command_blockchain())
                            await websocket.send(command)


asyncio.get_event_loop().run_until_complete(connect_servers())

print(f"Server in port ws://localhost:{port}")
start_server = websockets.serve(hello, 'localhost', port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
