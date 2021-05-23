
import json
#from web3.auto.infura import w3
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
#print(w3.eth.blockNumber)
#print(w3.isConnected())
import pprint

import requests, json
import time, datetime



def sensorData():
    api_key = "d89552e7fddf67b3ca6ad3fd03c9093f"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = "Delhi"

    complete_url = base_url + "q=" + city_name + "&appid=" + api_key 

    response = requests.get(complete_url) 
    x = response.json()
    #print(x)
    y = x["main"]  
    current_temperature = y["temp"] 
    current_pressure = y["pressure"]
    current_humidiy = y["humidity"]
    z = x["weather"] 
    weather_description = z[0]["description"]

    return {'temp': str(current_temperature), 'press': str(current_pressure), 'humid': str(current_humidiy)}

def mineData(privateKey, publicKey, smartContractAddress, data):

    node_url = "http://127.0.0.1:7545"

    web3_instance = Web3(HTTPProvider(node_url))

    print("Connection: ",web3_instance.isConnected())

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
    print("")
    print("Before Transaction #  Num of Tuples: ", contract.functions.numOfTuples().call())

    transaction = contract.functions.mineData(data["temp"], data["press"], data["humid"], data["time"]).buildTransaction({
        'gas': 1000000,
        'gasPrice': Web3.toWei('1', 'gwei'),
        'from': publicKey,
        'nonce': web3_instance.eth.getTransactionCount(publicKey)
    })


    ###############################EXECUTED################################
    signed_txn = web3_instance.eth.account.signTransaction(transaction, private_key=privateKey)
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


    print("After Transaction #  Num of Tuples: ", contract.functions.numOfTuples().call())
    print("")

def main():

    privateKey = input("Sender Account Private Key: ")
    publicKey = input("Sender Account Public Key: ")
    smartContractAddress = input("Address of SC: ")

    while(True):
        e = datetime.datetime.now()
        currTime = e.strftime("%Y-%m-%d::%H:%M:%S")
        data = sensorData()
        data["time"] = str(currTime)
        print("Mining Data: ", data)
        mineData(privateKey,publicKey, smartContractAddress, data)
        time.sleep(15)

main()