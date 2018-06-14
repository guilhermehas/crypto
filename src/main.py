from app import create_app
import sys

import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Creating criptocurrency')
    parser.add_argument("--port", const=5000, nargs='?', type=int, 
                        help="choose the port to connect")
    parser.add_argument("--ip", const='localhost', nargs='?', type=str, 
                        help="choose the ip server")
    parser.add_argument('--servers', nargs='*',
                        help="servers to connect")
    parser.add_argument("--wallet", const=1, nargs='?', type=int,
                        help="choose the wallet private key")
    args = parser.parse_args()
    args.servers = []
    return args

def get_server(args):
    port = args.port
    ip = args.ip or 'localhost'
    wallet_id = args.wallet or 1
    servers = args.servers or []
    return create_app(my_ip=f'{ip}:{port}', key=wallet_id, servers=servers)

def main():
    args = get_args()
    get_server(args).run(args.port)

if __name__ == '__main__':
    main()