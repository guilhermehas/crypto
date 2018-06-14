from app import create_app
import sys

import argparse

def main():
    parser = argparse.ArgumentParser(description='Creating criptocurrency')
    parser.add_argument("--port", type=int, help="choose the port to connect")
    parser.add_argument("--ip", type=str, help="choose the ip server")
    parser.add_argument('--servers', nargs='*', help="servers to connect")
    parser.add_argument("--wallet", help="choose the wallet private key", type=int)
    args = parser.parse_args()

    port = args.port or 5000
    ip = args.ip or 'localhost'
    wallet_id = args.wallet or 1
    servers = args.servers or []
    create_app(my_ip=f'{ip}:{port}', key=wallet_id, servers=servers).run(port=port)

if __name__ == '__main__':
    main()