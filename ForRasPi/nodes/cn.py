import socket

import urllib.request, json 
from web3.auto import w3
from eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import pprint

node_url = "https://ropsten.infura.io/v3/105a8a2d75f5428789ffd84c8c9b2ba9"

web3_instance = Web3(HTTPProvider(node_url))

print("Blockchain Connection: ",web3_instance.isConnected())


server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Enter the server : ")
server="172.21.12.160" #input()#"172.21.15.117"

#print("Enter the port : ")
port=1234#int(input())


server_socket.connect((server,port))

msg=server_socket.recv(100)	
pub_key=str(msg.decode("utf-8"))
print("public key received: ", pub_key)

msgToSign = input("Enter a message to sign: ")
server_socket.send(bytes(msgToSign,"utf-8"))

signature=server_socket.recv(1000)	
#print(signature)
pubKey = w3.eth.account.recover_message(encode_defunct(text=msgToSign), signature=signature)
print("public key: ", pubKey)

address = web3_instance.toChecksumAddress("0xbc5b9def6ec5d3e5fd75684c1aef853dcdc2a16a")

abi = [
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "nodeIP",
                    "type": "string"
                }
            ],
            "name": "addMaliciousNode",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "bool",
                    "name": "s",
                    "type": "bool"
                }
            ],
            "name": "changeStatus",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "nodeAddresses",
                    "type": "address[]"
                }
            ],
            "name": "declareClusterHeads",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "nodeIP",
                    "type": "string"
                }
            ],
            "name": "removeMaliciousNode",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "inputs": [],
            "name": "wipeAllClusterHeads",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "clusterHeads",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "name": "isClusterHead",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "name": "maliciousNodeIndex",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "maliciousNodes",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "status",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

contract = web3_instance.eth.contract(address = address, abi = abi)

#print(contract.all_functions())

if pub_key == pubKey:
    print("Signature Verified!!!")
    if contract.functions.isClusterHead(pubKey).call():
        print("Verification Successful!!!")
        server_socket.send(bytes("Accepted","utf-8"))
    else:
        print("Verification Unsuccessful!!!")
        server_socket.send(bytes("Rejected","utf-8"))

else:
    print("False Signature!!!")
    server_socket.send(bytes("Rejected","utf-8"))




#client_socket.send(bytes("connected","utf-8"))
#Code to send a msg to sign digitally and verify and declare join