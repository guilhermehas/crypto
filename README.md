Cryptocurrency
==
[![Build Status](https://travis-ci.org/guilhermehas/crypto.svg?branch=master)](https://travis-ci.org/guilhermehas/crypto)
[![Coverage Status](https://coveralls.io/repos/github/guilhermehas/crypto/badge.svg?branch=master)](https://coveralls.io/github/guilhermehas/crypto?branch=master)

This project is making an implementation of a copy of bitcoin in python.

## Instalation
Clone the repostitory before install.
```bash
git clone https://github.com/guilhermehas/crypto
cd crypto
```

### Python
#### Manual Installation
Install python 3.6 and its libraries needed. Run in command line:
```bash
python3 src/main.py
```

#### Pipenv
Install pipenv and run:
```bash
pipenv install
pipenv run python3 src/main.py
```

## Running Tests
#### Manual
Install pytest, libraries and run:
```bash
pytest
```

#### Pipenv
Install pipenv and run:
```bash
pipenv run pytest
```

## Usage
If you have some questions about command line interface. Use the command:
```bash
pipenv run python3 src/main.py --help
```
You can specify your wallet, port of using and peers:
### Example
Port 8765, wallet with private key 1
```bash
pipenv run python3 src/main.py --wallet 1 --port 8765 
```
Port 8766, wallet with private key 3, connected to peer with port 8765
```bash
pipenv run python3 src/main.py --wallet 3 --port 8766 \
--servers ws://localhost:8765
```
Port 8767, wallet with private key 5, connected to peer with port 8765, 8766
```bash
pipenv run python3 src/main.py --wallet 5 --port 8767 \
--servers ws://localhost:8765
```

#### HTTP REST API:
Use this command to [http://localhost:8765]() to lock up the blockchain
```
GET /blockchain
```
Send this command to mine a block
```
GET /mine
```
Use this command to send a transaction to person with public key equal to 1 and the amount is 5. The sender is the one which wallet was specified at command line.
```
POST /addtransaction
```
```json
{
	"receiver": 1,
	"amount": 5
}
```