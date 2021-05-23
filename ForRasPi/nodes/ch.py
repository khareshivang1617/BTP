import socket
import threading	

import urllib.request, json 
from web3.auto import w3
from eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import pprint

node_url = "https://ropsten.infura.io/v3/105a8a2d75f5428789ffd84c8c9b2ba9"

web3_instance = Web3(HTTPProvider(node_url))

print("Blockchain Connection: ",web3_instance.isConnected())

server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port=1234
print(f"Cluster head created on the port: {port}!!!\n")

server_socket.bind(('',port))
server_socket.listen(6)

pub_key = "0xbAE6e58D470195BeE55b22872d76B342d0e6BF25"#input("Enter CH public key: ")
pri_key = "c59c333e99ddedb9c8e46653b9a8d606a110074678db2c8206b08a29e0f39944"#input("Enter CH private key: ")

def server_thread():

	while True:
	
		client_socket, address = server_socket.accept()
		print(f"Connection with {address} has been established!")

        #Code to receive the msg and digitally sign it
		client_socket.send(bytes(pub_key,"utf-8"))
		
		msg=client_socket.recv(100)
		msgToSign=msg.decode("utf-8")
		print("To sign: ",msgToSign)

		message = encode_defunct(text=msgToSign)
		signed_message = w3.eth.account.sign_message(message, private_key=pri_key)
		#print(signed_message.signature)
		client_socket.send(signed_message.signature)

		msg=client_socket.recv(100)
		joinMsg=msg.decode("utf-8")
		print("Joining invite: ", joinMsg)

#server_thread()

for x in range(0,5):
    new_thread=threading.Thread(target =server_thread)
    new_thread.start()