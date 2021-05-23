import json
#from web3.auto.infura import w3
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

node_url = "http://127.0.0.1:7545"

web3_instance = Web3(HTTPProvider(node_url))

print("Connection: ",web3_instance.isConnected())

smartContractAddress = input("Smart Contract Address: ")
address = web3_instance.toChecksumAddress(smartContractAddress)
abi = [
        {
            "inputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "string",
                    "name": "temperature",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "pressure",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "humidity",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "dataTime",
                    "type": "string"
                }
            ],
            "name": "mineData",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "numOfTuples",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "sensorData",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "dataSender",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "temp",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "press",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "humid",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "time",
                    "type": "string"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
contract = web3_instance.eth.contract(address = address, abi = abi)
#print(contract.all_functions())

print("Num of Tuples: ", contract.functions.numOfTuples().call())

print("\nData Tuples: ")

for i in range(int(contract.functions.numOfTuples().call())):
    print(contract.functions.sensorData(i).call())