# Privv - Truly Private Messaging (Python Prototype) | PBL II 

import socket
import threading
import sys, os
import random
import string
import json

from h11 import Data

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'BlockChain'))
import BlockChain

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AES_Cyptography'))
import AES_Cyptography

# Coloured Terminal Text
from colorama import init
init()
from colorama import Fore, Back, Style

# Initialize BlockChain
blockchain = BlockChain.Blockchain()
genesisBlock = blockchain.head

# Random Key and GroupId Generation
def randomString(stringLength=10):

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# -------------------------------------------------------------------------------------------------------------------

# Server

class Server:

	port = 0
	
	# Creating Socket for connection
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Store list of client connections
	connections = []

	# Setting port address on init class
	# Constructor Method
	def __init__(self,port):
		self.port = port
		self.sock.bind(('0.0.0.0',int(port)))
		self.sock.listen(1)

	
	# Method to send message to client
	# Type "exit"to terminate program
	def sendBroadcast(self):

		while True:
			
			try:
				data = bytes(input(""),'utf-8')
				
				if(len(data.split()) == 2):
					
					BlockChain.editBlock(blockchain,genesisBlock, int(data.split()[1]))
				
				if(data == "exit"):
					
					print("SERVER CLOSED")
					os.kill(os.getpid(), 9)

				
			# Catches error when program terminates (CTRL+C)
			except EOFError as error:
				print("SERVER CLOSED")
				os.kill(os.getpid(), 9)

	
	# Message Handler from Client
	def handler(self, c, a):
	
		while True:
			try:
				data = c.recv(1024)
			
			# Catches error when client disconnects 
			# Remove that client connection
			except Exception as error:
				print(str(a[0])+':'+str(a[1])+" DISCONNECTED")
				self.connections.remove(c)
				c.close()
				break

			# Create New Block Data
			block = BlockChain.Block(data.decode('utf-8'))
			blockchain.mine(block)

			# Send New Block Data Clients
			for connection in self.connections:
				connection.send(bytes(str(block.data),'utf-8'))

			# Disconnect Client program closes
			if not data:
				print(str(a[0])+':'+str(a[1])+" DISCONNECTED")
				self.connections.remove(c)
				c.close()
				break


	# Start Server
	def run(self):

		# Thread to handle input
		iThread = threading.Thread(target=self.sendBroadcast)
		iThread.daemon = True
		iThread.start()
		
		# Clears terminal
		os.system('cls')
		os.system('clear')

		print("""
                                                       
		 ______    ______  	    __     __  __     __ 
		/      \  /      \     /  \   /  |/  \   /  |
		/$$$$$$  |/$$$$$$  |$$ |$$  \ /$$/ $$  \ /$$/ 
		$$ |  $$ |$$ |  $$/ $$ | $$  /$$/   $$  /$$/  
		$$ |__$$ |$$ |      $$ |  $$ $$/     $$ $$/   
		$$    $$/ $$ |      $$ |   $$$/       $$$/    
		$$$$$$$/  $$/       $$/     $/         $/     
		$$ |                                          
		$$ |                                          
		$$/                                           

		-----------Truly Private Messaging----------
                                            
		""")
		
		print(Fore.YELLOW +"		SERVER RUNNING ON PORT "+str(socket.gethostbyname(socket.gethostname()))+":"+str(self.port))
		print(Style.RESET_ALL)

		# Wait for Client connection
		while True:

			c,a = self.sock.accept()
			cThread = threading.Thread(target=self.handler,args=(c,a))
			cThread.daemon = True
			cThread.start()
			
			# Add Client connection to Array
			self.connections.append(c)
			print("\n"+str(a[0])+':'+str(a[1])+" CONNECTED")

# -------------------------------------------------------------------------------------------------------------------

# Client 

class Client:

	# Store GROUP key 
	key_aes = ''

	# Store client NAME
	name = ''

	# Store GROUP ID
	groupId = ''

	# Create Socket connection
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	

	# Method to send message to SERVER
	def sendMsg(self):

		# Message Handler
		while True:
			
			try:
				private_msg = input("")
				
				# Close Program user types "exit
				if(private_msg == "exit"):
					print("\nCONNECTION CLOSED")
					os.kill(os.getpid(), 9)

				secret_key = self.key_aes
				
				# Blockchain Data
				data = {
					"groupId" : str(self.groupId),
					"sender" : str(self.name),
					"msg" : str(AES_Cyptography.AESCipher(secret_key).encrypt(private_msg).decode('utf-8'))
				}

				jsonData = json.dumps(data)
				
				# Sending Data to SERVER
				self.sock.send(bytes(jsonData,"utf-8"))

			except EOFError as error:
				print("\nCONNECTION CLOSED")
				os.kill(os.getpid(), 9)


	# Constructor Method
	def __init__(self,address,port):

		# Socket connection to SERVER
		self.sock.connect((address,int(port)))

		# Clears terminal
		os.system('cls')
		os.system('clear')
		
		print("""
						                    
		 ______    ______  	    __     __  __     __ 
		/      \  /      \     /  \   /  |/  \   /  |
		/$$$$$$  |/$$$$$$  |$$ |$$  \ /$$/ $$  \ /$$/ 
		$$ |  $$ |$$ |  $$/ $$ | $$  /$$/   $$  /$$/  
		$$ |__$$ |$$ |      $$ |  $$ $$/     $$ $$/   
		$$    $$/ $$ |      $$ |   $$$/       $$$/    
		$$$$$$$/  $$/       $$/     $/         $/     
		$$ |                                          
		$$ |                                          
		$$/                                           

		-----------Truly Private Messaging----------
                                            
		""")
		
		self.name = input(" - ENTER YOUR NAME : ")
		print("\n   Press 1 to CREATE New Group")
		print("   Press 2 to JOIN Existing Group")
		
		while True:

			mode = input("\n - Select Mode : ")
			
			# CREATING New Group
			if(mode == "1"):

				print("\n--------CREATING NEW GROUP CHAT--------")
				
				# Generating AES Key
				self.key_aes = randomString(20).upper()

				# Generating Group ID
				self.groupId = randomString(10).upper()

				print(Fore.YELLOW,"\n - Your GroupID : ", str(self.groupId))
				print(Fore.YELLOW,"\n - Your Secrete Group Key : ", str(self.key_aes))
				print(Style.RESET_ALL)
				
				break

			# JOINING Group
			elif(mode == "2"):

				print("\n--------JOINING EXISTING GROUP CHAT--------")

				print(Fore.YELLOW)
				self.groupId = input(" - Enter GroupID : ")
				self.key_aes = input("\n - Enter Secrete Group Key : ")		
				print(Style.RESET_ALL)
				break

			else:
				print("   Invalid Input!")
		

		# ENTERING CHAT ROOM 
		print("--------WELCOME "+self.name+" TO CHAT ROOM--------")
		print("\n - Chat Room "+self.groupId+" Started!\n")
		
		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()
		
		while True:

			data = self.sock.recv(1024)
			
			if not data:
				break
			
			newBlock = json.loads(data.decode("utf-8"))

			# Getting infomation from JSON
			groupId = newBlock["groupId"]
			sender = newBlock["sender"]
			msg = newBlock["msg"]
			
			# Show Messages
			if (groupId == self.groupId):
				print(str(sender) + " : " + str(AES_Cyptography.AESCipher(self.key_aes).decrypt(msg).decode('utf-8')))


# -------------------------------------------------------------------------------------------------------------------

# Terminal Command Handler

if(len(sys.argv)>2):

	# Create CLIENT with IP and PORT
	client = Client(sys.argv[1],sys.argv[2])

else:
	
	# Create SERVER with PORT
	server = Server(sys.argv[1])
	server.run()