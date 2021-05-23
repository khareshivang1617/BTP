#HTTP://127.0.0.1:7545

import json
#from web3.auto.infura import w3
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
#print(w3.eth.blockNumber)
#print(w3.isConnected())
import pprint

node_url = "http://127.0.0.1:7545"

web3_instance = Web3(HTTPProvider(node_url))

print(web3_instance.isConnected())

account="0x2FC62Ea880c6dfb07675D3657A13540c5D987715"
balance = web3_instance.eth.getBalance(account)
print(f"Balance of account {account} : {balance}")


#contract address: 0xd59dcE817b0179a9cf91c62f227C383947EE3aBe

address = web3_instance.toChecksumAddress("0xd59dcE817b0179a9cf91c62f227C383947EE3aBe")

abi = [
        {
            "constant": false,
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
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "constant": true,
            "inputs": [],
            "name": "numOfTuples",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": true,
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": true,
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
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        }
    ]


contract = web3_instance.eth.contract(address = address, abi = abi)
print(contract.all_functions())
print("Before Transaction #  Num of deals: ", contract.functions.numberOfDeals().call())


pub_key = "0x2FEe5F067d3050EBaF5E62C6A2246cf4a3bF2918"
pri_key = "988aa97682e9ac93663265942e773de0669f8d88eca5b51e035671c2f9acb950"#"988AA97682E9AC93663265942E773DE0669F8D88ECA5B51E035671C2f9ACB950"

stringInput = input("Enter a json string: ")

transaction = contract.functions.dealsMade(stringInput).buildTransaction({
    'gas': 1000000,
    'gasPrice': Web3.toWei('1', 'gwei'),
    'from': pub_key,
    'nonce': web3_instance.eth.getTransactionCount(pub_key)
})


###############################EXECUTED################################
signed_txn = web3_instance.eth.account.signTransaction(transaction, private_key=pri_key)
tx = web3_instance.eth.sendRawTransaction(signed_txn.rawTransaction)
#############################################################
tx_hash = web3_instance.toHex(tx)
print("tx_hash = "+tx_hash)
receipt = web3_instance.eth.waitForTransactionReceipt(tx_hash)
print("\n\nTransaction receipt mined:")
pprint.pprint(dict(receipt))
print("\n\nWas transaction successful?")
status = receipt['status']
pprint.pprint(status)


print("After Transaction #  Num of deals: ", contract.functions.numberOfDeals().call())