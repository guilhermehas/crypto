Cryptocurrency
==
[![Build Status](https://travis-ci.org/guilhermehas/crypto.svg?branch=master)](https://travis-ci.org/guilhermehas/crypto)

This project is making an implementation of a copy of bitcoin in python.

## Instalation
Clone the repostitory before install.
```sh=
git clone https://github.com/guilhermehas/crypto
cd crypto
```

### Python
#### Manual Installation
Install python 3.6 and its libraries needed. Run in command line:
```sh=
python3 src/main.py
```

#### Pipenv
Install pipenv and run:
```sh=
pipenv install
pipenv run python3 src/main.py
```

## Running Tests
#### Manual
Install pytest, libraries and run:
```sh=
pytest
```

#### Pipenv
Install pipenv and run:
```sh=
pipenv run pytest
```

## Usage
If you have some questions about command line interface. Use the command:
```sh=
pipenv run python3 src/main.py --help
```
You can specify your wallet, port of using and peers:
### Example
Port 8765, wallet with private key 1
```sh=
pipenv run python3 src/main.py --wallet 1 --port 8765 
```
Port 8766, wallet with private key 3, connected to peer with port 8765
```sh=
pipenv run python3 src/main.py --wallet 3 --port 8766 \
--servers ws://localhost:8765
```
Port 8767, wallet with private key 5, connected to peer with port 8765, 8766
```sh=
pipenv run python3 src/main.py --wallet 5 --port 8767 \
--servers ws://localhost:8765
```

#### Sending web sockets commands:
Send this command to [ws://localhost:8765]() to lock up the blockchain
```json=
{
    "agent": "person",
    "command": "blockchain"
}
```
Send this command to mine a block
```json=
{
    "agent": "person",
    "command": "mine"
}
```
Send this command to send the transaction to person with public key equal to 1 and the amount is 5. The sender is the one which wallet was specified at command line.
```json=
{
	"agent": "person",
	"command": "transaction",
	"receiver": 1,
	"amount": 5
}
```