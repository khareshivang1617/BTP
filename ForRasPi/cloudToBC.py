import urllib.request, json 

from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import pprint


node_url = "https://ropsten.infura.io/v3/105a8a2d75f5428789ffd84c8c9b2ba9"

web3_instance = Web3(HTTPProvider(node_url))

print(web3_instance.isConnected())

account="0x469E8d8144619080c4D18C4e901A3c6F414b37bA"
balance = web3_instance.eth.getBalance(account)
print(f"Balance of account {account} : {balance}")


address = web3_instance.toChecksumAddress("0x62F4904D3D219cddeE2CE1D1b29EF489143335eE")

abi = [
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
		"inputs": [],
		"name": "farmerVerification",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "firmVerification",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "violation",
				"type": "string"
			}
		],
		"name": "reportViolation",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "jsonData",
				"type": "string"
			}
		],
		"name": "storeData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "clauses",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "farmer",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "firm",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "cloud",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "cloudAddress",
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
		"name": "contractClauses",
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
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "data",
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
		"name": "farmerAddress",
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
		"name": "firmAddress",
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
		"name": "isFarmerVerified",
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
		"inputs": [],
		"name": "isFirmVerified",
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
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "violationReported",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
contract = web3_instance.eth.contract(address = address, abi = abi)
print(contract.all_functions())

pub_key = "0x469E8d8144619080c4D18C4e901A3c6F414b37bA"
pri_key = "979969be403011eb42014cde8a5998797158901f8ae5d31401bbcb03106a8b82"

with urllib.request.urlopen("https://api.asksensors.com/read/Xu0jEshU7bzYL46NeEyGbDDX3pubpWND?module=module1&maxResults=1") as url:
    data = json.loads(url.read().decode())
    jsonInput = json.dumps(data[0])

print("Mining the data: ",jsonInput)

transaction = contract.functions.storeData(jsonInput).buildTransaction({
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
